# import datetime
# import urllib3
# import xmltodict
#
# import mainData
# from exchangeRates import boards
# from exchangeRates import commands
# from exchangeRates import repository
# import telebot
#
# import config
#
# bot = telebot.TeleBot(config.settings["TOKEN"])
#
# rates = []
#
# try:
#     now = datetime.datetime.now()
#     url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={now.day}/0{now.month}/{now.year}"
#     http = urllib3.PoolManager()
#     response = http.request('GET', url)
#     data = xmltodict.parse(response.data)
#     repository.appendRate()
# except IOError as e:
#     print(e)
#
#
# def exchangeRates(bot):
#     bot.message_handler(func=lambda message: message.text in commands.rate)(printRate)
#
#
# def ratesMenu(message):
#     bot.send_message(message.chat.id, "Курсы валют", reply_markup=boards.mainBoard())
#
#
# @bot.message_handler(func=lambda message: message.text in commands.rate)
# def printRate(message):
#     if mainData.whereUser == mainData.sections["rates"]:
#         repository.appendRate()
#         if message.text == commands.rate[0]:
#             bot.send_message(message.chat.id, f"{rates[0]['Name']}: {rates[0]['Value']} 🇺🇸 ",
#                              reply_markup=boards.mainBoard())
#         elif message.text == commands.rate[1]:
#             bot.send_message(message.chat.id, f"{rates[1]['Name']}: {rates[1]['Value']} 🇪🇺",
#                              reply_markup=boards.mainBoard())
#         elif message.text == commands.rate[2]:
#             bot.send_message(message.chat.id, f"{rates[2]['Name']}: {rates[2]['Value']} 🇬🇧",
#                              reply_markup=boards.mainBoard())
#         elif message.text == commands.rate[3]:
#             bot.send_message(message.chat.id, f"{rates[3]['Name']}: {rates[3]['Value']} 🇨🇳",
#                              reply_markup=boards.mainBoard())
#         else:
#             bot.send_message(message.chat.id, "Чтоasdfa?)")
#     else:
#         bot.send_message(message.chat.id, "Что?)")
