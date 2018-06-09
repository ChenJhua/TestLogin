from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户模型类"""
    # 不要定义int型,否则存不进数据库,会报错,Out of range
    # 建议使用char类型
    uphone = models.CharField(max_length=11)

    class Meta(object):
        # 指定表名
        db_table = 'df_user'


