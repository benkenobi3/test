import dramatiq
from datetime import datetime
from dramatiq.brokers.redis import RedisBroker

from app.settings import REDIS, DELAY
from common.net import get_page
from mongo.sync_database import add_result, has_counter
from mongo.models import Result, Counter


dramatiq.set_broker(RedisBroker(host=REDIS['HOST'], port=REDIS['PORT']))


@dramatiq.actor(actor_name='count_ads', max_retries=3)
def count_ads(counter: dict):
    count, top_ads = get_page(counter['phrase'], counter['region_id'])
    result_id: str = add_result(
        Result(
            counter_id=str(counter['id']),
            count=count,
            top_ads=top_ads,
            timestamp=int(datetime.now().timestamp())
        )
    )
    print('counter_id: {}, result_id: {}, count: {}'.format(str(counter['id']), result_id, count))
    counter_still_exist = has_counter(counter['id'])
    if counter_still_exist:
        count_ads.send_with_options(args=(counter,), delay=DELAY)
