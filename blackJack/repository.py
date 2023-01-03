import random
import telebot

from blackJack import bjData
from blackJack import card
from blackJack import giveCardClass
from blackJack import reactions
from blackJack import messages
from blackJack import boards

bot = telebot.TeleBot("5319244723:AAEdqpK9SA_ZSQGSbtIfwq-zvQkwEBZcgY0")


def startGame(message):
    if bjData.startGame and not bjData.replyCard:
        bjData.replyCard = True
        bjData.playerInGame = True
        replyCard()
        bot.send_message(message.chat.id, "Погнали!", reply_markup=boards.mainGameBoard())
        messages.printMesUserCard(message)

        if bjData.userCard.sum == 21:
            messages.printWonOrLoseMes(message, True)
            bjData.startGame = False

        elif bjData.userCard.sum > 21:

            if checkAce(bjData.userCard):
                messages.printDownAceMessage(message, "USER")

            else:
                messages.printWonOrLoseMes(message, False)
                bjData.startGame = False
    else:
        bot.send_message(message.chat.id, "Что?)")


def replyCard():
    for i in range(2):
        giveRandomCard(bjData.userCard, bjData.botCard)
        giveRandomCard(bjData.botCard, bjData.userCard)

    bjData.replyCard = True


def seeCard(player: object):
    message = ""
    sum = 0

    for i in range(len(player.card)):
        message = f" {message}\n{player.card[i].value} {player.card[i].suit}\n"
        sum = sum + int(player.card[i].point)

    player.sum = sum
    return f"\n{message}"


def giveRandomCard(player: object, observer: object):
    check = False

    while not check:
        point = random.randint(2, 11)
        suit = card.suitCard[random.randint(0, len(card.suitCard) - 1)]
        value = ""

        if point < 10:
            value = f"{point}"

        elif point == 11:
            value = card.ace

        else:
            value = card.highCard[random.randint(0, len(card.highCard) - 1)]

        if checkDuplicate(player.card, observer.card, value, suit):
            player.card.append(giveCardClass.GiveCard(value, point, suit))
            check = True


def checkDuplicate(playerCards: list, observerCards: list, value: str, suit: str):
    for i in range(len(playerCards)):

        if playerCards[i].value == value and playerCards[i].suit == suit:
            return False
    for n in range(len(observerCards)):
        if observerCards[n].value == value and observerCards[n].suit == suit:
            return False
    return True


def quitOrRebootGame(quit):
    if quit:
        bjData.startGame = False

    else:
        bjData.startGame = True
    bjData.aceDown.clear()
    bjData.replyCard = False
    bjData.playerInGame = False
    bjData.botCardImage.clear()
    bjData.userCardImage.clear()
    bjData.botCard.sum = 0
    bjData.botCard.card.clear()
    bjData.userCard.sum = 0
    bjData.userCard.card.clear()
    reactions.numReactions = 0
    bjData.gameRate = 0


def checkAce(player: object):
    for i in range(len(player.card)):

        if player.card[i].value == "Ace" and player.card[i].point == 11:
            player.card[i].point = 1

        seeCard(player)

        if player.sum < 21:
            return True

    return False


def printAceDown(player: object):
    for i in range(len(player.card)):

        if player.card[i].point == 1 and player.card[i].suit not in bjData.aceDown:
            bjData.aceDown.append(player.card[i].suit)
            return player.card[i].suit


def randomReaction(react: object):
    num = random.randint(0, len(react) - 1)
    reactions.numReactions = num
    return react[num][0]


def printStickers(won):
    if won:
        return reactions.won[reactions.numReactions][1]
    else:
        return reactions.losing[reactions.numReactions][1]


def sendCardImage(player: object):
    cardsImage = []
    for i in range(len(player.card)):
        cardsImage.append(telebot.types.InputMediaPhoto(
            open(f'Playing Cards/{player.card[i].suit}/{player.card[i].value}.png', 'rb')))

    return cardsImage
