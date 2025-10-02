import requests

API_URL = 'https://api.hh.ru/vacancies'
MAX_PAGES = 100
PER_PAGE = 20

SEARCH_TEXT = 'python'
AREA = 2  # Санкт-Петербург
SEARCH_FIELD = 'name'


def hh_get_vacancies():
    page = 0
    all_vacancies = []

    while page < MAX_PAGES:
        params = {
            'text': SEARCH_TEXT,
            'search_field': SEARCH_FIELD,
            'area': AREA,
            'per_page': PER_PAGE,
            'page': page,
        }

        response = requests.get(API_URL, params=params)
        if response.status_code != 200:
            break

        data = response.json()
        vacancies = data.get("items", [])
        if not vacancies:
            break

        all_vacancies.extend(vacancies)
        page += 1

    return all_vacancies
