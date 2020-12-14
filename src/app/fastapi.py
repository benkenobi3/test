import json
from fastapi import FastAPI, Depends, Form
from starlette.responses import Response

from tasks import count_ads
from common.net import get_region_id
from mongo import async_database, get_async_db
from mongo.models import Counter


app = FastAPI()


@app.on_event('startup')
def startup():
    async_database.connect_to_database()


@app.on_event('shutdown')
def shutdown():
    async_database.close_database_connection()


@app.post('/add', status_code=201)
async def add(phrase: str = Form(...), region: str = Form(...), db=Depends(get_async_db)) -> Response:
    """The method receives 'phrase' and 'region' as input, creates Counter and returns 'counter_id'

    Request body example
    {
      'phrase': 'string',
      'region': 'string'
    }

    Successful response example:
    {
      'counter_id': 'string'
    }
    """
    region_id: int = await get_region_id(region)
    if region_id:
        counter: Counter = await db.add_counter(
            Counter(phrase=phrase, region_id=region_id)
        )
        counter.id = str(counter.id)
        count_ads.send_with_options(args=[counter.dict()])
        res = json.dumps({'counter_id': counter.id})
        return Response(status_code=201, content=res, media_type='application/json')
    return Response(status_code=404, content='{ "msg": "Region not found" }')


@app.post('/stat')
async def stat(counter_id: str = Form(...), time_from: int = Form(...),
               time_to: int = Form(...), db=Depends(get_async_db)) -> Response:
    """The method receives 'counter_id' and two timestamp fields: 'time_from', 'time_to';
    and returns list of counter's results

    Request body example:
    {
      'counter_id': 'string',
      'time_from': 'int',
      'time_to': 'int'
    }

    Successful response example:
    [
      {
        'count': 'int',
        'timestamp': 'int'
      },
      ...
    ]
    """
    results = await db.get_results(counter_id=counter_id, time_from=time_from, time_to=time_to)
    if results:
        res = json.dumps(results)
        return Response(status_code=200, content=res, media_type='application/json')
    return Response(status_code=400, content='{ "msg: "No results with provided arguments" }')


@app.post('/stat/with_top')
async def top(counter_id: str = Form(...), time_from: int = Form(...),
              time_to: int = Form(...), db=Depends(get_async_db)) -> Response:
    """Does the same as '/stat' but adds additional field to response

    Successful response example:
    [
      {
        'count': 'int',
        'timestamp': 'int',
        'top_ads': 'string'
      },
      ...
    ]
    """
    results = await db.get_results(counter_id=counter_id, time_from=time_from, time_to=time_to, with_top=True)
    if results:
        res = json.dumps(results)
        return Response(status_code=200, content=res, media_type='application/json')
    return Response(status_code=400, content='{ "msg: "No results with provided arguments" }')
