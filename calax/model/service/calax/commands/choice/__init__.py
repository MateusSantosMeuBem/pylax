# --------------- BUILT-IN PACKAGES ---------------


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
from model.instances.calax import (
    calax
)
from util.room import (
    findRoomInCalaxByPlayerId
)

# Command to choose if it's verdade or consequencia
@calax.bot.command()
async def choice(
    context: Context,
    option: str = ''
):
    option = option.lower()
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel and\
        room.game.fase_controller == 2 and\
        room.game.victim.id == player.id:
            if option == 'v':
                # It can choose truth
                if room.game.victim.number_of_truths <= 3:
                    room.game.victim.response = 'verdade'
                    await context.send(f'<@{room.game.asker.id}>, faça sua pergunta.')
                    room.game.victim.number_of_truths += 1
                    room.game.fase_controller = 3
                    break
                # It must choose challenge
                else:
                    option = 'c'
                    await context.send(
                        f'<@{room.game.victim.id}> você escolheu 3 vezes verdade. Agora será feito um desafio para você.'
                    )
                    room.game.victim.number_of_truths = 0
            if option == 'c':
                room.game.victim.response = 'consequencia'
                await context.send(f'<@{room.game.asker.id}>, faça seu desafio.')
                room.game.fase_controller = 3
                break
        else:
            ...
            # await context.send(f'Não é possível enviar uma resposta para o bot agora.')