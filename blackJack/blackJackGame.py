import telebot

import mainData
from blackJack import bjData
from blackJack import repository
from blackJack import messages
from blackJack import boards
from blackJack import commands
import mainRepository

bot = telebot.TeleBot("5319244723:AAEdqpK9SA_ZSQGSbtIfwq-zvQkwEBZcgY0")


def blackjackCommands(bot):
    bot.message_handler(func=lambda message: message.text == commands.replyCards)(dealCards)
    bot.message_handler(func=lambda message: message.text == commands.exitGame)(leaveGame)
    bot.message_handler(func=lambda message: message.text == commands.more)(more)
    bot.message_handler(func=lambda message: message.text == commands.again)(again)
    bot.message_handler(func=lambda message: message.text == commands.pas)(pas)
    bot.message_handler(func=lambda message: message.text == commands.placeRate)(goRate)
    bot.message_handler(func=lambda message: message.text == commands.continues)(cont)
    bot.message_handler(func=lambda message: message.text == commands.showPoints)(visibleSum)
    bot.message_handler(func=lambda message: message.text in commands.rates)(getRate)


def startGame(message):
    if bjData.rates:
        bot.send_message(message.chat.id, "Делай ставку",
                         reply_markup=boards.startRateBoard())
    else:
        bot.send_message(message.chat.id, "Начнем!",
                         reply_markup=boards.startGameBoard())


@bot.message_handler(func=lambda message: message.text == commands.placeRate)
def goRate(message):
    if bjData.balance <= 2 and bjData.rates:
        bot.send_message(message.chat.id,
                         f"На твоем балансе не достаточно средств, для ставок\n",
                         reply_markup=boards.leaveGame())
        bot.send_message(message.chat.id,
                         f"Ты можешь пополнить баланс в настройках\nCейчас у тебя: {bjData.balance} 💲")
    else:
        bot.send_message(message.chat.id,
                         f"Сколько ставим?)\nCейчас у тебя: {bjData.balance} 💲",
                         reply_markup=boards.rateBoard())


@bot.message_handler(func=lambda message: message.text == commands.replyCards)
def dealCards(message):
    if bjData.rates and bjData.gameRate != 0:
        repository.startGame(message)
    elif bjData.rates and bjData.gameRate == 0:
        bot.send_message(message.chat.id, "Что?)")
    elif not bjData.rates:
        repository.startGame(message)


@bot.message_handler(func=lambda message: message.text == commands.more)
def more(message):
    if bjData.startGame and bjData.playerInGame:

        if bjData.userCard.sum < 21:
            bot.send_message(message.chat.id, "Держи")
            repository.giveRandomCard(bjData.userCard, bjData.botCard)
            messages.printMesUserCard(message)

        if bjData.userCard.sum == 21:
            messages.printWonOrLoseMes(message, True)
            bjData.startGame = False

        elif bjData.userCard.sum > 21:

            if repository.checkAce(bjData.userCard):
                messages.printDownAceMessage(message, "USER")

            else:
                messages.printWonOrLoseMes(message, False)
                bjData.startGame = False

    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.again)
def again(message):
    if mainData.whereUser == mainData.sections["bj"]:
        if bjData.gameRate != 0:
            bjData.balance = bjData.balance + bjData.gameRate
            bjData.gameRate = 0
        bot.send_message(message.chat.id, "Ну давай повторим")
        repository.quitOrRebootGame(False)
        startGame(message)
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.pas)
def pas(message):
    bjData.playerInGame = False
    cont(message)


@bot.message_handler(func=lambda message: message.text == commands.continues)
def cont(message):
    if bjData.startGame and not bjData.playerInGame:
        messages.printMesBotCard(message)

        if bjData.botCard.sum == bjData.userCard.sum:
            messages.printEndSum(message)
            bot.send_message(message.chat.id, f"Ничья\n может еще партейку?", reply_markup=boards.dropBoard())
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEEw29ihYKvmBVD4spBefA31PxcsBRamwACPAEAArnzlwvMnvUK9IcNFSQE")
            bjData.startGame = False

        elif bjData.botCard.sum == 21:
            messages.printEndSum(message)
            messages.printWonOrLoseMes(message, False)
            bjData.startGame = False

        elif bjData.userCard.sum < bjData.botCard.sum < 21:
            messages.printEndSum(message)
            messages.printWonOrLoseMes(message, False)
            bjData.startGame = False

        elif bjData.botCard.sum > 21:

            if repository.checkAce(bjData.botCard):
                # messages.printDownAceMessage(message, "BOT")
                if bjData.autoSum:
                    bot.send_message(message.chat.id, f"Добавлю себе еще одну карту\n Сумма: {bjData.botCard.sum}",
                                     reply_markup=boards.continueBoard())
                else:
                    bot.send_message(message.chat.id, f"Добавлю себе еще одну карту",
                                     reply_markup=boards.continueBoard())
                repository.giveRandomCard(bjData.botCard, bjData.userCard)
            else:
                messages.printEndSum(message)
                messages.printWonOrLoseMes(message, True)
                bjData.startGame = False
        else:
            bot.send_message(message.chat.id, "Добавлю себе еще одну карту", reply_markup=boards.continueBoard())
            repository.giveRandomCard(bjData.botCard, bjData.userCard)

    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.exitGame)
def leaveGame(message):
    if mainData.whereUser == mainData.sections["bj"]:
        if bjData.gameRate != 0:
            bjData.balance = bjData.balance + bjData.gameRate
            bjData.gameRate = 0
        repository.quitOrRebootGame(True)
        mainRepository.goMenu(message)
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text == commands.showPoints)
def visibleSum(message):
    if not bjData.startGame and mainData.whereUser == mainData.sections["bj"] and not bjData.autoSum:
        bjData.autoSum = True
        messages.printEndSum(message)
        bjData.autoSum = False
    else:
        bot.send_message(message.chat.id, "Что?)")


@bot.message_handler(func=lambda message: message.text in commands.rates)
def getRate(message):
    if message.text != commands.rates[5]:
        if mainData.whereUser == mainData.sections["bj"] and bjData.rates and bjData.gameRate == 0:
            if bjData.balance - int(message.text) >= 0:
                bjData.gameRate = int(message.text)
                bjData.balance = bjData.balance - bjData.gameRate
                bot.send_message(message.chat.id,
                                 f" Ставка принята")
                dealCards(message)
            elif bjData.balance - int(message.text) < 0:
                bot.send_message(message.chat.id,
                                 f"На твоем счете не достаточно средств, для ставки\nCейчас у тебя: {bjData.balance} 💲",
                                 reply_markup=boards.rateBoard())
            else:
                bot.send_message(message.chat.id, "Что?)")
        else:
            bot.send_message(message.chat.id, "ЭЭЭЭЭ")
    elif mainData.whereUser == mainData.sections["bj"] and bjData.rates and bjData.gameRate == 0 and message.text == \
            commands.rates[5]:
        if bjData.balance != 0:
            bjData.gameRate = int(bjData.balance)
            bjData.balance = bjData.balance - bjData.gameRate
            bot.send_message(message.chat.id,
                             f" Ставка принята")
            dealCards(message)
        else:
            bot.send_message(message.chat.id,
                             f"На твоем счете не достаточно средств, для ставки\nCейчас у тебя: {bjData.balance} 💲",
                             reply_markup=boards.rateBoard())
    else:
        bot.send_message(message.chat.id, "Что?)")



