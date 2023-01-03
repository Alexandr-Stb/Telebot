from blackJack import playerCardClass
from telebot import types
import telebot

replyCard = False
playerInGame = False
startGame = False
autoSum = True
aceDown = []
balance = 100
rates = False
gameRate = 0
imageCard = False

userCard = playerCardClass.Player([], 0)
botCard = playerCardClass.Player([], 0)
userCardImage = []
botCardImage = []

