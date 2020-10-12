from pydantic import BaseSettings, AnyHttpUrl
from typing import List
import os


class GlobalSettings(BaseSettings):

    API_PREFIX: str = '/api/v1.0/demo'
    COMMON_PREFIX: str = '/common/v1.0/demo'

    SECRET_KEY = 'IudhJtebnd0d863JKHdgui'

    PROJECT_NAME = 'fastapi-demo'

    DATABASE_POOL_SIZE = 30

    # 分页配置，每页默认值
    PAGE_SIZE = 10

    ALGORITHM = "HS256"

    # mysql数据库相关配置
    DATABASE_HOST: str = 'phoenix-mysql'
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = 'liuyz'
    DATABASE_PASSWORD: str = 'Zhian@2019'
    DATABASE_NAME: str = 'fastapi_demo'

    # redis相关配置
    REDIS_HOST: str = 'phoenix-redis'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = 'Antiddos2019'
    REDIS_DB: int = 1

    # 日志服务地址
    LOG_URL = "http://phoenix-log:8087/common/v1.0/log"

    class Config:
        case_sensitive = True


class DevelopSettings(GlobalSettings):
    # mysql数据库相关配置
    DATABASE_USER: str = 'liuyz'
    DATABASE_PASSWORD: str = 'Zhian@2019'
    DATABASE_HOST: str = '127.0.0.1'
    DATABASE_PORT: int = 19306
    DATABASE_NAME: str = 'fastapi_demo'

    # redis相关配置
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = 'Antiddos2019'
    REDIS_DB: int = 1

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['https://cloud9.zhianidc.com']

    # 日志服务地址
    LOG_URL = "http://127.0.0.1:8097/common/v1.0/log"


class DevDockerConfig(GlobalSettings):

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['https://cloud8.zhianidc.com']


class ProductionSettings(GlobalSettings):
    SECRET_KEY = 'ITsnHe8Wx5Xo2Ie2LxeS3wcRbxlIPms'

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['https://cloud.anlian.hk']


settings_by_name = dict(
    dev=DevelopSettings(),
    dev_docker=DevDockerConfig(),
    al_docker=ProductionSettings(),
)

settings = settings_by_name["dev"]
# settings = settings_by_name[os.getenv("PHOENIX_ENV", "dev")]



