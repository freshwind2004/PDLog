from django.db import models
from users.models import User

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.utils.translation import gettext_lazy as _

# Create your models here.
class BlogCategory(models.Model):
    
    name     = models.CharField(default='Blog Category', max_length=100, verbose_name=_('分类名')) 

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = _('博客分类')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    
    title     = models.CharField(default='Blog Title', max_length=100, verbose_name=_('标题'))
    category  = models.ForeignKey(BlogCategory, null=True, on_delete=models.SET_NULL, verbose_name=_('类别'))
    content   = models.TextField(default='The blog content goes here...', verbose_name=_('内容'))
    author    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('作者'))
    image     = models.ImageField(default='images/default/blog.jpg', upload_to='images/blogs/%Y/%m/', verbose_name=_('题图'))
    time      = models.DateTimeField(auto_now_add=True, verbose_name=_('日期'))

    class Meta:

        verbose_name = _('博客内容')
        verbose_name_plural = verbose_name
        ordering = ['-time']

    def __str__(self):
        return self.title

@receiver(pre_delete, sender=Blog)
def file_delete(sender, instance, **kwargs):
    if instance.image != 'images/default/blog.jpg':
        # 删除图片
        instance.image.delete(False)

class BlogComment(models.Model):

    blog    = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=_('博客'))
    content = models.TextField(default='The blog comment content goes here...', verbose_name=_('评论内容'))
    time    = models.DateTimeField(auto_now_add=True, verbose_name=_('日期'))
    author  = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_('作者'))

    class Meta:
        verbose_name = '_(博客评论)'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.author)