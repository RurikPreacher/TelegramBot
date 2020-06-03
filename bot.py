import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализировать бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # eсли он уже есть, то просто обновляем ему статус подписки
        db.update_subscrition(message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми!")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы и так подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscrition(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")

# тест таймера
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        now = datetime.utcnow()
        await bot.send_message(408312658, f"{now}", disable_notification=True)

# запускаем лонг поллинг
if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)