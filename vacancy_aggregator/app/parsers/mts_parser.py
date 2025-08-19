import requests
from bs4 import BeautifulSoup


def mts_get_vacancies(url='https://mts.ai/ru/career/'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    vacancy_items = soup.find_all('div', class_='p-hr__vacancy-item')

    vacancies = []
    for vacancy in vacancy_items:
        # Название вакансии
        title_tag = vacancy.find('div', class_='p-hr__vacancy-title')
        name = title_tag.get_text(strip=True) if title_tag else 'Нет названия'

        # Профессия из атрибута data-profession
        profession = vacancy.get('data-profession', 'Нет данных о профессии')

        # Ссылка на вакансию — ищем тег <a> с классом hr_apply p-hr__vacancy-block_link
        apply_link_tag = vacancy.find('a', class_='hr_apply p-hr__vacancy-block_link')
        url = apply_link_tag['href'] if apply_link_tag and apply_link_tag.has_attr('href') else 'Нет ссылки'

        vacancies.append({
            'name': name,
            'profession': profession,
            'url': url
        })

    return vacancies
