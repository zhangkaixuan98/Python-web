from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from pandas import json
import pymysql
import pymysql.cursors
from . import models


class MySQL:
    # def __init__(self,host=None,user=None,pwd=None,db=None):
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.pwd = '1998818'
        self.db = 'PythonWeb'

        self._conn = self.GetConnect()
        if (self._conn):
            self._cur = self._conn.cursor()

    # 连接数据库
    def GetConnect(self):
        conn = False
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db
            )
        except Exception as err:
            print("连接数据库失败, %s" % err)
        else:
            return conn

    # 执行查询
    def ExecQuery(self, sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

    # 执行含参数查询
    def ExecDataQuery(self, sql, data):
        res = ""
        try:
            self._cur.execute(sql % data)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

    # 执行非查询类语句
    def ExecNonQuery(self, sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as err:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % err)
        else:
            return flag

    # 获取连接信息
    def GetConnectInfo(self):
        print("连接信息：")
        print("服务器:%s , 用户名:%s , 数据库:%s " % (self.host, self.user, self.db))

    # 关闭数据库连接
    def Close(self):
        if (self._conn):
            try:
                if (type(self._cur) == 'object'):
                    self._cur.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except:
                raise ("关闭异常, %s,%s" % (type(self._cur), type(self._conn)))


# 首页
def index(request):
    topic_blog = models.blog.objects.all().order_by('-blog_view')[0:5]
    return render(request, 'index.html', {'topic_blog': topic_blog})


# 下拉加载
def blogs(request, number):
    if request.is_ajax():
        db = MySQL()
        sql = "select blog_id, blog_title, blog_date_time, blog_view, blog_content from blog_blog order by blog_date_time desc limit %d, %d"
        data = (int(number), 10)
        blogs = db.ExecDataQuery(sql, data)
        blogs_list = []
        for row in blogs:
            blogs = {'blog_id': row[0], 'blog_title': row[1], 'blog_date_time': str(row[2]), 'blog_view': row[3],
                     'blog_content': row[4].replace('�', '').replace(' ', '')[0: 100]}
            blogs_list.append(blogs)
        # print(blog_time_list)
        jsonDate = json.dumps(blogs_list, ensure_ascii=False)
        return HttpResponse(jsonDate, content_type='application/json')
    else:
        return HttpResponse('N')


# 文章详情
def blog_page(request, blog_id):
    blog = models.blog.objects.get(pk=blog_id)
    user = models.user.objects.get(pk=blog.blog_user_id)
    return render(request, 'blog_page.html', {'blog': blog, 'user': user})


# 分类
def category(request, category_name):
    if category_name == 'love':
        category_name = '爱情文章'
    elif category_name == 'family':
        category_name = '亲情文章'
    elif category_name == 'friend':
        category_name = '友情文章'
    elif category_name == 'life':
        category_name = '生活随笔'
    elif category_name == 'school':
        category_name = '校园文章'
    elif category_name == 'classic':
        category_name = '经典文章'
    elif category_name == 'philosophy':
        category_name = '人生哲理'
    elif category_name == 'encourage':
        category_name = '励志文章'
    elif category_name == 'diary':
        category_name = '心情日记/日志'
    elif category_name == 'funny':
        category_name = '搞笑文章'
    else:
        return render(request, '404.html')
    db = MySQL()
    db.GetConnect()
    sql = "select count(*) from blog_blog where blog_category = '%s'"
    data = category_name
    x = int(db.ExecDataQuery(sql, data)[0][0] / 10) + 1
    topic_blog = models.blog.objects.filter(blog_category=category_name).order_by('-blog_view')[0:5]
    jsonData = {'x': x, 'category': str(category_name)}
    category = json.dumps(jsonData, ensure_ascii=False)
    print(category)
    return render(request, 'blog_category.html',{'category': category, 'topic_blog': topic_blog})


# 分页加载
def blogs_category(request):
    data = request.GET
    print(data)
    number = int(data.get('number'))
    category = data.get('category')
    print(number, type(number))
    if request.is_ajax():
        db = MySQL()
        sql = "select blog_id, blog_title, blog_date_time, blog_view, blog_content from blog_blog where blog_category = '%s'order by blog_date_time desc limit %d, %d"
        data = (category, int(number), 10)
        blogs = db.ExecDataQuery(sql, data)
        blogs_list = []
        for row in blogs:
            blogs = {'blog_id': row[0], 'blog_title': row[1], 'blog_date_time': str(row[2]), 'blog_view': row[3],
                     'blog_content': row[4].replace('�', '').replace(' ', '')[0: 100]}
            blogs_list.append(blogs)
        jsonDate = json.dumps(blogs_list, ensure_ascii=False)
        return HttpResponse(jsonDate, content_type='application/json')
    else:
        return HttpResponse('N')


# 分析页
def analysis(request):
    # 性别
    def sex():
        sql = "select user_sex, count(*) from blog_user group by user_sex"
        sexes = db.ExecQuery(sql)
        sex_list = []
        for row in sexes:
            if not row[0] == '':
                sex_dict = {'sex': row[0], 'number': row[1]}
                sex_list.append(sex_dict)
        return json.dumps(sex_list, ensure_ascii=False)
    # 总数据
    def tall():
        db = MySQL()
        sql = "select count(*) from blog_user"
        user_number = db.ExecQuery(sql)
        sql = "select count(*) from blog_blog"
        blog_number = db.ExecQuery(sql)
        sex_list = []
        sex_dict = {'number': blog_number[0][0]}
        sex_list.append(sex_dict)
        sex_dict = {'number': user_number[0][0]}
        sex_list.append(sex_dict)
        return json.dumps(sex_list, ensure_ascii=False)
    # 时间段
    def blog_time():
        db = MySQL()
        sql = "select date_format (blog_date_time, '%H'), count(*) from blog_blog group by date_format (blog_date_time, '%H')"
        blog_time = db.ExecQuery(sql)
        blog_time_list = []
        for row in blog_time:
            blog_time = {'time': row[0], 'number': row[1]}
            blog_time_list.append(blog_time)
        return json.dumps(blog_time_list, ensure_ascii=False)
    # 省份分布
    def address():
        db = MySQL()
        sql = "select user_address, count(*) from blog_user group by user_address"
        address = db.ExecQuery(sql)
        address_list = []
        for row in address:
            if not row[0] == '保密':
                address_dict = {'address': row[0], 'number': row[1]}
                address_list.append(address_dict)
        jsonDate = json.dumps(address_list, ensure_ascii=False)
        return jsonDate
    # 迁移
    def migrate2():
        db = MySQL()
        sql = """select user_address, count(*) from (
        select migrate, user_address, user_hometown, count(*) from ( select
        case
        when user_address = '保密' or user_hometown = '保密' then '保密'
        when user_address != '保密' and user_hometown != '保密' and user_address = user_hometown then '否'
        else '是'
        end as migrate, user_address, user_hometown
        from blog_user
        ) as user_migrate
        group by migrate, user_address, user_hometown) as migrate_address
        group by user_address;"""
        migrate = db.ExecQuery(sql)
        migrate_list = []
        for row in migrate:
            migrate_dict = {'address': row[0], 'number': row[1]}
            migrate_list.append(migrate_dict)
        jsonDate = json.dumps(migrate_list, ensure_ascii=False)
        return jsonDate
    # 星座
    def star():
        db = MySQL()
        sql = "select user_star, count(*) from blog_user group by user_star"
        star = db.ExecQuery(sql)
        star_list = []
        for row in star:
            if not row[0] == '保密':
                star_dict = {'star': row[0], 'number': row[1]}
                star_list.append(star_dict)
        jsonDate = json.dumps(star_list, ensure_ascii=False)
        return jsonDate
    # 分类
    def blog():
        db = MySQL()
        sql = "select blog_category, count(*) from blog_blog group by blog_category"
        blogs = db.ExecQuery(sql)
        blogs_list = []
        for row in blogs:
            blogs = {'category': row[0], 'number': row[1]}
            blogs_list.append(blogs)
        # print(blog_time_list)
        jsonDate = json.dumps(blogs_list, ensure_ascii=False)
        return jsonDate
    # 年月
    def blog_year():
        db = MySQL()
        sql = "select year (blog_date_time), month (blog_date_time), count(*) from blog_blog group by  year (blog_date_time), month (blog_date_time)"
        blog_num = db.ExecQuery(sql)
        blog_num_list = []
        for row in blog_num:
            blog_num = {'year_month': str(row[0]) + ' ' + str(row[1]), 'number': row[2]}
            blog_num_list.append(blog_num)
        jsonDate = json.dumps(blog_num_list, ensure_ascii=False)
        return jsonDate
    # 发表最多用户前20
    def active_user():
        db = MySQL()
        sql = """select user_name, user_blog from (
        select user_name, count(*) as user_blog
        from blog_user, blog_blog 
        where user_id = blog_user_id 
        group by user_name) as active_user
        order by user_blog desc limit 10"""
        active_user = db.ExecQuery(sql)
        active_user_list = []
        for row in active_user:
            active_user_dict = {'user': row[0], 'number': row[1]}
            active_user_list.append(active_user_dict)
        jsonDate = json.dumps(active_user_list, ensure_ascii=False)
        return jsonDate
    # 年代
    def age():
        db = MySQL()
        sql = """
        select age, count(*) from ( select
        case  
        when 2000 <= year(user_birth) then '00后'
        when 1990 <= year(user_birth) and year(user_birth) < 2000 then '90后'
        when 1980 <= year(user_birth) and year(user_birth) < 1990 then '80后'
        when 1970 <= year(user_birth) and year(user_birth) < 1980 then '70后'
        when 1960 <= year(user_birth) and year(user_birth) < 1970 then '60后'
        else '60前'
        end as age
        from blog_user
        ) as user_age
        group by age;"""
        age = db.ExecQuery(sql)
        age_list = []
        for row in age:
            age_dict = {'age': row[0], 'number': row[1]}
            age_list.append(age_dict)
        jsonDate = json.dumps(age_list, ensure_ascii=False)
        return jsonDate
    db = MySQL()
    sex = sex()
    tall = tall()
    blog_time = blog_time()
    address = address()
    migrate = migrate2()
    star = star()
    category = blog()
    year = blog_year()
    active_user = active_user()
    age = age()
    db.Close()
    return render(request, 'analysis.html', {'sex': sex, 'tall': tall, 'blog_time': blog_time, 'address': address, 'migrate': migrate, 'star': star, 'category': category, 'year': year, 'active_user': active_user, 'age': age})


# 查询
def search(request):
    if request.method == 'POST':
        print("the POST method")
        concat = request.POST
        print(concat)
        title = concat['title']
    jsonData = json.dumps({'title': title}, ensure_ascii=False)
    topic_blog = models.blog.objects.all().order_by('-blog_view')[0:5]
    return render(request, 'search.html', {'topic_blog': topic_blog, 'title': jsonData})


# 下拉加载
def search_ajax(request):
    data = request.GET
    print(data)
    number = int(data.get('number'))
    title = "'%" + data.get('title') + "%'"
    if request.is_ajax():
        db = MySQL()
        sql = "select blog_id, blog_title, blog_date_time, blog_view, blog_content from blog_blog where blog_title like %s limit %d, %d"
        data = (title, int(number), 10)
        blogs = db.ExecDataQuery(sql, data)
        blogs_list = []
        for row in blogs:
            blogs = {'blog_id': row[0], 'blog_title': row[1], 'blog_date_time': str(row[2]), 'blog_view': row[3],
                     'blog_content': row[4].replace('�', '').replace(' ', '')[0: 100]}
            blogs_list.append(blogs)
        # print(blog_time_list)
        jsonDate = json.dumps(blogs_list, ensure_ascii=False)
        return HttpResponse(jsonDate, content_type='application/json')
    else:
        return HttpResponse('N')