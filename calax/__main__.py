from model.entities.player import Player
from model.entities.room import Room
from model.entities.calax import Calax
from model.instances.calax import calax

from discord.ext.commands import Context

from util import ROOT_PATH

@calax.bot.event
async def on_ready():
  print('Everything running is okay!')

if __name__ == '__main__':
    calax.bot.run(token = calax.bot_token)