import json
from fastapi import FastAPI, Form
from starlette.responses import Response

from tasks import count_ads
from app.settings import DELAY
from common.net import get_region_id
from mongo.models import Counter
from mongo.async_database import add_counter, get_results


app = FastAPI()


@app.post('/add', status_code=201)
async def add(phrase: str = Form(...), region: str = Form(...)) -> Response:
    region_id: int = get_region_id(region)
    if region_id:
        counter: Counter = await add_counter(
            Counter(phrase=phrase, region_id=region_id)
        )
        counter.id = str(counter.id)
        count_ads.send_with_options(args=[counter.dict()], delay=DELAY)
        res = json.dumps({'id': counter.id})
        return Response(status_code=201, content=res, media_type='application/json')
    return Response(status_code=400, content='Region not found')


@app.post('/stat')
async def stat(counter_id: str = Form(...), time_from: int = Form(...), time_to: int = Form(...)) -> Response:
    results = await get_results(counter_id=counter_id, time_from=time_from, time_to=time_to)
    if results:
        res = json.dumps(results)
        return Response(status_code=200, content=res, media_type='application/json')
    return Response(status_code=404, content='No one result with provided arguments')


@app.post('/stat/with_top')
async def top(counter_id: str = Form(...), time_from: int = Form(...), time_to: int = Form(...)) -> Response:
    results = await get_results(counter_id=counter_id, time_from=time_from, time_to=time_to, with_top=True)
    if results:
        res = json.dumps(results)
        return Response(status_code=200, content=res, media_type='application/json')
    return Response(status_code=404, content='No one result with provided arguments')
