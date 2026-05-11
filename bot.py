import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup  # ← Правильный импорт!
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, Message
import asyncio
import urllib.request
import urllib.parse
import urllib.parse
import httpx
import urllib.parse

BOT_TOKEN = "8744811672:AAFtznWzIwrd69-sAPOJA6jXLQDwQypzOhs"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def parser(book_name: str):
    """Поиск книг через httpx (лучше работает с SSL)"""

    query = urllib.parse.quote(book_name)
    url = f"https://openlibrary.org/search.json?q={query}&limit=5"

    try:
        response = httpx.get(url, timeout=10, verify=False)  # verify=False отключает проверку SSL
        data = response.json()

        books = []
        for item in data.get('docs', []):
            title = item.get('title', 'Без названия')
            author = item.get('author_name', ['Неизвестен'])[0]
            year = item.get('first_publish_year', '')

            book_name = f"{title} — {author} ({year})" if year else f"{title} — {author}"
            books.append(Book(book_name, len(books)))

        return books if books else None

    except Exception as e:
        print(f"Ошибка: {e}")
        return None


# Правильный класс состояний
class States(StatesGroup):
    enter_name = State()  # Состояние ожидания названия книги
    # find - НЕ НУЖЕН как состояние, это будет результат поиска

class Book:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id


# def parser(name):
#     # Здесь должна быть реальная логика поиска
#     # Сейчас просто заглушка
#     if name.lower() == "война и мир": #поиск совпадений
#         mathes = [Book("Война и мир - Лев Толстой", 1),
#                 Book("Война миров - Герберт Уэллс", 2),
#                 Book("Три товарища - Эрих Ремарк", 3),
#                 Book("Мастер и Маргарита - Михаил Булгаков", 4)]
#         #Возврат результата: обязательно класс Book(имя, айди)
#         return mathes
#     return None

def get_inline_keyboard(books_list):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=book.name, callback_data=f"book_{book.id}")]
        for book in books_list]
    )
    return keyboard


def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🆘 Помощь")],
            [KeyboardButton(text="🔍 Поиск книги"), KeyboardButton(text="🔍 Поиск манги")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_find_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text = "Назад")]
        ],
        resize_keyboard=True
    )
    return keyboard


@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"Привет, {user_name}! 👋\n\n"
        f"Выбери действие с помощью кнопок внизу экрана:",
        reply_markup=get_main_keyboard()
    )


# Обработка кнопки "Поиск книги"
@dp.message(lambda message: message.text == "🔍 Поиск книги")
async def search_book(message: types.Message, state: FSMContext):
    await state.set_state(States.enter_name)
    await message.answer("Введите книгу, которую хотите найти", reply_markup=get_find_keyboard())


# Обработка ввода названия книги
@dp.message(States.enter_name)
async def process_name(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await state.clear()
        await message.answer(text = 'Вы попали в главное меню', reply_markup=get_main_keyboard())
    else:
        found_books = parser(message.text)

        if found_books:  # Если книги найдены
            await message.answer(f"Результат поиска по запросу '{message.text}'",
                                 reply_markup = get_inline_keyboard(found_books))
            await state.clear()
        else:
            await message.answer(f"По запросу '{message.text}' ничего не найдено, проверьте правильность"
                                 f" написанного текста или введите полное название")




@dp.message(lambda message: message.text == "👤 Профиль")
async def profile(message: types.Message):
    await message.answer("👤 Ваш профиль:\nИмя: {}\nID: {}".format(
        message.from_user.first_name, message.from_user.id
    ))


@dp.message(lambda message: message.text == "🆘 Помощь")
async def help_button(message: types.Message):
    await message.answer("❓ Напишите /start чтобы увидеть меню\nИли задайте вопрос @TOmiokaqqq.")


@dp.message(lambda message: message.text == "🔍 Поиск манги")
async def search_book(message: types.Message, state: FSMContext):
    await state.set_state(States.enter_name)
    await message.answer("Введите название манги, которую хотите найти", reply_markup=get_find_keyboard())


@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "agree":
        await callback.message.answer("😊 Спасибо! Рады что вам нравится!")
        await callback.answer()
    elif callback.data == "disagree":
        await callback.message.answer("😔 Жаль! Что можно улучшить? Напишите в поддержку.")
        await callback.answer()
    else:
        await callback.answer("Неизвестная команда", show_alert=True)


@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}\n\nИспользуй /start для меню или нажми кнопку 🆘 Помощь.")


async def main():
    print("Бот запущен...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
