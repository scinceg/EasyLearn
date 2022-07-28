from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from parsing import pars

async def on_startup(_):
	sqlite_db.sql_start()
	x = pars.parst_start()
	
from handlers import client, admin

admin.register_handlers_admin(dp)
client.register_handlers_client(dp) 

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)