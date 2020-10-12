import jwt
import requests
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jwt.exceptions import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from app.core.config import settings

reusable_oauth2 = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    """
    校验用户
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="用户认证失败，请重新登陆"
        )
    user = payload.get('identity')
    data = {
        'uid': user.get('uid')
    }
    url = f'{settings.AUTH_URL}/identity'
    res = requests.post(url, data).json()
    if res.get('status') == 'fail':
        message = res.get('message')
        raise HTTPException(status_code=404, detail=message)
    else:
        return res.get('result')


def get_current_staff(request: Request, token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    """
    校验用户
    :param token:
    :param request:
    :return:
    """
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="用户认证失败，请重新登陆"
        )
    user = payload.get('identity')
    data = {
        'uid': user.get('uid')
    }
    url = f'{settings.AUTH_URL}/common/v1.0/auth/staff_identity'
    res = requests.post(url, data).json()
    if res.get('status') == 'fail':
        message = res.get('message')
        raise HTTPException(status_code=404, detail=message)
    else:
        path = request.url.path
        method = request.method
        if "​/api​/v1.0​/ticket​/staff​/remark​/upload_file" in path:
            path = '/api​/v1.0​/ticket​/staff​/remark​/upload_file'
        if "​/api​/v1.0​/ticket​/staff​/contact_file​" in path:
            path = '​/api​/v1.0​/ticket​/staff​/contact_file​'
        data = {
            'uid': user.get('uid'),
            'request_method': method,
            'request_path': path
        }
        response = requests.post(f'{settings.AUTH_URL}/permission', data).json()
        if not response.get('result'):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail='您无权操作'
            )
        return res.get('result')