import requests
from playhouse.shortcuts import model_to_dict

from app.api.utils.response import success_response
from app.core.redis_app import redis_client
from app.models.user import UserInfo
from app.schemas.user import AddUser, UpdateUser
from app.service.public_service import add_oper_log, generate_uuid
from app.utils.log import Logger

logger = Logger()


def list_user_s(name, email, page, page_size):
    name_str = "%" + name + "%" if name else "%%"
    email_str = "%" + email + "%" if email else "%%"
    user_info_set = UserInfo.select().where(UserInfo.name ** name_str, UserInfo.email ** email_str)

    total = user_info_set.count()
    user_info_set = user_info_set.paginate(page, page_size)

    rs_list = list()
    for i in user_info_set:
        tmp_dict = model_to_dict(i)
        rs_list.append(tmp_dict)

    result = {"list": rs_list, "total": total}

    return result


def add_user_s(add_user_schema: AddUser):
    uuid = generate_uuid()

    UserInfo.create(uuid=uuid,
                    name=add_user_schema.name,
                    email=add_user_schema.email,
                    phone=add_user_schema.phone,
                    )

    return success_response("新增用户成功")


def del_user_s(uuid):

    UserInfo.delete().where(UserInfo.uuid == uuid).execute()

    return success_response("删除用户成功")


def update_user_s(update_user_schema: UpdateUser):
    uuid = update_user_schema.uuid
    name = update_user_schema.name
    email = update_user_schema.email
    phone = update_user_schema.phone

    user_model = UserInfo.get_or_none(uuid=uuid)
    if not user_model:
        return user_model("资源已被冻结或不存在")

    if name is not None:
        user_model.name = name
    if email is not None:
        user_model.email = email
    if phone is not None:
        user_model.phone = phone

    user_model.save()

    return success_response("修改用户成功")
