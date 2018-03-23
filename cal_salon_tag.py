# encoding:utf8
"""
这个脚本有以下二个用处：
> 对tag分类，将对应的tag划分至对应的school
> 根据salon tag标签将对应的salon划分至对应的school
"""
import sys
import xlrd
import pickle
from main import DBHandle

class Classify(DBHandle):

    salon_school_dict = {}  # 都是字符串salon_id 和 school对应
    app_salontag_result = [] # salon_id和tag_id
    app_tag_result = [] # tag_id  name
    app_tag_dict = {} #  将app_tag_result转化成tag_id:name字典
    salon_tag_dict ={}  #  key salon_id字符串  value:tag_id的列表字符串
    department_xlsx = [] # 二维列表，每一个一维列表对应xlsx一行，第一个为学院名称，其余的为学院下的学科

    def __init__(self, DB = 0):
        self.DB = DB  # DB是否初始化父类
        if DB:
            DBHandle.__init__(self)
        self.readexcel()
        self.compare_neededschool()
        print "[+]start to getmoreinfo"
        self.getmoreinfo()
        print "[+]start to classify"
        self.classify()
        self.save("salon_school_dict.pickle", self.salon_school_dict)
        self.save("salon_tag_dict.pickle",self.salon_tag_dict)
        self.save("app_tag_dict.pickle",self.app_tag_dict)

    def check_xlsx(self,tag_name):
        tag_name = tag_name.strip()
        for line in self.department_xlsx:
            school = line[0]
            for i  in xrange(1,len(line)):
                # 包含匹配
                if tag_name in line[i]:
                    return school
        return ''

    def classify(self):
        for key,value in self.salon_tag_dict.items():
            salon_id = str(key)
            tag_id_list = value
            for tag_id in tag_id_list:
                tag_name = self.app_tag_dict[tag_id]
                # 在department_xlsx里面检查
                school = self.check_xlsx(tag_name)
                school = school.strip()
                if school !='':
                    break
            self.salon_school_dict[salon_id] = school



    def readexcel(self, FileName="Department.xlsx"):
        ExcelFile = xlrd.open_workbook(FileName)
        sheet = ExcelFile.sheet_by_index(0) #得到第一个sheet
        # print sheet.name,sheet.nrows,sheet.ncols #  打印sheet的名称，行数，列数
        # rows = sheet.row_values(0)  # 得到第一行，是个列表形式，最后可能会有空u''
        for row in xrange(0,sheet.nrows):
            line = sheet.row_values(row)
            line = [ x for x in line if x!='']
            self.department_xlsx.append(line)

    def compare_neededschool(self):
        if self.DB:
            neededschool = self.effectiveschools
            print "[+]总共地neededschool数量: ", len(neededschool)
            for item in self.department_xlsx:
                school = item[0]
                if school in neededschool:
                    neededschool.remove(school)
                else:
                    pass
                    #print school +" ",
            #print "\n",
            print "[+]Department.xlsx未包含的neededschool数量: ",len(neededschool)
            print "[-]Department.xlsx没有包含的School有: ",
            self.OneListShow(neededschool)

    def OneListShow(self,OneList=[]):
        print"[",
        for i in xrange(0,len(OneList)):
            print OneList[i],
            if i == len(OneList)-1:
                print "]"
            else:
                print", ",


    def getmoreinfo(self):
        self.app_salontag_result = self.execute_sql("select item_id,tag_id from app_salontag where id>=20")
        for item in self.app_salon_results:
            salon_id = str(item[0])
            tag_list = []
            for item2 in self.app_salontag_result:
                salon_id2 = str(item2[0])
                tag_id = str(item2[1])
                if salon_id2 == salon_id:
                    tag_list.append(tag_id)
            self.salon_tag_dict[salon_id] = tag_list

        self.app_tag_result = self.execute_sql("select id,name from app_tag")
        for item in self.app_tag_result:
            tag_id = str(item[0])
            name = item[1]
            self.app_tag_dict[tag_id] = name

def main():
    C = Classify(DB=1)

if __name__ == '__main__':
    # sys.exit(C = Classify(DB = 1))

    with open("salon_school_dict.pickle") as f:
        salon_school_dict = pickle.load(f)
    with open("salon_tag_dict.pickle") as f:
        salon_tag_dict = pickle.load(f)
    with open("app_tag_dict.pickle") as f:
        app_tag_dict = pickle.load(f)
    with open("task_six_needed_school.pickle") as f:
        needed_school = pickle.load(f)

    # 统计与该学院相关的微沙龙场数
    school_saloncount = {}
    for school in needed_school:
        school_saloncount[school] = 1
    for k,v in salon_school_dict.items():
        school = v
        # 排除所有没有school对应的salon活动
        if school == '':
            continue
        try:
            school_saloncount[school] += 1
        except KeyError:
            school_saloncount[school] = 1
    # 排序输出
    for item in sorted(school_saloncount.items(),key = lambda x:x[1],reverse = True):
        school = item[0]
        count = item[1]
        print "%s : %d, " % (school, count),

    sys.exit()

    # 统计有多少沙龙没能匹配到school
    total = 0
    non_school = 0
    for key,value in salon_school_dict.items():
        total +=1
        if value == '':
            non_school += 1
    print "沙龙总场数: %d, 没有匹配到school的沙龙场数: %d" % (total,non_school)
    # 统计salon涉及的tag标签有多少
    tag = []
    for key,value in salon_tag_dict.items():
        for item in value:
            if item not in tag:
                tag.append(item)
    print "[+]所有saln活动涉及标签数量: %d" % (len(tag))

