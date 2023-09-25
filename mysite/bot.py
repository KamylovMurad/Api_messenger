import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from config import TG_TOKEN, domain

bot = Bot(TG_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def on_start(message: types.Message):
    token = message.text
    api_url = f'http://{domain}/api/get_chat_id'
    response = requests.post(
        api_url,
        data={
            'token': token,
            'chat_id': message.from_user.id
        }
    )
    data = response.json()
    await message.answer(data['data'])


async def start_bot():
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f'[!!! Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())
