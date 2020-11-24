import uvicorn
from app.settings import PORT, LOG_LEVEL


if __name__ == '__main__':
    uvicorn.run('app.fastapi:app', host="0.0.0.0", port=PORT, log_level=LOG_LEVEL, reload=True)
