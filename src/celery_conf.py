import asyncio

from celery import Celery

from src.admin.update_db import get_updater_db
from src.config import settings

celery_app = Celery('tasks', broker=settings.rabbit_url)
celery_app.conf.beat_schedule = {
    'update-db-from-excel': {
        'task': 'src.celery_conf.update_db',
        'schedule': settings.DB_UPDATE_PERIOD_IN_SECONDS,
    },
}


async def update_db_async():
    """Обновление базы."""
    db_updater = await get_updater_db()
    await db_updater.update_db_from_admin_data()


@celery_app.task
def update_db():
    """Задача на обновление базы каждое фиксированное время."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_db_async())
