from celery import Celery
from vacancyparse.config import celeryconfig

celery_app = Celery("vacancyparse")
celery_app.config_from_object(celeryconfig)

import vacancyparse.app.celery.tasks  # импорт задач для регистрации
