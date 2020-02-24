from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import BlogCategory, Blog, BlogComment
from django.db.models import Q
from django.http import JsonResponse

# 查询easy_thumbnails生成的略缩图类
from easy_thumbnails.files import get_thumbnailer

# 分页工具
from django.core.paginator import Paginator
def pagination(queryset, display_num, page_num):
    content = Paginator(queryset, display_num).get_page(page_num)
    if content.paginator.num_pages <= 5 :
        pagerange = list(range(1, content.paginator.num_pages + 1))
    elif content.number <= 3 :
        pagerange = [ 1 , 2 , 3 , 4 , 5 , '...' ]
    elif content.number >= (content.paginator.num_pages - 2) :
        pagerange = [ '...', content.paginator.num_pages - 4 , content.paginator.num_pages - 3 , content.paginator.num_pages - 2 , content.paginator.num_pages - 1 , content.paginator.num_pages ]
    else :
        pagerange = [ '...' , content.number - 2 , content.number - 1 , content.number , content.number + 1 , content.number + 2 , '...' ]
    
    context = {'content':content, 'pagerange':pagerange}
    
    return context

# Create your views here.
def search(request):
    if request.method == 'GET':
        keyword = request.GET.get('s', '')
        if keyword != '':
            page_num = request.GET.get('page')
            query_blogs = Blog.objects.filter(Q(title=keyword)|Q(content__icontains=keyword))
            count = query_blogs.count()
            page = pagination(query_blogs, 10, page_num)
            blogs = page['content']
            pagerange = page['pagerange']
            return render(request, 'blog-list.html', {'keyword':keyword, 'count':count, 'blogs':blogs, 'pagerange':pagerange})
        else:
            return redirect('blog_list')

def about(request):
    return render(request, 'about-us.html')

def blog_list(request):
    blogs = Blog.objects.all()
    page_num = request.GET.get('page')
    page = pagination(blogs, 10, page_num)
    blogs = page['content']
    pagerange = page['pagerange']
    return render(request, 'blog-list.html', {'blogs':blogs, 'pagerange':pagerange})

def blog_item(request, id):
    blog = get_object_or_404(Blog, pk=id)
    comments = BlogComment.objects.filter(blog=blog)
    related_blogs = Blog.objects.exclude(pk=id).filter(category=blog.category)[:3]
    return render(request, 'blog-item.html', {'blog':blog, 'comments':comments, 'related_blogs':related_blogs})

# 新建博客
@login_required
def create_blog(request):
    warning = []
    categories = BlogCategory.objects.all()[:10]

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        add_category = request.POST.get('add_category')
        content = request.POST.get('content')
        
        blog = Blog()
        blog.author = request.user
        blog.title = title
        if add_category:
            try:
                has_category = BlogCategory.objects.get(name=add_category)
                blog.category = has_category
            except BlogCategory.DoesNotExist:
                blog.category = BlogCategory.objects.create(name=add_category)
        else:
            blog.category_id = category
        blog.content = content

        try:
            image = request.FILES['image']
            blog.image = image
        except:
            warning = ['未提交图片!']

        blog.save()

        warning += ['博客创建成功!', '5秒钟后跳转至文章页面']
        rewrite = '<meta http-equiv="refresh" content="5;URL=' + reverse('blog_item', kwargs={'id':blog.id}) + '" />'
        return render(request, 'blog-edit.html', {'blog': blog, 'categories':categories, 'warning': warning, 'rewrite': rewrite})

    else: 
        return render(request, 'blog-edit.html', {'categories':categories})

# 编辑博客
@login_required
def edit_blog(request, id):
    warning = []
    categories = BlogCategory.objects.all()[:10]
    blog = get_object_or_404(Blog, pk=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        add_category = request.POST.get('add_category')
        content = request.POST.get('content')

        if title == '' :
            warning += ['标题字段为空']
        else:
            if title == blog.title:
                warning += ['标题未修改']
            else:
                blog.title = title

        if add_category:
            try:
                has_category = BlogCategory.objects.get(name=add_category)
                blog.category = has_category
            except BlogCategory.DoesNotExist:
                blog.category = BlogCategory.objects.create(name=add_category)
        else:
            blog.category_id = category
        blog.content = content

        try:
            image = request.FILES['image']
            # 如果有新图就删老图
            if blog.image != 'images/default/blog.jpg':
                blog.image.delete(False)
                thumbnailer = get_thumbnailer(blog.image)
                thumbnailer.delete_thumbnails()
                thumbnailer.delete()
            blog.image = image
        except:
            warning += ['图片未修改']
        
        blog.save()
        warning += ['文章保存成功！']

        return render(request, 'blog-edit.html', {'warning':warning, 'blog': blog, 'categories':categories})

    else:  
        return render(request, 'blog-edit.html', {'blog': blog,'categories':categories})

# 删除博客
@login_required
def delete_blog(request, id):
    next = request.GET.get('next', '')
    blog = get_object_or_404(Blog, pk=id)
    if request.user == blog.author:
        blog.delete()
        if next:
            return redirect(next)
        else:
            return redirect('blog_list')

# 管理所有评论
@login_required
def all_comments(request):
    page_num = request.GET.get('page')
    all_comments = BlogComment.objects.filter(author=request.user)
    count = all_comments.count()
    page = pagination(all_comments, 10, page_num)
    comments = page['content']
    pagerange = page['pagerange']
    return render(request, 'comments.html', {'comments':comments, 'pagerange':pagerange, 'count':count})

# Ajax发表评论
@login_required
def blog_comment(request, id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = BlogComment()
            comment.blog_id = id
            comment.content = content
            comment.author = request.user
            comment.save()
            message = '评论发表成功！'
            return JsonResponse({'message':message})

@login_required
def blog_comment_del(request, id):
    comment = get_object_or_404(BlogComment, pk=id)
    operator = request.user
    if comment.author == operator:
        comment.delete()
        return JsonResponse({'message':'评论删除成功!'})

@login_required
def blog_add_category(request):
    if request.method == 'POST':
        caregory = request.POST.get('category')
        if caregory:
            new_category = BlogCategory.objects.create(name=caregory)
            return JsonResponse({'message':'博客类别创建成功！', 'id':new_category.id})

@login_required
def blog_category_del(request, id):
    category = get_object_or_404(BlogCategory, pk=id)
    if request.user.is_staff:
        category.delete()
        return JsonResponse({'message':'类别删除成功!'})

def page_not_found(request, exception):
 return render(request, '404.html')
 
def server_error(request):
 return render(request, '500.html')