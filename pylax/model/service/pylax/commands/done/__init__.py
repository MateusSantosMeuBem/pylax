# --------------- BUILT-IN PACKAGES ---------------
from time import (
    sleep
)

# --------------- DISCORD PACKAGES ---------------
from discord.ext.commands.context import (
    Context
)
from discord.message import Message

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import (
    Player
)
from model.entities.room import (
    Room
)
from model.instances.pylax import (
    pylax
)
from model.service.pylax.commands.start import (
    start
)
from util.room import (
    findRoomInpylaxByPlayerId
)

# Command to be used when the challenge or the answer is done
@pylax.bot.command()
async def done(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = pylax.bot.get_user(int(player.id))
    player_room: Room = findRoomInpylaxByPlayerId(player.id, pylax)
    for room in pylax.rooms:
        punished_player_ids: list[str] =\
                    [punished_playes.id for punished_playes in room.game.punished_players]
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.fase_controller == 3 and\
        room.game.victim.id == player.id:
            if len([player for player in room.game.players if player.id not in punished_player_ids]) > 1:
                # Clear last votes
                room.game.votes = []

                # Starts the vote to see if people believe in the victim
                message = await context.send("VocÃªs acreditam nessa pessoa?")
                await message.add_reaction("ð")
                await message.add_reaction("ð")
                room.game.id_voting_message = str(message.id)

                # Wait 10 seconds to finish the vote
                number_emojis: list[str] = [
                    "ð", "9ï¸â£", "8ï¸â£", "7ï¸â£", "6ï¸â£", "5ï¸â£", "4ï¸â£", "3ï¸â£", "2ï¸â£", "1ï¸â£", "0ï¸â£"
                ]
                for number_emoji in number_emojis:
                    await message.add_reaction(number_emoji)
                    # if all the players already voted, stop votes 
                    if len(room.game.votes) == len(room.game.players) - 1:
                        try:
                            await message.clear_reaction(number_emoji)
                            break
                        except:
                            await message.clear_reaction(number_emoji)
                            break
                    sleep(1)
                    await message.clear_reaction(number_emoji)

                updated_message: Message = await context.channel.fetch_message(message.id)

                positive: int = 0
                negative: int = 0 
                # Counts the votes
                for reaction in updated_message.reactions:
                    if str(reaction) == "ð":
                        positive = reaction.count
                    elif str(reaction) == "ð":
                        negative = reaction.count

                # Verifies results
                if positive > negative:
                    room.game.victim.stars += 1
                    await context.send(
                        f'<@{room.game.victim.id}>, as pessoas acreditaram em vocÃª.\nMuito bem! Ganhou uma estrelinha.â­'
                    )
                elif negative > positive:
                    room.game.victim.faults += 1
                    await context.send(
                        f'<@{room.game.victim.id}>, as pessoas nÃ£o acreditaram em vocÃª.\nVocÃª vai pagar por isso!ð'
                    )
                    
                    if room.game.victim.faults >= 2:
                        room.game.addPunishedPlayer(
                            player = room.game.victim
                        )
                else:
                    await context.send(
                        f'<@{room.game.victim.id}>, as pessoas ficaram na DÃºvida.\nVocÃª falhou.'
                    )
                room.game.fase_controller = 0
                
                # Remove one fault of each player if it is not a victim
                for punished_player in room.game.punished_players:
                    if punished_player.id != room.game.victim.id:
                        punished_player.faults -= 1
                        if punished_player.faults <= 0:
                            room.game.removePunishedPlayer(
                                id_player = punished_player.id
                            )         

                # Starts a new round after 1s
                sleep(1)
                await start(room.game.master_context)
                break
            else:
                await context.send(f'ð¥ | NÃ£o Ã© possÃ­vel responder agora. Veja o nÃºmero de jogadores ou em que fase estamos.')
        else:
            # [IMPLEMENTS]
            ...
            

# --------------- ALIASES ---------------
def done_aliases() -> None:
    @pylax.bot.command()
    async def feito(context: Context):
        await done(context)