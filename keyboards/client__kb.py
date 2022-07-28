from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

test = KeyboardButton('Тестирование 📝')
materials = KeyboardButton('Материалы 📚')
news = KeyboardButton('Новости 📰')
trainer = KeyboardButton('Тренажер 🏋🏼')
basic_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
basic_menu.add(test, materials, news, trainer)

yes = KeyboardButton('Да')
no = KeyboardButton('Нет')
test_ready = ReplyKeyboardMarkup(resize_keyboard=True)
test_ready.add(yes, no)

trainer_kb = ReplyKeyboardMarkup(resize_keyboard=True)
new_word = KeyboardButton('Новое слово 🆕')
translate = KeyboardButton('Перевести предложение 💭     ')
trainer_kb.add(new_word, translate)

movies = KeyboardButton('Фильмы 📽')
benefits = KeyboardButton('Пособия 📗')
books = KeyboardButton('Книги 📚')
articles = KeyboardButton('Статьи 📑')
back = KeyboardButton('Назад ◀️')
materials_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
materials_kb.add(movies, benefits, books, articles, back)



