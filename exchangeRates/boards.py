from telebot import types
from exchangeRates import commands


def mainBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    usdButton = types.KeyboardButton(commands.rate[0])
    eurButton = types.KeyboardButton(commands.rate[1])
    gbrButton = types.KeyboardButton(commands.rate[2])
    cny = types.KeyboardButton(commands.rate[3])
    leave = types.KeyboardButton(commands.leave)
    markup.add(usdButton, eurButton, gbrButton,cny, leave)
    return markup
