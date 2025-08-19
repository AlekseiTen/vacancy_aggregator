from vacancy_aggregator.app.core.tasks import send_unsent_hh_vacancies_task
from vacancy_aggregator.app.core.celery_app import celery_app

if __name__ == "__main__":
    print(f"Broker URL: {celery_app.conf.broker_url}")
    send_unsent_hh_vacancies_task.delay()
    print("Задача отправлена в очередь")
