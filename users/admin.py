from django.contrib import admin

from .models import User
# 引入用户管理类.
from django.contrib.auth.admin import UserAdmin

# 注册UserAdmin
class UserAdmin(UserAdmin):
    #重写fieldsets在admin后台加入自己新增的字段
    list_display = ['id', 'username', 'email', 'telephone']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('email', 'telephone')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# Register your models here.

admin.site.register(User, UserAdmin)