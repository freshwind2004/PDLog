from django.db import models

# Create your models here.
# 引入 AbstractUser
from django.contrib.auth.models import AbstractUser

#创建用户类
class User(AbstractUser):

    telephone   = models.CharField(blank=True, max_length=11, verbose_name='电话')
    nickname    = models.CharField(blank=True, max_length=10, verbose_name='昵称')

    # USERNAME_FIELD = 'telephone'
    # 在这里，我们不改变用户名的名称为 telephone， 所以注释掉

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username