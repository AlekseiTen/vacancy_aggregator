import asyncio
from vacancyparse.app.db.database import init_models
from dotenv import load_dotenv

load_dotenv()  # для загрузки настроек из .env

if __name__ == "__main__":
    asyncio.run(init_models())
