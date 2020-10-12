from fastapi import APIRouter, Depends, Query, Request

from app.api.utils.security import get_current_user
from app.schemas.user import User, AddUser, UpdateUser
from app.api.utils.response import success_response, fail_response
from app.core.config import settings
from app.service.user_service import list_user_s, add_user_s, del_user_s, update_user_s
from app.utils.log import Logger

router = APIRouter()
logger = Logger()


@router.post('/user', name='新增用户')
def add_user(*, add_user_schema: AddUser):
    logger.debug("", "", "新增用户", "", **{"add_user_schema": add_user_schema})

    return add_user_s(add_user_schema)


@router.delete('/user', name='删除用户')
def del_user(*, uuid: str = Query(..., description='uuid')):
    logger.debug("", "", "删除用户", "", **{"uuid": uuid})

    return del_user_s(uuid)


@router.put('/user', name='修改用户')
def update_user(*, update_user_schema: UpdateUser):
    logger.debug("", "", "修改用户", "", **{"update_user_schema": update_user_schema})

    return update_user_s(update_user_schema)


# @router.get('/user', name='用户列表', dependencies=[Depends(get_current_user)])
@router.get('/user', name='用户列表')
def list_user(*,
              name: str = Query(None, description='用户名'),
              email: str = Query(None, description='邮箱'),
              page: int = Query(1, description='页码'),
              page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
              ):
    logger.debug("", "", "用户列表", "", **{"name": name, "email": email})

    rs_list = list_user_s(name, email, page, page_size)

    return success_response(rs_list)