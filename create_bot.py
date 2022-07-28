from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = '5489718919:AAFLWBLyt6cNK8s_Hur8YE-j1Q4_R-ui4tY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

