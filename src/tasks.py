import logging
import dramatiq
from datetime import datetime
from dramatiq.brokers.redis import RedisBroker

from app.settings import REDIS, DELAY
from common.net import get_page
from mongo import sync_db, get_sync_db
from mongo.models import Result, Counter


dramatiq.set_broker(RedisBroker(host=REDIS['HOST'], port=REDIS['PORT']))

sync_db.connect_to_database()
database = get_sync_db()

logger = logging.getLogger()


@dramatiq.actor(actor_name='count_ads', max_retries=3)
def count_ads(counter: dict):
    counter_still_exist = database.has_counter(counter['id'])
    if counter_still_exist:
        count, top_ads = get_page(counter['phrase'], counter['region_id'])
        result_id: str = database.add_result(
            Result(
                counter_id=str(counter['id']),
                count=count,
                top_ads=top_ads,
                timestamp=int(datetime.now().timestamp())
            )
        )
        logger.info(f'counter_id: {str(counter["id"])}, result_id: {result_id}, count: {count}')
        count_ads.send_with_options(args=(counter,), delay=DELAY)
