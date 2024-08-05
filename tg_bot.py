

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline
from main import check_news_update
from API import TOKEN_API, ID_CHENNEL

bot = Bot(TOKEN_API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
@dp.message_handler(commands="/start")

async def news_every_minute():
    while True:
        fresh_news = check_news_update()
        if fresh_news is None:
            await asyncio.sleep(1800)

            continue
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news =  f"{hbold(v['article_name'])} \n" \
                        f"{(v['article_text'])} \n" \
                        f"{hunderline(v['card_url'])}"



                await bot.send_message(ID_CHENNEL, news)
            else:

                await asyncio.sleep(1800)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
