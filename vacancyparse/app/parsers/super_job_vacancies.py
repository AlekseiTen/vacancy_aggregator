import os
import requests
from dotenv import load_dotenv

load_dotenv()  # чтобы подгрузить .env, если запускаете локально

API_URL = "https://api.superjob.ru/2.0/vacancies/"
API_KEY = os.getenv("SUPERJOB_API_KEY")  # ключ в переменной окружения

def sj_get_vacancies():
    if not API_KEY:
        raise ValueError("Не найден ключ SUPERJOB_API_KEY в переменных окружения")

    headers = {"X-Api-App-Id": API_KEY}

    page = 0
    all_vacancies = []

    while True:
        params = {
            "keywords[0][srws]": 10,
            "keywords[0][skwc]": "and",
            "keywords[0][keys]": "python",
            "page": page,
            "count": 20,  # макс 100
            "town": "Санкт-Петербург",
        }

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        vacancies = data.get("objects", [])

        if not vacancies:
            break

        all_vacancies.extend(vacancies)
        page += 1

    return all_vacancies
