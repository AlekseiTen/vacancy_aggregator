import requests


def hh_get_vacancies():  # pages - это кол-во стр пол-ых
    url = 'https://api.hh.ru/vacancies'

    page = 0
    all_vacancies = []

    while page < 100:
        params = {
            'text': '(python AND (разработчик OR developer)) OR (django OR flask OR fastapi)',
            'page': page,  # Номер страницы (с 0)
            'per_page': 20,
            'area': 2,  # Санкт-Петербург
            'schedule': 'remote',  # удалённая работа
            'search_field': 'name'
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            break

        data = response.json()
        vacancies = data.get("items", [])

        if not vacancies:
            break

        all_vacancies.extend(vacancies)
        page += 1

    return all_vacancies

