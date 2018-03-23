# encoding:utf8
import sys
import pymysql

reload(sys)
sys.setdefaultencoding('utf-8')


class DBHandle(object):
    def __init__(self,host="localhost",user="root",password="new_password",database="wsalon",debug=0):
        db = pymysql.connect(host,user,password,database,charset="utf8")
        self.db = db

    def execute_sql(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def dbclose(self):
        self.db.close()

def check(dbh):
    result = dbh.execute_sql("select start,end from app_salon")
    for item in result:
        start_time_dd = item[0]
        end_time_dd = item[1]
        if start_time_dd.year != end_time_dd.year:
            print "Year %s : %s" % (start_time_dd.year, end_time_dd.year)
            return 0
        #if start_time_dd.month != end_time_dd.month:
            #print "Month %s : %s" % (start_time_dd.month, end_time_dd.month)
            #return 0
        #if start_time_dd.day != end_time_dd.day:
            #print "Day %s : %s" % (start_time_dd.day, end_time_dd.day)
            #return 0
    return 1


def analyze(start):
    hour = str(start.time()).split(":")[0]
    if int(hour) <= 12:
        return 0
    if int(hour) <= 18:
        return 1
    if int(hour) <= 24:
        return 2

def main():
    dbh = DBHandle()
    try:
        #print check(dbh)
        print analyze(dbh.execute_sql("select start,end from app_salon where id = 7492")[0][0])# 得到一个datetime.datetime对象
        print dbh.execute_sql("select start,end from app_salon where id = 7492")[0][1].time()

        #print dbh.execute_sql("select p_joined,id from app_salon where id = 7495")# [0][0]=="读书会选书讨论"
        #print dbh.execute_sql("select from_user_id,to_user_id from app_user_followings where from_user_id < 100")
    finally:
        dbh.dbclose()

def  myplot():
    import numpy as np
    #import matplotlib as mpl
    #mpl.use('Agg')
    import matplotlib.pyplot as plt

    x = np.arange(9)
    y = np.sin(x)
    z = np.cos(x)
    # marker数据点样式，linewidth线宽，linestyle线型样式，color颜色
    plt.plot(x, y, marker="*", linewidth=3, linestyle="--", color="orange")
    plt.plot(x, z)
    plt.title("matplotlib")
    plt.xlabel("height")
    plt.ylabel("width")
    # 设置图例
    plt.legend(["Y", "Z"], loc="upper right")
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
