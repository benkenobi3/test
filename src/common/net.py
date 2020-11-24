import ssl
import json
from httpx import Client
from httpcore import SyncConnectionPool


ssl_context = ssl.create_default_context()
ssl_context.options |= ssl.OP_NO_TLSv1_2

transport = SyncConnectionPool(
    ssl_context=ssl_context,
    max_connections=100,
    max_keepalive_connections=20,
    keepalive_expiry=5.0,
    local_address="0.0.0.0",
)


sync_http = Client(transport=transport)


def get_region_id(region: str) -> int:
    url = 'https://m.avito.ru/api/1/slocations?limit=1&q={region}' \
        '&key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'.format(region=region)
    response = sync_http.get(url)
    print(response.json())
    locations = response.json()['result']['locations']
    if locations:
        region_id: int = locations[0]['id']
        return region_id


def get_page(phrase: str, region_id: int) -> (int, str):
    api_url = 'https://m.avito.ru/api/9/items?locationId={location}&query={phrase}&page=1&display=list&limit=5' \
              '&key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'.format(location=region_id, phrase=phrase)
    response = sync_http.get(api_url)
    count: int = response.json()['result']['mainCount']
    if count:
        top_ads: str = json.dumps(response.json()['result']['items'])
        return count, top_ads
    return 0, 'Not found'
