import ssl
import json
from httpx import Client, AsyncClient
from httpcore import SyncConnectionPool, AsyncConnectionPool


ssl_context = ssl.create_default_context()
ssl_context.options |= ssl.OP_NO_TLSv1_2


kwargs = {
    'ssl_context': ssl_context,
    'max_connections': 100,
    'max_keepalive_connections': 20,
    'keepalive_expiry': 5.0,
    'local_address': '0.0.0.0'
}


sync_http = Client(transport=SyncConnectionPool(**kwargs))
async_http = AsyncClient(transport=AsyncConnectionPool(**kwargs))


API_KEY = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
TOP_ADS_LIMIT = 5


async def get_region_id(region: str) -> int:
    url = f'https://m.avito.ru/api/1/slocations?limit=1&q={region}&key={API_KEY}'
    response = await async_http.get(url)
    locations = response.json()['result']['locations']
    if locations:
        region_id: int = locations[0]['id']
        return region_id


def get_page(phrase: str, region_id: int) -> (int, str):
    api_url = f'https://m.avito.ru/api/9/items?locationId={region_id}&query={phrase}&page=1&display=list' \
              f'&limit={TOP_ADS_LIMIT}&key={API_KEY}'
    response = sync_http.get(api_url)
    count: int = response.json()['result']['mainCount']
    if count:
        top_ads: str = json.dumps(response.json()['result']['items'])
        return count, top_ads
    return 0, 'Not found'
