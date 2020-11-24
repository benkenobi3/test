import os


# Tasks
DELAY: int = 1000 * 60 * 5
DELAY: int = int(os.environ.get('DELAY', DELAY))


# Uvicorn settings
# Uvicorn https://www.uvicorn.org/
PORT: int = int(os.environ.get('PORT', '80'))
LOG_LEVEL: str = 'debug'


# Database
# MongoDB https://www.mongodb.com/
DATABASE = {
    'NAME': os.environ.get('DB_NAME', 'SeriesDB'),
    'HOST': os.environ.get('DB_HOST', 'localhost'),
    'PORT': int(os.environ.get('DB_PORT', '27017')),
}


# Redis as broker
# Redis https://redis.io/
REDIS = {
    'HOST': os.environ.get('REDIS_HOST', 'localhost'),
    'PORT': os.environ.get('REDIS_PORT', '6379')
}
