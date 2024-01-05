from aiogram import Bot, Dispatcher, executor, types
import os
import time
import sqlite3
from main import process_image, translit_to_eng

bot = Bot('6488256372:AAEgpyLqWUzMKBkHCEeS3Fh0GpFjFx13hVk')
dp = Dispatcher(bot)

colors = {"red": (0, 0, 255),
          "orange": (0, 165, 255),
          "yellow": (0, 255, 255),
          "green": (0, 255, 0),
          "blue": (255, 0, 0),
          "pink": (255, 0, 255),
          }


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup_start = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                             input_field_placeholder="Создай свой уникальный стиль")
    bt1 = types.KeyboardButton('💎Начать')
    markup_start.add(bt1)
    await message.answer(
        f'Привет, {message.from_user.first_name}, этот бот поможет тебе определиться с дизайном маникюра',
        reply_markup=markup_start)


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    markup_info = types.InlineKeyboardMarkup(resize_keyboard=True)
    bt1 = types.InlineKeyboardButton('Связаться с админом💬', url='https://t.me/vldwrr')
    markup_info.add(bt1)
    await message.answer('Для того, чтобы задать свой вопрос, нажмите на кнопку', reply_markup=markup_info)


@dp.message_handler(content_types=['text'])
async def game(message: types.Message):
    if message.text == '💎Начать' or message.text == 'Начать заново🔁':
        await bot.send_message(message.chat.id, 'Отправьте фотографию своей руки')
    elif message.text == "Показать результат":
        for image in os.listdir('user_nails_changed'):
            if translit_to_eng(message.from_user.first_name) in image:
                restart_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                bt1 = types.KeyboardButton("Начать заново🔁")
                restart_markup.add(bt1)
                await bot.send_photo(message.chat.id, photo=open(f"user_nails_changed/{image}", 'rb'),
                                     reply_markup=restart_markup)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await message.photo[-1].download(f'user_nails/'
                                     f'{translit_to_eng(message.from_user.first_name)}.jpg')
    markup_choose_color = types.InlineKeyboardMarkup(resize_keyboard=True)
    bt1 = types.InlineKeyboardButton('красный', callback_data='color_red')
    bt2 = types.InlineKeyboardButton('оранжевый', callback_data='color_orange')
    bt3 = types.InlineKeyboardButton('желтый', callback_data='color_yellow')
    bt4 = types.InlineKeyboardButton('зеленый', callback_data='color_green')
    bt5 = types.InlineKeyboardButton('голубой', callback_data='color_blue')
    bt6 = types.InlineKeyboardButton('розовый', callback_data='color_pink')
    markup_choose_color.add(bt1, bt2, bt3, bt4, bt5, bt6)
    await message.answer('Выберите новый цвет ногтей', reply_markup=markup_choose_color)
    time.sleep(3)
    show_image_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt1 = types.KeyboardButton("Показать результат")
    show_image_markup.add(bt1)

    await bot.send_message(chat_id=message.chat.id, text='Фотография обработана', reply_markup=show_image_markup)


@dp.callback_query_handler(text_startswith='color')
async def create_new_image(callback: types.CallbackQuery):
    color = callback.data.split("_")[1]
    for image in os.listdir('user_nails'):
        if translit_to_eng(callback.from_user.first_name) in image:
            process_image(f'user_nails/{image}', colors[color])


executor.start_polling(dp)