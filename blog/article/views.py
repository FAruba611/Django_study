from django.shortcuts import render, redirect

# 导入HttpResponse模块
from django.http import HttpResponse


from .models import ArticlePost
from .forms import ArticlePostForm

#引入user模型
from django.contrib.auth.models import User


import markdown
# Create your views here.





# 视图函数
def article_list(request):
    # 初始化：return HttpResponse("Hello World!")
    # 取出所有博客文章
    articles = ArticlePost.objects.all()

    # 需要传递给模板（template）的对象
    context = { 'articles': articles }

    return render(request, 'article/list.html', context)

def article_detail(request, id):
    # 取出相应得文章
    article = ArticlePost.objects.get(id=id)

    # 将文章markdown语法渲染成html格式
    article.body = markdown.markdown(article.body, 
        extension=[
           # 包含 缩写、表格等常用扩展
           'markdown.extensions.extra',
           # 语法高亮扩展 
           'markdown.extensions.codehilite',
        ])

    # 需要传递给模板的对象
    context = { 'article': article }

    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

def article_create(request):
    #判断用户是否提交数据
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)

        if article_post_form.is_valid():

            new_article = article_post_form.save(commit=False)

            new_article.author = User.objects.get(id=1)

            new_article.save()

            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form': article_post_form }

        return render(request, 'article/create.html', context)

def article_delete(request, id):
    # article = ArticlePost.objects.get(id=id)

    # article.delete()

    # return redirect("article:article_list")
    return render(request, "base.html", "<h1>Testing...</h1>")

def article_safe_delete(request, id):
    #视图一定要限制为POST 
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单
    GET方法进入初始表单页面
    id: 文章的id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        #表单实例：包含提交的数据
        article_post_form = ArticlePostForm(data=request.POST)
        
        if article_post_form.is_valid():
            #保存新写入的title, body数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            #完成后返回到修改后的文章中，需传入文章的id值
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article': article, 'article_post_form': article_post_form }
        return render(request, 'article/update.html', context)