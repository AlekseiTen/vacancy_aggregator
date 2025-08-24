import asyncio

from vacancy_aggregator.app.db.models import AsyncSessionLocal, HH, SJ, MTS
from vacancy_aggregator.app.parsers.hh_vacancies import hh_get_vacancies
from vacancy_aggregator.app.parsers.mts_parser import mts_get_vacancies
from vacancy_aggregator.app.parsers.super_job_vacancies import sj_get_vacancies
from vacancy_aggregator.app.schemas.prepare_functions import hh_prepare_vacancies, sj_prepare_vacancies, \
    mts_prepare_vacancies
from vacancy_aggregator.app.schemas.vacancy_saver import save_vacancy


async def main():
    # hh
    raw_hh = hh_get_vacancies()
    prepared_hh = hh_prepare_vacancies(raw_hh)

    # SJ
    raw_sj = sj_get_vacancies()
    prepared_sj = sj_prepare_vacancies(raw_sj)

    # MTS
    raw_mts = mts_get_vacancies()
    prepared_mts = mts_prepare_vacancies(raw_mts)

    async with AsyncSessionLocal() as session:
        await save_vacancy(prepared_hh, HH, session)
        await save_vacancy(prepared_sj, SJ, session)
        await save_vacancy(prepared_mts, MTS, session)


if __name__ == "__main__":
    asyncio.run(main())
