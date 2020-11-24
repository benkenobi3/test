## Test task in the Market Intelligence unit

### Quick start:
    $ docker-compose up

### Api methods:

#### /add
The method receives 'phrase' and 'region' fields as input, creates Counter and returns 'counter_id'

##### Request body example:
    {
      'phrase': 'string',
      'region': 'string'
    }

##### Successful response example:
    {
      'counter_id': 'string'
    }

##### Validation Error:
    {
      "detail": [
        {
          "loc": [
            "string"
          ],
          "msg": "string",
          "type": "string"
        }
      ]
    }

##### Not found error:
    {
      "msg": "Region not found"
    }


#### /stat
The method receives 'counter_id' and two timestamp fields: 'time_from', 'time_to'; and returns list of counter's results

##### Request body example:
    {
      'counter_id': 'string',
      'time_from': 'int',
      'time_to': 'int'
    }

##### Successful response example:
    [
      {
        'count': 'int',
        'timestamp': 'int'
      },
      ...
    ]

##### Validation Error:
    {
      "detail": [
        {
          "loc": [
            "string"
          ],
          "msg": "string",
          "type": "string"
        }
      ]
    }

##### Not found error:
    {
      "msg": "No results with provided arguments"
    }

#### /stat/with_top
Does the same as '/stat' but adds additional field to response

##### Successful response example:
    [
      {
        'count': 'int',
        'timestamp': 'int',
        'top_ads': 'string'
      },
      ...
    ]
