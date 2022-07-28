from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('Загрузить ✔️')
button_delete = KeyboardButton('Удалить ❌')
cancel = KeyboardButton('Отмена 🚫')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load, button_delete).add(cancel)


