import telebot
from settings import boards
import mainData
from blackJack import bjData
from settings import repository
from settings import commands

bot = telebot.TeleBot("5319244723:AAEdqpK9SA_ZSQGSbtIfwq-zvQkwEBZcgY0")


def settingsCommands(bot):
    bot.message_handler(func=lambda message: message.text == commands.back)(back)
    bot.message_handler(func=lambda message: message.text == commands.settingsGame)(gameSettings)
    bot.message_handler(func=lambda message: message.text in commands.gameMenu)(autoSumPoints)
    bot.message_handler(func=lambda message: message.text in commands.enableFeatures)(yes)
    bot.message_handler(func=lambda message: message.text in commands.disableFeatures)(no)
    bot.message_handler(func=lambda message: message.text == commands.topUpBalance)(topUpBalance)
    bot.message_handler(func=lambda message: message.text == commands.imageCard)(card)
    bot.message_handler(func=lambda message: message.text in commands.card)(cardSettings)


def menu(message):
    bot.send_message(message.chat.id, "Настройки", reply_markup=boards.settingsBoard())


@bot.message_handler(func=lambda message: message.text == commands.back)
def back(message):
    if mainData.whereUser == mainData.sections["settings"]:
        bot.send_message(message.chat.id, "Назад", reply_markup=boards.settingsBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.settingsGame)
def gameSettings(message):
    if mainData.whereUser == mainData.sections["settings"]:
        bot.send_message(message.chat.id,
                         f"Настройки игры:\n\nАвтосумма очков: {repository.printGameSettings(bjData.autoSum)}\n\n"
                         f"Картинки: {repository.printGameSettings(bjData.imageCard)}\n\n"
                         f"Ставки: {repository.printGameSettings(bjData.rates)}\n\n"
                         f"Баланс: {bjData.balance}💲", reply_markup=boards.settingsGameBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text in commands.gameMenu)
def autoSumPoints(message):
    if mainData.whereUser == mainData.sections["settings"]:
        if message.text == commands.gameMenu[0]:
            if not bjData.autoSum:
                bot.send_message(message.chat.id, "Включить автосумму очков?", reply_markup=boards.autoSumBoard())
            else:
                bot.send_message(message.chat.id, "Выключить автосумму очков?", reply_markup=boards.autoSumBoard())
        else:
            if not bjData.rates:
                bot.send_message(message.chat.id, "Включить ставки?", reply_markup=boards.ratesBoard())
            else:
                bot.send_message(message.chat.id, "Выключить ставки?", reply_markup=boards.ratesBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text in commands.enableFeatures)
def yes(message):
    if mainData.whereUser == mainData.sections["settings"]:
        if message.text == commands.enableFeatures[0]:
            if not bjData.autoSum:
                bjData.autoSum = True
                bot.send_message(message.chat.id, "Автосумма включена", reply_markup=boards.settingsGameBoard())
            else:
                bot.send_message(message.chat.id, "Автосумма уже включена", reply_markup=boards.settingsGameBoard())
        else:
            if not bjData.rates:
                bjData.rates = True
                bot.send_message(message.chat.id, "Ставки включены", reply_markup=boards.settingsGameBoard())
            else:
                bot.send_message(message.chat.id, "Ставки уже включены", reply_markup=boards.settingsGameBoard())

    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text in commands.disableFeatures)
def no(message):
    if mainData.whereUser == mainData.sections["settings"]:
        if message.text == commands.disableFeatures[0]:
            if bjData.autoSum:
                bjData.autoSum = False
                bot.send_message(message.chat.id, "Автосумма выключена", reply_markup=boards.settingsGameBoard())
            else:
                bot.send_message(message.chat.id, "Автосумма уже выключена", reply_markup=boards.settingsGameBoard())
        else:
            if bjData.rates:
                bjData.rates = False
                bot.send_message(message.chat.id, "Ставки выключены", reply_markup=boards.settingsGameBoard())
            else:
                bot.send_message(message.chat.id, "Ставки уже выключены", reply_markup=boards.settingsGameBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.topUpBalance)
def topUpBalance(message):
    if mainData.whereUser == mainData.sections["settings"]:
        if bjData.balance <= 2:
            bjData.balance = 100
            bot.send_message(message.chat.id, f"Баланс успешно пополнен\nТеперь твой баланс: {bjData.balance}💲",
                             reply_markup=boards.settingsGameBoard())
        else:
            bot.send_message(message.chat.id, f"На твоем балансе достаточно денег, чтобы сделать ставку",
                             reply_markup=boards.settingsGameBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.imageCard)
def card(message):
    if mainData.whereUser == mainData.sections["settings"]:
        bot.send_message(message.chat.id, "Какой вид карт тебе сделать?", reply_markup=boards.cardsSettingBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text in commands.card)
def cardSettings(message):
    if mainData.whereUser == mainData.sections["settings"]:
        if message.text == commands.card[0]:
            bjData.imageCard = True
            bot.send_message(message.chat.id, "Окей, буду выдавать карты в виде картинок)",
                             reply_markup=boards.settingsGameBoard())
        else:
            bjData.imageCard = False
            bot.send_message(message.chat.id, "Окей, буду выдавать карты в виде текста)",
                             reply_markup=boards.settingsGameBoard())
