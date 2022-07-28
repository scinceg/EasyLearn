from unittest.mock import call
from aiogram import types, Dispatcher
from create_bot import dp, bot, storage
from keyboards import basic_menu, test_ready, materials_kb, trainer_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import text, bold, italic
import time
import random
from data_base import sqlite_db
from aiogram.types import ParseMode


questions = [
        'I ____ a teacher', 'He ____ like backetball', '____ two songs', 'I am reading. What ____ doing?',
        '____ he go for a walk every evening?' 
]
variants = [
        ['am','are','is'], ['do','doesn\'t','didn\'t'], ['she have','she has got','she is'],
        ['are', 'do', 'is'], ['has','does', 'do']
]
right_answers = ['am', 'doesn\'t', 'she has got', 'are', 'does']

translates_eng = [['play', 'tenis', 'likes', 'he', 'to'], ['?', 'doing', 'are', 'now', 'what', 'you'], ['to', 'been', 'have', 'Paris', 'never', 'I']]
translates_right = [['he', 'likes', 'to', 'play', 'tenis'], ['what', 'are', 'you', 'doing', 'now', '?'], ['I', 'have', 'never','been','to','Paris']]

translates_rus = ['Он любит играть в тенис', 'Чем ты сейчас занимаешься?', 'Я никогда не был в Париже']

news = [
        ['https://polyglot.recipes/media/english/books-literature.jpg', 'Эксперты дали советы для изучения английского языка', 'https://ria.ru/20210423/angliyskiy-1729566275.html'],
        ['https://englishperovo.ru/files/uploads/700.jpg','ЯсноПонятно. Как взрослому учить английский и не бояться делать ошибки?','https://ria.ru/20210624/english-1738308281.html'],
        ['https://visaapp.ru/wp-content/uploads/2019/02/Obuchenie-v-Anglii.jpg', 'I don\'t understand. На каком языке заговорят в Европе после Brexit?', 'https://radiosputnik.ria.ru/20210115/yazyk-1593173521.html']
]

laudatory_msg = ['Все верно, модец!','Так держать!', 'Отлично!']

rights = 0
order = 0
order_tr = 0
click_words = []

async def command_start(message: types.Message):
        await bot.send_message(message.from_user.id, 'Привет! Что интерисует? 🤔 ', 
        reply_markup=basic_menu)
async def text_message(message: types.Message):
        global rights
        if message.text == 'Тестирование 📝':
                await bot.send_message(message.from_user.id, 'Тест состоит из 5 вопросов. Готов?',
                         reply_markup=test_ready)
        if message.text == 'Да':
                for number_of_question in range(len(questions)):
                        variant_kb = InlineKeyboardMarkup(resize_keyboard=True)
                        for variant in variants[number_of_question]:
                                if variant in right_answers:
                                        variant_btn = InlineKeyboardButton(variant, callback_data='right')
                                else: 
                                        variant_btn = InlineKeyboardButton(variant, callback_data='wrong')
                                variant_kb.add(variant_btn)
                        await bot.send_message(message.from_user.id, questions[number_of_question],\
                                reply_markup=variant_kb)
                        time.sleep(4)
                await bot.send_message(message.from_user.id, 
                'Результат теста: {0}/{1}'.format(rights, len(questions)), reply_markup=basic_menu)
        if message.text == 'Нет'  or message.text == 'Назад ◀️':
                  await bot.send_message(message.from_user.id, 'Обратно в главном меню 🔙', reply_markup=basic_menu)
        if message.text == 'Новости 📰':
                one_news_btn = InlineKeyboardButton('Продолжение', url='https://translate.yandex.ru/?lang=ru-en')
                continue_news = InlineKeyboardButton('Еще одну новость', callback_data='more_news')
                one_news_kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(one_news_btn).add(continue_news)
                await bot.send_photo(chat_id=message.chat.id, photo=news[order][0])
                await bot.send_message(message.from_user.id, news[order][1], reply_markup=one_news_kb)
        if message.text == 'Тренажер 🏋🏼':
                  await bot.send_message(message.from_user.id, 'Пришло время улушчить навыки', reply_markup=trainer_kb)
        if message.text == 'Материалы 📚':
                await sqlite_db.sql_read(message)
        if message.text == 'Перевести предложение 💭':
                sentence = translates_eng[order_tr]
                translates_sentence = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
                translate_btn_array = []
                rus_translate = text(italic(translates_rus[order_tr]))
                for word in sentence:
                        word_btn = InlineKeyboardButton(word, callback_data=str(word))
                        translate_btn_array.append(word_btn)
                translates_sentence.row(*translate_btn_array)\
                        .add(InlineKeyboardButton("Отправить", callback_data='translate'))
                msg =  'Переведи предложение и выбери правильную очередность:\n' + rus_translate
                await bot.send_message(message.from_user.id, msg, reply_markup=translates_sentence, parse_mode=ParseMode.MARKDOWN)    

async def translate_word(callback_query: types.CallbackQuery):
        click_words.append(callback_query.data)
        
async def translates_sentences(callback_query: types.CallbackQuery):
        global click_words, translates_right, order_tr, laudatory_msg
        if click_words in translates_right:
                choice = random.choice(laudatory_msg)
                await bot.send_message(callback_query.from_user.id, choice)
                time.sleep(1)
        else:
                msg = 'Не верно, правильный вариант:\n'
                for word in translates_right[order_tr]:
                        msg += text(italic(word)) + ' '
                await bot.send_message(callback_query.from_user.id,  msg, parse_mode=ParseMode.MARKDOWN)
                time.sleep(2)
        click_words = []
        if order_tr<len(translates_eng)-1:
                order_tr +=1
                sentence = translates_eng[order_tr]
                translates_sentence = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
                translate_btn_array = []
                rus_translate = text(italic(translates_rus[order_tr]))
                for word in sentence:
                        word_btn = InlineKeyboardButton(word, callback_data=str(word))
                        translate_btn_array.append(word_btn)
                translates_sentence.row(*translate_btn_array)\
                        .add(InlineKeyboardButton("Отправить", callback_data='translate'))
                msg =  'Переведи предложение и выбери правильную очередность:\n' + rus_translate
                await bot.send_message(callback_query.from_user.id, msg, reply_markup=translates_sentence, parse_mode=ParseMode.MARKDOWN)    
        else: 
                await bot.send_message(callback_query.from_user.id, 'Вопросы закончились 😅')    

async def right_answer(callback_query: types.CallbackQuery):
        global rights
        rights = rights + 1

async def wrong_anwear(callback_query: types.CallbackQuery):
        pass

async def send_more_news(callback_query: types.CallbackQuery):
        global order
        if order<len(news)-1:
                order+=1
                one_news_btn = InlineKeyboardButton('Продолжение', url='https://translate.yandex.ru/?lang=ru-en')
                continue_news = InlineKeyboardButton('Еще одну новость', callback_data='more_news')
                one_news_kb = InlineKeyboardMarkup(resize_keyboard=True).add(one_news_btn).add(continue_news)
                await bot.send_photo(chat_id=callback_query.from_user.id, photo=news[order][0])
                await bot.send_message(callback_query.from_user.id, news[order][1], reply_markup=one_news_kb)
        else: 
                await bot.send_message(callback_query.from_user.id, 'На сегодня все')
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(text_message, content_types=['text'])
    dp.register_callback_query_handler(right_answer, text = 'right')
    dp.register_callback_query_handler(wrong_anwear, text = 'wrong')
    dp.register_callback_query_handler(send_more_news, text = 'more_news')
    dp.register_callback_query_handler(translate_word, lambda x: x.data in translates_eng[order_tr])
    dp.register_callback_query_handler(translates_sentences, text = 'translate')
