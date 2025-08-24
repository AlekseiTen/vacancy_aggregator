from celery import Celery

celery_app = Celery(
    "vacancy_aggregator",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.task_default_queue = "vacancy_aggregator_queue"
celery_app.conf.timezone = "Europe/Moscow"

# Настройка расписания
celery_app.conf.beat_schedule = {
    'send-unsent-vacancies-every-minute': {
        'task': 'vacancy_aggregator.app.celery.tasks.send_unsent_hh_vacancies_task',
        'schedule': 60.0,  # через 60 секунд, т.е. каждую минуту
    },
}

# Импортируем tasks, чтобы зарегистрировать задачи
import vacancy_aggregator.app.celery.tasks  # НЕ менять порядок! ИМПОРТ ПОСЛЕ создания celery_app