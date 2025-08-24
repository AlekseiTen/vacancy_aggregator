from vacancy_aggregator.app.celery.celery_app import celery_app

if __name__ == '__main__':
    # Запускаем beat с автозагрузкой расписания
    celery_app.Beat().run()
