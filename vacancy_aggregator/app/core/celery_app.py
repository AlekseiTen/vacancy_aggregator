from celery import Celery

celery_app = Celery(
    "vacancy_aggregator",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_app.conf.task_default_queue = "vacancy_aggregator_queue"
celery_app.conf.timezone = "Europe/Moscow"

# Импортируем tasks, чтобы зарегистрировать задачи
import vacancy_aggregator.app.core.tasks  # НЕ менять порядок! ИМПОРТ ПОСЛЕ создания celery_app