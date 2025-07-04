import asyncio
from use import admin,user
from config import dp,bot

async def main():

    dp.include_routers(admin.router, user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())