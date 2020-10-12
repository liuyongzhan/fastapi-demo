import traceback
from fastapi import FastAPI, Request, Response

from app.api.utils.response import fail_response
from app.core.config import settings
from app.db.database import database as db, db_state_default
from starlette.middleware.cors import CORSMiddleware
from app.api.api import api_router
from fastapi.logger import logger
import logging

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_PREFIX}/openapi.json", docs_url="/")


@app.on_event("startup")
def startup():
    logger.info('连接数据库-------------------------------------------------------')
    db.connect()


@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        logger.info('关闭数据库-------------------------------------------------------')
        db.close()


def ha_close_db():
    try:
        db.close()
        # db.close_idle()  # 关闭空闲的连接，不包括任何当前正在使用的连接——只包括那些以前创建但已经返回到池中的连接。
        # db.manual_close()  # 关闭连接，而且不放回连接池。
        logger.debug('关闭数据库-------------------------------------------------------')
        logger.debug('关闭连接')
    except Exception as e:
        if not db.is_closed():
            db.close()
        logger.error(f'系统异常：{e}')
    finally:
        if not db.is_closed():
            db.close()


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
    logger.error(f'错误为{exc}')
    ha_close_db()
    return Response("Internal server error", status_code=500)


@app.middleware("http")
async def close_database(request: Request, call_next):
    db._state._state.set(db_state_default.copy())
    db._state.reset()

    try:
        if db.is_closed():
            db.connect()
            logger.debug('连接数据库-------------------------------------------------------')
    except Exception as e:
        logger.error(f'数据库连接失败，失败原因：{e}')

    response = await call_next(request)
    ha_close_db()

    return response

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.include_router(api_router)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)

