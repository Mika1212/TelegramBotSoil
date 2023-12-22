# TelegramBotSoil #
---
Телеграм-бот для определения содержания углерода в почве.

## Описание
---
Данный бот предназначен для гражданских ученых и фермеров. Этот бот позволяет определять содержание органического углерода в почве по фотографии, что позволяет делать первичную оценку плодородности почвы.

Данный репозиторий содержит исходный код бота и сервера, необходимых для работы. Этот проект разрабатывается в рамках обучения.

Release 1.0

---
## Структура проекта
---
- /src - тут находится исходный код бота и все необходимые для его работы файлы.
- /Python_Server - тут находится код сервера и дополнительных функций.
- /samples - тут находятся примеры фотографии для обработки ботом.
- /tests - тут находятся все тесты и доплонительные материалы для тестов.

## Запуск бота
---
1. Клонирование репозитория:

'''
 git clone (https://github.com/Mika1212/TelegramBotSoil)

 cd TelegramBotSoil
 '''
2. Установка зависимостей:
'''
 pip install -r requirements.txt
 '''
3. Запуск сервера:
'''
 python -m uvicorn src.Python_Server.FastApiServer:app 
'''
4. Запуск проекта:
'''
python main.py
'''

## Лицензия
---
Этот проект лицензирован в соответствии с условиями лицензии MIT — подробности см. в файле LICENSE.
