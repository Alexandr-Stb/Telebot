import telebot
from blackJack import blackJackGame
import boards
from blackJack import bjData
import commands
import mainData
from settings import settingsMenu
from mainData import sections
from exchangeRates import exchangeRatesMenu

bot = telebot.TeleBot("5319244723:AAEdqpK9SA_ZSQGSbtIfwq-zvQkwEBZcgY0")

blackJackGame.blackjackCommands(bot)
# exchangeRatesMenu.exchangeRates(bot)
settingsMenu.settingsCommands(bot)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    if mainData.whereUser == sections["none"]:
        mainData.whereUser = sections["mMenu"]
        bot.send_message(message.chat.id, f"Приветик, {message.from_user.first_name}!", reply_markup=boards.mainBoard())
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEw1NihYKFM_sgHajgD_2v95-YfCzjnwACKwIAArnzlwv7BQOMjG9ozCQE")
        mainData.startBot = True
    else:
        bot.send_message(message.chat.id, "Бот уже запущен")


@bot.message_handler(func=lambda message: message.text == commands.goGame)
def messageStartGame(message):
    if mainData.whereUser == sections["mMenu"]:
        mainData.whereUser = sections["bj"]
        bjData.startGame = True
        bot.send_message(message.chat.id, "Ну давай поиграем))")
        blackJackGame.startGame(message)
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.settings)
def messageStartGame(message):
    if mainData.whereUser == sections["mMenu"]:
        mainData.whereUser = sections["settings"]
        settingsMenu.menu(message)

    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.exchangeRates)
def exchange(message):
    if mainData.whereUser == sections["mMenu"]:
        mainData.whereUser = sections["rates"]
        exchangeRatesMenu.ratesMenu(message)
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.goMenu)
def backMenu(message):
    if mainData.whereUser != mainData.sections["mMenu"]:
        bot.send_message(message.chat.id, "Главное меню", reply_markup=boards.mainBoard())
        mainData.whereUser = mainData.sections["mMenu"]
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.aboutBot)
def messageStartGame(message):
    if not bjData.startGame:
        bot.send_message(message.chat.id, "Я бот крупье, сыграем?)")

    else:
        bot.send_message(message.chat.id, "Что?)")


bot.polling(none_stop=True)
