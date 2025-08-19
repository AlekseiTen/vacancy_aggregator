import requests


def sj_get_vacancies():  # pages - это кол-во стр пол-ых
    url = "https://api.superjob.ru/2.0/vacancies/"
    api_key = "v3.r.139144767.0b36ec9481d5b6b56f4cffc0c45ad1e331eb132d.32c4f25683e5851c2f19963bcef69b64fcdd0aac"

    headers = {"X-Api-App-Id": api_key}  # Обязательный заголовок

    page = 0
    all_vacancies = []

    while True:
        params = {
            "keywords[0][srws]": 10,
            "keywords[0][skwc]": "and",
            "keywords[0][keys]": "python",
            "page": page,
            "count": 20,  # количество вакансий на странице (максимум 100)
            "town": "Санкт-Петербург",
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        vacancies = data.get("objects", [])

        if not vacancies:
            break

        all_vacancies.extend(vacancies)
        page += 1

    return all_vacancies
