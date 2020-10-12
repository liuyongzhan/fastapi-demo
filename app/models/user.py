from peewee import Model, CharField, DateTimeField
from app.db.database import database
import datetime


class UserInfo(Model):

    uuid = CharField(max_length=32, primary_key=True, index=True, verbose_name='uuid')
    name = CharField(max_length=32, verbose_name='用户名')
    email = CharField(max_length=64, verbose_name='邮箱')
    phone = CharField(max_length=32, verbose_name='电话')
    created = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    modified = DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        return super(UserInfo, self).save(*args, **kwargs)

    class Meta:
        database = database
        table_name = "user_info"
