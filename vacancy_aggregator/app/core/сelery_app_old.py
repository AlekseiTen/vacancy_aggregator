# from celery import Celery
# from celery.schedules import crontab
#
# celery_app = Celery(
#     "vacancy_aggregator",
#     broker="redis://localhost:6379/0",
#     backend="redis://localhost:6379/0",
# )
#
# celery_app.conf.timezone = "Europe/Moscow"
# celery_app.conf.task_default_queue = "vacancy_aggregator_queue"
# celery_app.conf.beat_schedule = {
#     "parse-site-hh-every-minute": {  # изменил на "every-minute" для теста
#         "task": "vacancy_aggregator.app.core.tasks.hh_get_vacancies_task",
#         "schedule": crontab(minute="*"),  # каждая минута
#         "options": {"queue": "vacancy_aggregator_queue"},
#     },
#     # "parse-site-sj-every-minute": {
#     #     "task": "vacancy_aggregator.app.core.tasks.sj_get_vacancies_task",
#     #     "schedule": crontab(minute="*"),
#     #     "options": {"queue": "vacancy_aggregator_queue"},
#     # },
# }
#
# # Импортируем tasks, чтобы зарегистрировать задачи
# import vacancy_aggregator.app.core.tasks  # НЕ менять порядок! ИМПОРТ ПОСЛЕ создания celery_app