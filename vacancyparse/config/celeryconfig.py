import os
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()  # загрузка переменных окружения из .env

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
task_default_queue = "vacancy_aggregator_queue"
timezone = "Europe/Moscow"
enable_utc = True

# Явно указываем куда сохранять файл расписания
beat_schedule_filename = os.getenv("CELERY_BEAT_SCHEDULE", "/celery_data/celerybeat-schedule")
beat_scheduler = "celery.beat.PersistentScheduler"

beat_schedule = {
    'parse-twice-daily': {
        'task': 'vacancyparse.app.celery.tasks.daily_parse_and_save_vacancies',
        'schedule': crontab(minute=0, hour='9,21'),
    },
    'send-twice-daily-after-parse': {
        'task': 'vacancyparse.app.celery.tasks.send_unsent_hh_vacancies_task',
        'schedule': crontab(minute=30, hour='9,21'),
    },
}
