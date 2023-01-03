from telebot import types
from settings import commands


def settingsBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    blackJackSettings = types.KeyboardButton(commands.settingsGame)
    back = types.KeyboardButton(commands.goMenu)
    markup.add(blackJackSettings, back)
    return markup


def settingsGameBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    sum = types.KeyboardButton(commands.gameMenu[0])
    rate = types.KeyboardButton(commands.gameMenu[1])
    topUpBalance = types.KeyboardButton(commands.topUpBalance)
    card = types.KeyboardButton(commands.imageCard)
    back = types.KeyboardButton(commands.back)
    markup.add(sum, rate, topUpBalance, card, back)
    return markup


def cardsSettingBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    image = types.KeyboardButton(commands.card[0])
    text = types.KeyboardButton(commands.card[1])
    markup.add(image, text)
    return markup


def ratesBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes = types.KeyboardButton(commands.enableFeatures[1])
    no = types.KeyboardButton(commands.disableFeatures[1])
    markup.add(yes, no)
    return markup


def autoSumBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes = types.KeyboardButton(commands.enableFeatures[0])
    no = types.KeyboardButton(commands.disableFeatures[0])
    markup.add(yes, no)
    return markup
