# encoding:utf8
import sys
import pymysql
import datetime
import pickle
from task_one import task_one
from task_six import task_six
# 使用微软雅黑替换过matplotlib的字体文件

reload(sys)
sys.setdefaultencoding('utf-8')


class DBHandle(object):
    figure_id = 0
    # 得到的类似一个二维数组一维参数是每行结果，二维参数就是列
    app_salon_results = []  # id,title,creator_id,p_joined,start,end
    # 注意start end 是datatime.datetime对象
    app_salonsign_results = [] # salon_id,user_id
    app_user_results = [] #  id,school
    app_user_school_dict = {}  # 可能有school为NULL的情况，索引是ID字符串
    schools = []  # 所有数据库统计出来的学院
    excep = ["档案馆", "保卫部", "信息办", "总务办", "出版社", "基金会", "发展规划处", "劳服办", "无", "工会",
             "信息国家实验室", "北京清华长庚医院", "通力公司", "网络研究院", "正大公司", "艺术博物馆", "发展规划处",
             "国际处", "电教中心", "训练中心", "信息技术中心", "科研院", "组织部", "附中", "网络中心",
             "附小", "文科高研所", "深圳研究生院", "资产处", "宣传部", "党办校办", "技术转移研究院", "学生处",
             "数学科学中心", "教务处", "研究生院", "信研院", "体育部", "建筑技术", "全校", "", "地球科学中心",
             "图书馆", "校医院","计算机", "计算中心","交叉信息院"] # "网络研究院"
    effectiveschools = []

    # 合并的学院名称
    # 每一个子列表所有后面的学院school字符串都会被替换成第一个字符串，这个步骤在所有的查询函数中调用
    # 每个子列表的除第一个字符串均需要写入excep列表里
    merge = [["计算机系", "计算机中心", "计算机"], ["交叉信息研究院", "交叉信息院"]]

    app_user_followings_results = [] # from_user_id,to_user_id

    def __init__(self,host="localhost",user="root",password="new_password",database="wsalon",debug=0):
        db = pymysql.connect(host,user,password,database,charset="utf8")
        self.db = db
        self.getinfo()
        self.debug = debug
        if self.debug:
            print "所有有效学院："
            # 直接打出print self.schools会出现乱码
            for school in self.effectiveschools:
                print school + ", ",
            print "\n"

    def check_merge(self,school):
        for item in self.merge:
            if school in item:
                return item[0]
        return school

    def execute_sql(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def getinfo(self):
        self.app_salon_results=self.execute_sql("select id,title,creator_id,p_joined,start,end from app_salon where id >= 7492")# 过滤测试
        self.app_salonsign_results = self.execute_sql("select salon_id,user_id from app_salonsign")
        self.app_user_results = self.execute_sql("select id,school from app_user where id>= 10252")# 过滤测试
        for row in self.app_user_results:
            id = str(row[0])
            school = row[1]
            try:
                school = school.strip()  # 去除学院二边不可见字符
            except AttributeError:
                pass
            self.app_user_school_dict[id] = school
            if school not in self.schools and school!=None:
                self.schools.append(school)
        self.geteffectiveschool()

        self.app_user_followings_results = self.execute_sql("select from_user_id,to_user_id from app_user_followings "
                                                            "where from_user_id > 10000")


    def getuserschool(self,user_id):
        try:
            school = self.app_user_school_dict[str(user_id)]
            return self.check_merge(school)
        except KeyError:
            print "[Error] can not find userid = " + str(user_id) + " in app_user_school_dict"
            return ""

    def getsalonschool(self,salon_id):
        if 1:
            for item in self.app_salon_results:
                if item[0] == salon_id:
                    create_id = item[2]
                    try:
                        school = self.app_user_school_dict[str(create_id)]
                        return self.check_merge(school)
                    except KeyError:
                        print "[Error] can not find create_id = " + str(create_id) + " in app_user_school_dict",
                        print " from get salonschool where salon_id = " + str(salon_id)
                        return ""

    def geteffectiveschool(self):
        for school in self.schools:
            if school not in self.excep:
                self.effectiveschools.append(school)

    def save(self,filename="",data={}):
        if filename == "":
            filename = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        f = open(filename, 'w')
        pickle.dump(data, f, 0)
        f.close()

    def dbclose(self):
        self.db.close()


def main():
    dbh = DBHandle(debug=0)
    try:
        pass
        task_one(dbh)
        # task_six(dbh)
    finally:
        dbh.dbclose()
        print "[+]End!"



if __name__ == '__main__':
    main()