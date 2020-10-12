import json
import random
import time
import uuid

import requests
from app.utils.log import Logger

from app.core.config import settings

logger = Logger()


def generate_uuid():
    uuid_str = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).replace("-", "")
    return uuid_str


def add_log(**param):
    url = settings.LOG_URL + '/add_log'
    headers = {'Content-Type': 'application/json'}
    for i in range(0, 3):
        try:
            r = requests.post(url, data=json.dumps(param), headers=headers)
            if r.status_code == requests.codes.ok:
                if r.json()["status"] == "success":
                    return r.json()
                else:
                    raise Exception('状态码[%s]--信息[%s]' % (r.status_code, r.json()))
            elif str(r.status_code).startswith("4"):
                raise Exception('状态码[%s]--信息[%s]' % (r.status_code, r))
            else:
                raise Exception('状态码[%s]--信息[%s]' % (r.status_code, r.json()))
        except Exception as e:
            time.sleep(1)
            if i == 2:
                raise Exception('调用日志服务添加操作日志异常，异常信息:{}，url：{}'.format(e, url))


def add_oper_log(request, rs, rs_name, desc, before, after, user_name, operator=""):
    param = {
            "classification": rs,
            "dispose_name": rs_name,
            "description": desc,
            "before_operation": str(before),
            "after_operation": str(after),
            "user_name": user_name,
        }
    if operator:
        param["operator_name"] = operator
    try:
        if request.headers.get('X-Forwarded-For'):
            ip_str = request.headers.get('X-Forwarded-For').split(',')[0]
        elif request.client.host:
            ip_str = request.client.host
        else:
            ip_str = ''
        user_agent = request.headers.get("User-Agent", "")

        param["ip"] = ip_str
        param["user_agent"] = user_agent

        add_log(**param)
    except Exception as e:
        logger.error("", "", "记录操作日志", e, **{"param": param})
