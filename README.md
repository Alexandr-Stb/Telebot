# The Croupier bot

# Для запуска бота, вам нужно:
### Открыть проект в PyCharm, затем выбрать конфигурацию и указать в Script path - "Telebot/CroupierBot.py", запустить конфигурацию CroupierBot.py.
### Найти бота по ссылке: https://t.me/PartyBotbot
### Запустить командой /start

---


The Croupier bot - это игровой бот, в котором реализована 
механика карточной игры BlackJack с разными вариациями(ставки, замена карт, автосумма очков).

Бот построен по следующей иерархии:

* Игра Blakjack
  * Раздача карт и ставка (если включена)
  * Механика самой игры
  * Выход или продолжение игры
* Настройка игры
  * Настройка ставкок, автосуммы, карт и пополнение баланса
  * В каждой вкладке есть выбор между кнопкой "включить" или "выключить"

---

### Изначально бот предалагает на выбор три действия:

![Screen_1](https://user-images.githubusercontent.com/98232785/210860314-b9e9df8d-0b08-4375-b82c-bfed0de2288c.png)


* *Настройки - Переход на страницу настроек игры
* О боте - Краткая информация о боте
* Blackjack - Запуск игры

---

## Игра Blackjack

При запуске игры активируется скрипт который выдает игроку случайную карту:

```python
for i in range(2):      #бот раздает две карты себе и игроку
    giveRandomCard(bjData.userCard, bjData.botCard)     #записывает карту в объект игрока и сравнивает со своим
    giveRandomCard(bjData.botCard, bjData.userCard)     #записывает карту в свой объект и сравнивает с игроком
                                                        #сравнение нужно для проверки дубликатов
```

![Screen_2](https://user-images.githubusercontent.com/98232785/210860489-042aaa59-6c0f-4544-8bd7-5d64118d1d43.png)

---
Дальше есть вариация ходов:

### Выход

При нажатии на кнопку выхода, запускается скрипт, который чистит все данные о последних играх.
Если игра была со ставками, то бот проверяет, когда вышел игрок: в процессе или по окончании игры.
Это нужно для того, чтобы баланс игрока не менялся, если он вышел до окончания игры.


```python
@bot.message_handler(func=lambda message: message.text == commands.exitGame)  #слушатель кнопки выход
def leaveGame(message): 
    if mainData.whereUser == mainData.sections["bj"]:               #проверка того, что игрок находится в игре
        if bjData.gameRate != 0:                                    #Если ставка есть
            bjData.balance = bjData.balance + bjData.gameRate       #Мы к балансу прибавляем цену ставки
            bjData.gameRate = 0                                     #Обнуляем цену игровой ставки
        repository.quitOrRebootGame(True)                           #Очищаем данные прошлой игры
        mainRepository.goMenu(message)                              #Возвращаем игрока в меню
```
---

### Больше

При нажатии добавляем игроку одну карту и проверяем количество очков:

```python
if bjData.userCard.sum < 21:                                   #если сумма меньше 21
    bot.send_message(message.chat.id, "Держи")                 #пишем сообщение
    repository.giveRandomCard(bjData.userCard, bjData.botCard) #выдаем рандомную карту
    messages.printMesUserCard(message)                         #показываем игроку карты

if bjData.userCard.sum == 21:                                  #если сумма равна 21
    messages.printWonOrLoseMes(message, True)                  #пишем сообщениие о победе
    bjData.startGame = False                                   #заканчиваем скрипт игры

elif bjData.userCard.sum > 21:                                 #если сумма больше 21
    if repository.checkAce(bjData.userCard):                   #проверям, есть ли туз в колоде игрока
        messages.printDownAceMessage(message, "USER")          #если есть, заменяем значение туза с 11 на 1
    else:                                                      #если туза нету
        messages.printWonOrLoseMes(message, False)             #пишем сообщение о проирыше
        bjData.startGame = False                               #заканчиваем скрипт игры
```

![Screeen_3](https://user-images.githubusercontent.com/98232785/210969754-c1833016-2e4c-4782-a0dc-983786efd8f5.png)

---

### Пас

При нажатии на кнопку, игрок покидает игру и бот выводит сообщение со своими картами. Меню заменяется.  

Далее бот добавляет себе по одной карте до выйгрыша, проигрыша или ничьи.  

![Screen_3](https://user-images.githubusercontent.com/98232785/210969266-5a11918d-fb19-41fe-93e1-5636d8776aaa.png)
![Screen_4](https://user-images.githubusercontent.com/98232785/210976295-ab7c4d21-dfc7-4e69-bb19-aabf924f0943.png)

---

### Заново

При нажатии на кнопку скрипт игры перезапускается, ставки обнуляются(если они включены в настройках).

```python
if bjData.gameRate != 0:                                #если была ставка
    bjData.balance = bjData.balance + bjData.gameRate   #добавляем игроку на счет, прошлую ставку
    bjData.gameRate = 0                                 #обнуляем ставку
bot.send_message(message.chat.id, "Ну давай повторим")  #отправляем сообщение
repository.quitOrRebootGame(False)                      #перезапускаем скрипт игры
startGame(message)                                      #запускаем скрипт игры
```
![Screen_5](https://user-images.githubusercontent.com/98232785/210978635-2aea717e-c65d-40b1-90aa-5a3a955a3825.png)

---

### Игра со ставками

Игра со ставками почти не отличается от игры без ставок, просто  скрипт заполняет поле со ставкой, 
и в конце игры переписывает значение баланса игрока и баланс ставки. Также  при перезапуске игры
(если она не была закончена) ставка возвращается на баланс игрока, а игровая ставка обнуляется.

---

### Настройки

В настройках есть четыре поля:
* Автосумма очков
* Ставки
* Пополнение баланса
* Карты

Также при переходе в поле настроек, бот выводит сообщение о состоянии всех настроек. 

![image](https://user-images.githubusercontent.com/98232785/210983739-c0e2cbaf-4507-452b-bf66-76d42b543c06.png)  

При нажатии на любое поле, бот спросит что именно сделать с определенной настройкой.

![image](https://user-images.githubusercontent.com/98232785/210985085-9284dbb4-a35f-4758-8cde-0ed8ab44549b.png)
![image](https://user-images.githubusercontent.com/98232785/210985330-566029f5-c08d-4bed-ae3d-ba047796886d.png)

При изменении настроек, меняется поле настройки в файле [bjData](https://github.com/Alexandr-Stb/Telebot/blob/master/blackJack/bjData.py)
Это основной файл данных, связанных с игрой.

---

### Остальное

При переключении настроек карт, бот будет присылать карты не текстом, а картинками.  

![image](https://user-images.githubusercontent.com/98232785/210990711-438b08fc-98dd-4c61-a3a6-7758c5e244bd.png)
![image](https://user-images.githubusercontent.com/98232785/210992022-0482a7be-4711-4f99-8b92-4452000ef91d.png)

При отключении автосуммы, она не будет выводится ботом.

![image](https://user-images.githubusercontent.com/98232785/210993014-b392ccab-6e46-4f59-bee6-6299d54f7edd.png)
![image](https://user-images.githubusercontent.com/98232785/210992830-749670c8-18b7-4134-a26c-50819362a881.png)

