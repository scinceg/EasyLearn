import sqlite3 as sq
from create_bot import dp, bot
from aiogram.utils.markdown import text, bold, italic
from aiogram.types import ParseMode

def sql_start():
    global base, cur
    base = sq.connect('Projects\Python\Bots\EasyLearn\easy_learn.db')
    cur = base.cursor()
    if base: 
        print("Data base connected OK!")
    base.execute('''CREATE TABLE IF NOT EXISTS menu(img TEXT, 
    name TEXT PRIMARY KEY, description TEXT)''')
    base.execute('''CREATE TABLE IF NOT EXISTS pars_data(img BLOB, 
    name TEXT PRIMARY KEY, description TEXT)''')
    base.commit()

async def sql_add_command(state):
    global base, cur
    async with state.proxy() as data: 
        cur.execute('INSERT INTO menu VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_add_pars_data(titles, links):
    print(titles, links)
 
async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        if len(ret[2])>600:
                await bot.send_photo(message.from_user.id, ret[0], 
                text(bold(ret[1]))+'\n\n'+ret[2][:600], parse_mode=ParseMode.MARKDOWN)
                for x in range(200, len(ret[2]), 1000):
                    await bot.send_message(message.from_user.id, ret[2][x:x+1000], parse_mode=ParseMode.MARKDOWN)
        else:
               await bot.send_photo(message.from_user.id, ret[0], 
                text(bold(ret[1]))+'\n\n'+ret[2], 
                parse_mode=ParseMode.MARKDOWN)
async def sql_read2():
      return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE substr(name, 1, 10) == ?', (data,))
    base.commit()

