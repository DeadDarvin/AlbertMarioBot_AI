# AlbertMarioBot_AI
Test task from MindFusion. Bot for talking with Mario or Albert Einstein persons. Uses GPT-3.5

## [Бот здесь](https://t.me/AlbertMarioBot)

# Техническое задание:

### 1. /start (Стартовое сообщение):
1. Отправляем событие регистрации пользователя ***(Amplitude)***
2. Сохраняем пользователя в БД (user_id, username, name, surname, time)
3. Отправляем приветственное сообщение с объяснением функционала и кнопкой на WebApp для выбора персонажа

### 2. WebApp (Выбор персонажа):
1. Отправляем событие о выборе персонажа ***(Amplitude)***
2. Сохраняем персонажа пользователя в БД (Может, Mongo подсоединить)
3. Закрываем WebApp
4. Отправляем сообщение персонажа из БД

### 3. Message Reaction (Сообщение от пользователя):
1. Сохраняем сообщение в БД
2. Отправляем событие о запросе пользователя ***(Amplitude)***
3. Отправляем запрос в OpenAI с сообщением пользователя в промте
4. Отправляем событие об ответе OpenAI на запрос пользователя ***(Amplitude)***
5. Отправляем сообщение пользователю
6. Сохраняем ответ от OpenAI рядом с сообщением в БД
7. Отправляем событие об ответе на сообщение пользователя ***(Amplitude)***

### 4. /menu:
1. Отправляем кнопку для перевыбора персонажа (на WebApp)


## Идеи:
1. Прикрутить redis {"user_id": "person"} для оптимизации
