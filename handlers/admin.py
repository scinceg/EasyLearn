from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import button_case_admin
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.utils.markdown import text, bold, italic
from aiogram.types import ParseMode

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()

async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что надо, хозяин?',
     reply_markup=button_case_admin)

async def download(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

async def delete(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            # В телеграме стоит огранияения на 1024 символа при отправке текста вместо с фотографией
            # Ниже одно из решений
            if len(ret[2])>600:
                await bot.send_photo(message.from_user.id, ret[0], 
                text(bold(ret[1]))+'\n\n'+ret[2][:600], parse_mode=ParseMode.MARKDOWN)
                for x in range(200, len(ret[2]), 1000):
                    await bot.send_message(message.from_user.id, ret[2][x:x+1000], parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(message.from_user.id, text='⬆⬆⬆⬆⬆', 
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить', 
                callback_data=f'del {ret[1][:10]}')))
                print(ret[1][:10])
            else:
                await bot.send_photo(message.from_user.id, ret[0], 
                    text(bold(ret[1]))+'\n\n'+ret[2], 
                    parse_mode=ParseMode.MARKDOWN)
                await bot.send_message(message.from_user.id, text='⬆⬆⬆⬆⬆', 
                    reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить', 
                    callback_data=f'del {ret[1][:10]}')))
                print(ret[1][:10])

async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return 
        await state.finish()
        await message.reply("Как скажешь, хозяин ✅")

async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')

async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введите описание')

async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:

        async with state.proxy() as data:
            data['description'] = message.text
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await bot.send_message(message.from_user.id, 'Данные успешано добавлены ✔️',  reply_markup=button_case_admin)

async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text='Запись удалена', show_alert = True)

async def delete_item(message: types.Message):
      if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], text(bold(ret[1]))+'\n\n'+ ret[2], parse_mode=ParseMode.MARKDOWN)
            await bot.send_message(message.from_user.id, text='Удалить', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить', callback_data=f'del {ret[1]}')))

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], state=None)
    dp.register_message_handler(download, Text(equals="Загрузить ✔️"))
    dp.register_message_handler(delete, Text(equals="Удалить ❌"))
    dp.register_message_handler(cancel_handler, Text(equals='Отмена 🚫', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(make_changes_command,commands=['moderator'], is_chat_admin=True )
    dp.register_callback_query_handler(del_callback_run, lambda x:x.data and x.data.startswith('del '))