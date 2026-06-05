# 📚 Mangareado

Telegram бот для поиска и скачивания книг с Coollib.net и манги с Remanga.org.

## 🚀 Возможности

- 🔍 Поиск книг на Coollib.net
- 📥 Скачивание книг в форматах FB2 и PDF
- 🔍 Поиск манги на Remanga.org
- 📖 Просмотр глав по номерам или томам
- 📥 Скачивание отдельных глав или целых томов в PDF
- 🗜️ Автоматическое сжатие больших PDF файлов

## 📋 Требования

- Python 3.9 или выше
- Токен Telegram бота (получить у [@BotFather](https://t.me/BotFather))

## 🛠️ Полная установка (все в одном)

```bash
# 1. Создайте папку проекта и перейдите в нее
mkdir tg-book-manga-bot && cd tg-book-manga-bot

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте окружение
# Windows:
venv\Scripts\activate
# Linux/MacOS:
source venv/bin/activate

# 4. Создайте файл requirements.txt и установите зависимости
echo "aiogram>=3.0.0
aiohttp>=3.9.0
httpx>=0.25.0
aiofiles>=23.0.0
img2pdf>=0.4.0
Pillow>=10.0.0
beautifulsoup4>=4.12.0
lxml>=4.9.0" > requirements.txt

pip install -r requirements.txt

# 5. Создайте файл bot.py (скопируйте код ниже)

# 6. Замените токен в bot.py на свой от @BotFather

# 7. Запустите бота
python bot.py
