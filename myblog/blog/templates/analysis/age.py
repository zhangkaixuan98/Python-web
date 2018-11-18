import re
import pymysql.cursors
from datetime import datetime
import json
import sys


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


# 年龄区间
def age():
    db = MySQL()
    sql = """
select age, count(*) from ( select
case  
when (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )<20 then '20以下'  
when (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )>=20 and (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )<30 then '20-30'  
when (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )>=30 and (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )<40 then '30-40'  
when (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )>=40 and (year(now())-year(user_birth)-1) + ( DATE_FORMAT(user_birth, '%m%d') <= DATE_FORMAT(NOW(), '%m%d') )<50 then '40-50'   
else '大于50'
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
    print(jsonDate)


# 年代
def age2():
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
    print(jsonDate)


def redo():
    db = MySQL()
    sql = "update blog_user set user_birth = null where user_birth = '0000-00-00'"
    db.ExecNonQuery(sql)


if __name__ == '__main__':
    # redo()
    age()
    print('\n\n\n\n\n\n\n')
    age2()
