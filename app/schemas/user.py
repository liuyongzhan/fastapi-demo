from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class User(BaseModel):
    uid: str
    user_name: str
    real_name: str
    email: EmailStr = Field(None, description='邮箱')
    phone_number: str = Field(None, description='手机号')
    id: Optional[int] = Field(None, description='id')
    global_permission: Optional[bool] = Field(..., description='是否有全局数据权限')
    department_name_list: Optional[List[str]] = Field(..., description='所属部门')


class AddUser(BaseModel):
    name: str = Field(..., max_length=32, description='用户名')
    email: str = Field(..., max_length=64, description='邮箱')
    phone: str = Field(..., max_length=32, description='电话')

    class Config:
        schema_extra = {
            "example": {
                "name": "用户名",
                "email": "1665439369@qq.com",
                "phone": "15768218888",
            }
        }


class UpdateUser(BaseModel):
    uuid: str = Field(..., max_length=32, description='uuid')
    name: str = Field(None, max_length=32, description='用户名')
    email: str = Field(None, max_length=64, description='邮箱')
    phone: str = Field(None, max_length=32, description='电话')

    class Config:
        schema_extra = {
            "example": {
                "uuid": "uuid",
                "name": "用户名",
                "email": "1665439369@qq.com",
                "phone": "15768218888",
            }
        }