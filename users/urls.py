from django.urls import path
from . import views

urlpatterns = [
    path('', views.userpanel, name='userpanel'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('changepw/', views.change_password, name='changepw'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('account/del/', views.del_account, name='del_account'),
]
