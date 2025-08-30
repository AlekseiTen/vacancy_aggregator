from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "vacancy_aggregator",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.task_default_queue = "vacancy_aggregator_queue"
celery_app.conf.timezone = "Europe/Moscow"
celery_app.conf.enable_utc = True

# Настройка расписания
celery_app.conf.beat_schedule = {
    'parse-twice-daily': {
        'task': 'vacancy_aggregator.app.celery.tasks.daily_parse_and_save_vacancies',
        'schedule': crontab(minute=0, hour='9,21'),  # запускать в 9:00 и 21:00 по Москве
    },
    'send-twice-daily-after-parse': {
        'task': 'vacancy_aggregator.app.celery.tasks.send_unsent_hh_vacancies_task',
        'schedule': crontab(minute=30, hour='9,21'),  # через 30 минут после парсинга
    },
}

# Импортируем tasks, чтобы зарегистрировать задачи
import vacancy_aggregator.app.celery.tasks  # НЕ менять порядок! ИМПОРТ ПОСЛЕ создания celery_app
