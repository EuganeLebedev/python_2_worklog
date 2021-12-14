from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text
import os
import logging
from jira import get_open_issues_list, create_worklog, get_typical_issues_list
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import get_registred_users_id

API_TOKEN = os.getenv("TB_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


class CreateWorklog(StatesGroup):
    waiting_for_spend_time = State()
    waiting_for_comment = State()


def auth(func):

    async def wrapper(message, *args, **kwargs):
        if message.from_user.id not in get_registred_users_id():
            print(f"{message.from_user.id=}")
            return await message.answer("Access denied")
        return await func(message, *args, **kwargs)
    return wrapper


@dp.message_handler(commands=['start'])
@auth
async def send_welcome(message: types.Message, *args, **kwargs):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    start_buttons = ['Открытые задачи', 'Типовые задачи', ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Выберите категорию', reply_markup=keyboard)


@dp.message_handler(Text(equals='Открытые задачи'))
@auth
async def get_open_issues(message: types.Message, *args, **kwargs):
    await message.answer('Please waiting...')

    issue_list_responce = get_open_issues_list(user_id=message.from_user.id)

    for index, issue in enumerate(issue_list_responce.json().get("issues")):
        inline_btn = InlineKeyboardButton(
            f'Отметить время', callback_data="create_worklog" + issue.get("key"))
        inline_kbd = InlineKeyboardMarkup().add(inline_btn)
        card = f'{hbold(issue.get("key"))}\n{issue.get("fields").get("summary")}'

        if index % 20 == 0:
            asyncio.sleep(3)

        await message.answer(card, reply_markup=inline_kbd)


@dp.message_handler(Text(equals='Типовые задачи'))
@auth
async def get_typical_issues(message: types.Message, *args, **kwargs):
    await message.answer('Please waiting...')

    issue_list_responce = get_typical_issues_list(user_id=message.from_user.id)

    for index, issue in enumerate(issue_list_responce.json().get("issues")):
        inline_btn = InlineKeyboardButton(
            f'Отметить время', callback_data="create_worklog" + issue.get("key"))
        inline_kbd = InlineKeyboardMarkup().add(inline_btn)
        card = f'{hbold(issue.get("key"))}\n{issue.get("fields").get("summary")}'

        if index % 20 == 0:
            asyncio.sleep(3)

        await message.answer(card, reply_markup=inline_kbd)


@dp.callback_query_handler(lambda c: c.data.startswith('create_worklog'))
@auth
async def create_worklog_start(callback_query: types.CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.update_data(issue_id=callback_query.data[14:])
    await callback_query.message.answer(f"TASK {callback_query.data[14:]}:")
    await callback_query.message.answer("Сколько часов было затрачено?:")
    await CreateWorklog.waiting_for_spend_time.set()


@dp.message_handler(state=CreateWorklog.waiting_for_spend_time)
@auth
async def spend_time_chosen(message: types.Message, state: FSMContext, *args, **kwargs):

    try:
        spend_time = int(float(message.text)*60*60)
    except ValueError as e:
        await message.answer("Пожалуйста, введите число")
        return

    if spend_time < 0:
        await message.answer("Пожалуйста, введите значение больше нуля")
        return

    await state.update_data(spend_time=spend_time)

    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await CreateWorklog.waiting_for_comment.set()
    await message.answer("Что было сделано?")


@dp.message_handler(state=CreateWorklog.waiting_for_comment)
@auth
async def worklog_comment_chosen(message: types.Message, state: FSMContext, *args, **kwargs):

    if not message.text:
        await message.answer("Пожалуйста, укажите что было сделано.")
        return

    await state.update_data(comment=message.text)
    user_data = await state.get_data()

    worklog = create_worklog(comment=user_data.get("comment"),
                             duration=user_data.get("spend_time"), issue_id=user_data.get("issue_id"), user_id=message.from_user.id)
    if worklog.json().get("errorMessage"):
        await message.answer(f"{worklog.json().get('errorMessages')}\n{worklog.json().get('errors')}")
    elif worklog.status_code in [200, 201, 202]:
        await message.answer(f"Готово!")
    else:
        await message.answer(f"{worklog.status_code} {worklog.text}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
