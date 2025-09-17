def hh_prepare_vacancies(raw_vacancies: list[dict]) -> list[dict]:
    """
    Преобразует сырые вакансии hh.ru в формат, подходящий для модели HH.
    """
    prepared = []
    for vac in raw_vacancies:
        prepared.append({
            "name": vac.get('name'),
            "employer": vac.get('employer', {}).get('name'),
            "url": vac.get('alternate_url')
        })
    return prepared


def sj_prepare_vacancies(raw_vacancies: list[dict]) -> list[dict]:
    """
    Преобразует сырые вакансии sj.ru в формат, подходящий для модели SJ.
    """
    prepared = []
    for vac in raw_vacancies:
        prepared.append({
            "name": vac.get('profession'),
            "employer": vac.get('firm_name'),
            "url": vac.get('link')
        })
    return prepared


def mts_prepare_vacancies(raw_vacancies: list[dict]) -> list[dict]:
    """
    Преобразует сырые вакансии mts.ru в формат, подходящий для модели mts.
    """
    prepared = []
    for vac in raw_vacancies:
        prepared.append({
            "name": vac.get('name'),
            "profession": vac.get('profession'),
            "url": vac.get('url')
        })
    return prepared
