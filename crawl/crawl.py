import copy
import re
import requests
import pymysql.cursors
from bs4 import BeautifulSoup
import time

send_head = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive"
}
link_page = set()
link_next = set()


def get_class_link(url):
    html = requests.get(url, send_head)
    html.encoding = 'gb2312'
    soup = BeautifulSoup(html.text, 'html.parser')
    # 分类链接
    blog_class = soup.select('.daohang')[0].select('a')[1: -2]
    for link in blog_class:
        link_next.add(link['href'])


def get_blog_link(n):
    for url in link_page:
        html = requests.get(url, send_head)
        html.encoding = 'gb2312'
        soup = BeautifulSoup(html.text, 'html.parser')
        # 当前位置
        now_local = soup.select('.pindao')[0].contents[3]['href']
        # 标题链接
        class_and_title = soup.select('.tbspan')[3].select('b')
        for class_title in class_and_title:
            # print(class_title.select('a'))
            if len(class_title.select('a')) == 1:
                n += 1
                url = class_title.select('a')[0]['href']
                print('第' + str(n) + '篇文章')
                blog_download(url)
                # link_need_download.add(url)
            if len(class_title.select('a')) == 2:
                n += 1
                url = class_title.select('a')[1]['href']
                print('第' + str(n) + '篇文章')
                blog_download(url)
                # link_need_download.add(url)
        # 下页链接
        links = soup.select('.tbspan')[3].select('a')
        for link in links:
            if link.text == '下一页':
                link_next.add(now_local + link['href'])
    return n


def blog_download(url):
    sql = "select * from blog_blog where blog_url = '%s'"
    data = url
    cursor.execute(sql % data)
    blog = cursor.fetchall()
    if not len(blog) == 0:
        print('exist')
        return 0
    else:
        html = requests.get(url, send_head)
        html.encoding = 'gb2312'
        soup = BeautifulSoup(html.text, 'html.parser')
        # 分类
        blog_category = soup.select('.pindao')[0].select('a')[1].text
        # 文章标题
        blog_title = soup.select('h1')[0].text
        # 作者id 作者链接
        try:
            user_id = 0
            blog_user = soup.select('.author')[0].select('a')[0].text
            if not blog_user == '':
                user_url = 'http://www.duwenzhang.com' + soup.select('.author')[0].select('a')[0]['href'] + "&action=infos"
                sql = "select user_id from blog_user where user_url = '%s'"
                data = user_url
                cursor.execute(sql % data)
                users = cursor.fetchall()
                if len(users) == 0:
                    if info_download(user_url):
                        sql = "select user_id from blog_user where user_url = '%s'"
                        data = user_url
                        cursor.execute(sql % data)
                        users = cursor.fetchall()
                        user_id = users[0][0]
                    else:
                        return 0
                elif len(users) == 1:
                    user_id = users[0][0]
            else:
                return 0
        except:
            print('作者',url)
        # 时间
        blog_date_time = 0
        try:
            date_time = soup.select('.author')[0].contents[2]
            # date_time 2010-12-07 14:37 <class 'str'>
            date_time1 = re.findall(r"时间：(.+?) 阅读：", date_time)[0]
            # time0 time.struct_time(tm_year=2010, tm_mon=12, tm_mday=7, tm_hour=14, tm_min=37, tm_sec=0, tm_wday=1, tm_yday=341, tm_isdst=-1)
            # <class 'time.struct_time'>
            date0 = time.strptime(date_time1, '%Y-%m-%d %H:%M')
            # date1 1291703820.0 <class 'float'>
            date1 = time.mktime(date0)
            date1 -= 28800
            # date2 time.struct_time(tm_year=2010, tm_mon=12, tm_mday=7, tm_hour=6, tm_min=37, tm_sec=0, tm_wday=1, tm_yday=341, tm_isdst=0)
            # <class 'time.struct_time'>
            date2 = time.localtime(date1)
            # 2010-12-07 06:37:00 <class 'str'>
            blog_date_time = time.strftime('%Y-%m-%d %H:%M:%S', date2)
        except:
            print('时间', url)
        # 浏览数
        try:
            php_url = soup.select('.author')[0].select('script')[0]['src']
            blog_view = get_view(php_url)
        except:
            print('浏览数', url)
        # 评论数
        try:
            php_url2 = soup.select('center')[0].select('table')[3].select('script')[5]['src']
            blog_comment = get_comment(php_url2)
        except:
            print('评论数', url)
        # 文章内容
        try:
            blog_content = soup.select('#wenzhangziti')[0].text.replace("'", "\\'")
        except:
            print('文章内容：', url)
        # 写入数据库
        # print(blog_content)
        try:
            sql = """
                insert into blog_blog
                (blog_title, blog_url, blog_content, blog_date_time, blog_view, blog_comment,blog_user_id, blog_category)
                values ('%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s')"""
            date = (blog_title, url, blog_content, blog_date_time, int(blog_view), int(blog_comment), user_id, blog_category)
            cursor.execute(sql % date)
            connect.commit()
            print('插入成功')
        except:
            print('数据库',url)


def get_view(url):
    try:
        view_php = requests.get(url, send_head)
        view_php.encoding = 'gb2312'
        view = str(BeautifulSoup(view_php.text, 'html.parser'))
        return re.findall(r"'(.+?)'", view)[0]
    except:
        print('getView:', url)


def get_comment(url):
    try:
        view_php = requests.get(url, send_head)
        view_php.encoding = 'gb2312'
        view = BeautifulSoup(view_php.text, 'html.parser').text
        return re.findall(r"所有感言\((.+?)条", view)[0]
    except:
        print('getComment:', url)

def info_download(url):
    try:
        html = requests.get(url, send_head)
        html.encoding = 'gb2312'
        soup = BeautifulSoup(html.text, 'html.parser')
        # 文章标题
        infos = soup.select('div')[7].select('dl')[1].select('tr')
        # 昵称
        name = infos[0].select('td')[1].text.replace('�', '')
        # 性别
        sex = infos[1].select('td')[1].text
        # 地址
        address = infos[2].select('td')[1].text.replace(' ', '').replace('\r', '').replace('\xa0', '')
        address = re.findall(r"(.+?)城市：", address)
        if len(address) == 0:
            address = '保密'
            # addres.append('保密')
        else:
            address = address[0]
        # 家乡
        hometown = infos[3].select('td')[1].text.replace(' ', '').replace('\r', '').replace('\xa0', '')
        hometown = re.findall(r"(.+?)城市：", hometown)

        if len(hometown) == 0:
            hometown = '保密'
            # addres.append('保密')
        else:
            hometown = hometown[0]
        # 生日
        birth = infos[4].select('td')[1].text
        # 交友目的
        aim = infos[5].select('td')[1].text
        # 感情状态
        status = infos[6].select('td')[1].text
        # 星座
        star = infos[7].select('td')[1].text
        # 血型
        blood = infos[8].select('td')[1].text
        # 身高
        height = infos[9].select('td')[1].text.replace('>', '').replace(' 厘米', '')
        # 体型
        shape = infos[10].select('td')[1].text
        print(name, sex, address, hometown, birth, aim, status, star, blood, height, shape)
        # 写入数据库
        # , user_addres = %s, user_hometown = %s, user_birth = %s, user_aim = %s, user_status = %s, user_star = %s, user_blood = %s, user_height = %s, user_shape = %s
        # , addres, hometown, birth, aim, status, star, blood, height, shape

        sql = """
    insert into  blog_user
    (user_name, user_url, user_sex, user_address, user_hometown, user_birth, user_aim, user_status, user_star, user_blood, user_height, user_shape)
    values ('%s','%s', '%s','%s','%s','%s', '%s','%s', '%s','%s','%s','%s')"""
        date = (name, url, sex, address, hometown, birth, aim, status, star, blood, height, shape)
        cursor.execute(sql % date)
        connect.commit()
        # print('插入成功')
        return 1
    except:
        print('info:',url)
        return 0


if __name__ == '__main__':
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1998818',
        db='PythonWeb',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()

    # 获取分类链接
    get_class_link('http://www.duwenzhang.com/')
    number = 0
    while len(link_next) != 0:
        link_page.clear()
        link_page = copy.deepcopy(link_next)
        link_next.clear()
        number = get_blog_link(number)
    print(number)

    # 关闭连接
    cursor.close()
    connect.close()
