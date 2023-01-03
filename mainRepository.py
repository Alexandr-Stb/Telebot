import telebot

import boards
import config
import mainData

bot = telebot.TeleBot(config.settings["TOKEN"])


def goMenu(message):
    bot.send_message(message.chat.id, "Главное меню", reply_markup=boards.mainBoard())
    mainData.whereUser = mainData.sections["mMenu"]
