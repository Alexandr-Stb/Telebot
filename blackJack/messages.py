import telebot
from blackJack import bjData
from blackJack import repository
from blackJack import boards
from blackJack import reactions

bot = telebot.TeleBot("5319244723:AAEdqpK9SA_ZSQGSbtIfwq-zvQkwEBZcgY0")


def printMesUserCard(message):
    if bjData.autoSum:
        if bjData.imageCard:
            repository.seeCard(bjData.userCard)
            bot.send_media_group(message.chat.id, repository.sendCardImage(bjData.userCard))
            bot.send_message(message.chat.id, f"👤 сумма: {bjData.userCard.sum}")
        else:
            bot.send_message(message.chat.id, f"👤 Карты{repository.seeCard(bjData.userCard)}\n"
                                              f"👤 сумма: {bjData.userCard.sum}")
    else:
        if bjData.imageCard:
            repository.seeCard(bjData.userCard)
            bot.send_media_group(message.chat.id, repository.sendCardImage(bjData.userCard))
        else:
            bot.send_message(message.chat.id, f"👤 Карты{repository.seeCard(bjData.userCard)}")


def printMesBotCard(message):
    if bjData.autoSum:
        if bjData.imageCard:
            repository.seeCard(bjData.botCard)
            bot.send_media_group(message.chat.id, repository.sendCardImage(bjData.botCard))
            bot.send_message(message.chat.id, f"🤖 сумма: {bjData.botCard.sum}")
        else:
            bot.send_message(message.chat.id, f"🤖 Карты{repository.seeCard(bjData.botCard)}\n"
                                              f"🤖 сумма: {bjData.botCard.sum}")
    else:
        if bjData.imageCard:
            repository.seeCard(bjData.botCard)
            bot.send_media_group(message.chat.id, repository.sendCardImage(bjData.botCard))
        else:
            bot.send_message(message.chat.id, f"🤖 Карты{repository.seeCard(bjData.botCard)}")


def printEndSum(message):
    if bjData.autoSum:
        bot.send_message(message.chat.id, f"👤 сумма: {bjData.userCard.sum}\n\n"
                                          f"🤖 сумма: {bjData.botCard.sum}", reply_markup=boards.dropBoard())


def requestRate(message):
    if bjData.rates:
        bot.send_message(message.chat.id, f"Делайте ставки!", reply_markup=boards.rateBoard())


def printDownAceMessage(message, botOrUser: str):
    if botOrUser == "USER":
        if bjData.autoSum:
            # bot.send_message(message.chat.id,
            #                  f"Понизил очки 'Ace {repository.printAceDown(bjData.userCard)}' до 1\n👤 сумма: {bjData.userCard.sum}")
            bot.send_message(message.chat.id,
                             f"Понизил очки 'Ace {repository.printAceDown(bjData.userCard)}' до 1\n👤 сумма: {bjData.userCard.sum}")
    elif botOrUser == "BOT":
        if bjData.autoSum:
            bot.send_message(message.chat.id, f"Понизил очки 'Ace {repository.printAceDown(bjData.botCard)}' до 1")


def printWonOrLoseMes(message, won):
    if won:
        if bjData.rates:
            bjData.balance = bjData.balance + bjData.gameRate * 2
            bot.send_message(message.chat.id,
                             f"Твой выйгрыш составил: {bjData.gameRate}💲\n Твой счет: {bjData.balance}💲",
                             reply_markup=boards.dropBoard())
            bot.send_message(message.chat.id,
                             {repository.randomReaction(reactions.won)},
                             reply_markup=boards.dropBoard())
            bot.send_sticker(message.chat.id, repository.printStickers(True))
            bjData.gameRate = 0
            reactions.numReactions = 0
        else:
            bot.send_message(message.chat.id,
                             repository.randomReaction(reactions.won),
                             reply_markup=boards.dropBoard())
            bot.send_sticker(message.chat.id, repository.printStickers(True))
            reactions.numReactions = 0

    else:
        if bjData.rates:
            bot.send_message(message.chat.id,
                             f"Ты проиграл: {bjData.gameRate}💲\n Твой счет: {bjData.balance}💲",
                             reply_markup=boards.dropBoard())
            bot.send_message(message.chat.id,
                             repository.randomReaction(reactions.losing),
                             reply_markup=boards.dropBoard())
            bot.send_sticker(message.chat.id, repository.printStickers(False))
            reactions.numReactions = 0
            bjData.gameRate = 0
        else:
            bot.send_message(message.chat.id,
                             repository.randomReaction(reactions.losing),
                             reply_markup=boards.dropBoard())
            bot.send_sticker(message.chat.id, repository.printStickers(False))
            reactions.numReactions = 0
