from vacancy_aggregator.app.core.celery_app import celery_app
import vacancy_aggregator.app.core.tasks

if __name__ == '__main__':
    # Передаем явно в argv команду worker и другие параметры
    celery_app.worker_main(argv=['worker', '--loglevel=info', '--pool=solo'])
