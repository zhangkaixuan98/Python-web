import pymysql.cursors
import json


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


# 发表最多用户前20
def active_user():
    db = MySQL()
    sql = """select user_name, user_blog from (
select user_name, count(*) as user_blog
from blog_user, blog_blog 
where user_id = blog_user_id 
group by user_name) as active_user
order by user_blog desc limit 20"""
    active_user = db.ExecQuery(sql)
    active_user_list = []
    if not active_user == '':
        for row in active_user:
            active_user_dict = {'user': row[0], 'blog_number': row[1]}
            active_user_list.append(active_user_dict)
        jsonDate = json.dumps(active_user_list, ensure_ascii=False)
        print(jsonDate)
    else:
        print(active_user)


def active_user2():
    db = MySQL()
    sql = """
select user_name, blog_date_time
from blog_user, blog_blog 
where user_id = blog_user_id
order by blog_date_time desc limit 20"""
    active_user = db.ExecQuery(sql)
    active_user_list = []
    for row in active_user:
        active_user_dict = {'user': row[0], 'time': str(row[1])}
        active_user_list.append(active_user_dict)
    jsonDate = json.dumps(active_user_list, ensure_ascii=False)
    print(jsonDate)


if __name__ == '__main__':
    active_user()
    print('\n\n\n\n')
    active_user2()