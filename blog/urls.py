"""buddyright URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import pages.views
import users.urls

from django.conf import settings             # 导入设置
from django.conf.urls.static import static   # 导入静态链接

urlpatterns = [
    path('admin/', admin.site.urls),
    # 网站页面
    path('search/', pages.views.search, name='search'),
    path('about/', pages.views.about, name='about'),
    # 子系统
    path('user/', include(users.urls)),
    # 博客
    path('', pages.views.blog_list, name='blog_list'),
    path('create/', pages.views.create_blog, name='create_blog'),
    path('del/<int:id>/', pages.views.delete_blog, name='delete_blog'),
    path('edit/<int:id>/', pages.views.edit_blog, name='edit_blog'),
    path('<int:id>/', pages.views.blog_item, name='blog_item'),
    path('<int:id>/comment/', pages.views.blog_comment, name='blog_comment'),
    path('comment/del/<int:id>/', pages.views.blog_comment_del, name='blog_comment_del'),
    path('comment/all/', pages.views.all_comments, name='all_comments'),
    path('category/add/', pages.views.blog_add_category, name='blog_add_category'),
    path('category/del/<int:id>/', pages.views.blog_category_del, name='blog_category_del'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 增加媒体文件链接

handler404 = pages.views.page_not_found
handler500 = pages.views.server_error
