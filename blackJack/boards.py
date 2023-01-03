from telebot import types
from blackJack import bjData
from blackJack import commands


def startRateBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = types.KeyboardButton(commands.exitGame)
    if bjData.rates:
        deal_cards = types.KeyboardButton(commands.placeRate)
    else:
        deal_cards = types.KeyboardButton(commands.replyCards)

    markup.add(deal_cards, back)
    return markup


def startGameBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    deal_cards = types.KeyboardButton(commands.replyCards)
    back = types.KeyboardButton(commands.exitGame)
    markup.add(deal_cards, back)
    return markup


def mainGameBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    more = types.KeyboardButton(commands.more)
    pas = types.KeyboardButton(commands.pas)
    out = types.KeyboardButton(commands.exitGame)
    play_again = types.KeyboardButton(commands.again)

    markup.add(more, pas, out, play_again)
    return markup


def dropBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    leave = types.KeyboardButton(commands.exitGame)
    reboot = types.KeyboardButton(commands.again)
    visSum = types.KeyboardButton(commands.showPoints)
    if bjData.autoSum:
        markup.add(reboot, leave)
    else:
        markup.add(reboot, visSum, leave)
    return markup


def leaveGame():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    leave = types.KeyboardButton(commands.exitGame)
    markup.add(leave)
    return markup


def rateBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    leave = types.KeyboardButton(commands.exitGame)
    two = types.KeyboardButton(commands.rates[0])
    five = types.KeyboardButton(commands.rates[1])
    ten = types.KeyboardButton(commands.rates[2])
    fifty = types.KeyboardButton(commands.rates[3])
    hundred = types.KeyboardButton(commands.rates[4])
    allIn = types.KeyboardButton(commands.rates[5])
    markup.add(two, five, ten, fifty, hundred,allIn, leave)
    return markup




def continueBoard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    continues = types.KeyboardButton(commands.continues)
    leave = types.KeyboardButton(commands.exitGame)
    markup.add(continues, leave)
    return markup
