import telebot
from telebot import types
import commands
import mainData

bot = telebot.TeleBot("5319244723:AAEdqpK9SA_ZSQGSbtIfwq-zvQkwEBZcgY0")


def mainBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    game_button = types.KeyboardButton(commands.goGame)
    website = types.KeyboardButton(commands.settings)
    start = types.KeyboardButton(commands.aboutBot)
    exchangeRates = types.KeyboardButton(commands.exchangeRates)

    markup.add(website, start, game_button, exchangeRates)
    return markup
