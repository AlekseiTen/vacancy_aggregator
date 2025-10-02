import nest_asyncio
import asyncio
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()
# запуск тг бота

from vacancyparse.app.bot.tg_bot import main

if __name__ == "__main__":
    asyncio.run(main())
