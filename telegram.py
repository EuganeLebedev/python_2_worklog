from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
import os
import logging
from jira import get_open_issues_list, create_worklog
import asyncio

API_TOKEN = os.getenv("TB_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

def auth(func):

    async def wrapper(message):
        if message.from_user.id != 192151684:
            return await message.reply("Access denied", reply=False)
        return await func(message)
    
    return wrapper



@dp.message_handler(commands=['start'])
@auth
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    start_buttons = ['Открытые задачи', 'Еще что-то',]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    
    await message.answer('Выберите категорию', reply_markup=keyboard)



@dp.message_handler(Text(equals='Открытые задачи'))
@auth
async def get_discount_knives(message: types.Message):
    await message.answer('Please waiting...')
    
    issue_list_responce = get_open_issues_list()
    # for issue in issue_list_responce.json().get("issues"):
    #     print(issue['key'])
    
    for index, issue in enumerate(issue_list_responce.json().get("issues")):
        inline_btn = InlineKeyboardButton(f'Отметить время', callback_data="create_worklog" + issue.get("key"))
        inline_kbd = InlineKeyboardMarkup().add(inline_btn)
        card = f'{hbold(issue.get("key"))}\n{issue.get("fields").get("summary")}'
    
    
        if index%20 == 0:
            asyncio.sleep(3)
            
        await message.answer(card, reply_markup=inline_kbd)

@dp.callback_query_handler(lambda c: c.data.startswith('create_worklog'))
async def process_callback_button(callback_query: types.CallbackQuery):
    issue_id = callback_query.data[14:]
    await bot.answer_callback_query(callback_query.id)
    worklog = create_worklog(message='I did some work here.', duration=60, issue_id=issue_id)
    if worklog.status_code == 200:
        await bot.send_message(callback_query.from_user.id, f'Готово!')
    else:
        await bot.send_message(callback_query.from_user.id, f'{worklog.text}')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)