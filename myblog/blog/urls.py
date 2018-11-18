from django.contrib import admin
import re
from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 分析
    path('analysis', views.analysis, name='analysis'),
    # 文章详情
    path('blogs/<int:blog_id>/', views.blog_page, name='blog_page'),
    # 下拉加载
    path('blogs/ajax/<int:number>', views.blogs, name='blog_add'),
    # 分类
    path('category/<str:category_name>', views.category, name='blog_category'),
    # 分页加载
    path('blogs/category/ajax/', views.blogs_category, name='blog_paging'),
    # 查询
    path('blogs/search', views.search, name='search'),
    # 分页加载
    path('blogs/search/ajax/', views.search_ajax, name='search_ajax'),
    # path('sql/', views.sql, name='sql'),
    # path('sqls/', views.sqls, name='sqls'),
    # path('dict/', views.dict, name='dict'),
]