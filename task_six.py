#encoding:utf8
import networkx as nx
import matplotlib.pyplot as plt
import pickle


class Portrait(object):
    # 人均发起场数
    # 人均参数场数
    # 参与交流的的活动规模图
    # 参与前三的活动所在学院
    # 学院用户followd对象
    # 哪个时段参与的活动最多（上午下午晚上）
    def __init__(self, school=""):
        self.school = school # 标识这个实例指代的是哪个学院的用户
        self.total_people = 1
        self.avg_launch = 0
        self.avg_attend = 0
        self.scale = {}  # key是string,value是int
        self.scale_max = 0 # int
        self.attend_school = {}
        self.follow_school={}
        self.time_interval =[0,0,0]  # 上午 下午 晚上


task_six_results_dir = ".\\task_six_results\\"


def sixsavechinese(name ="", data = {}):
    f = open(task_six_results_dir + name.decode('UTF-8').encode('GBK'),'w')
    pickle.dump(data,f,0)
    f.close()


def sixreadchinese(name=""):
    # f = open(task_six_results_dir + name.decode('UTF-8').encode('GBK'))
    f = open(task_six_results_dir + name)
    r = pickle.load(f)
    f.close()
    return r

def sixanalyze(start,end):
    # datetime..datetime对象
    # 返回0,1,2整型分别代表上午中午晚上
    if start.year != end.year:
        return ''
    if start.month != end.month:
        return ''
    if start.day != end.day:
        return ''
    hour = str(start.time()).split(":")[0]
    if int(hour) <= 12:
        return 0
    if int(hour) <= 18:
        return 1
    if int(hour) <= 24:
        return 2

def task_six_bak(dbh):
    flag_school = "建筑学院"
    launch = 0
    # 计算人均发起场数
    for item in dbh.app_salon_results:
        creator_id = item[2]
        school = dbh.getuserschool(creator_id)
        if school == flag_school:
            launch += 1

    attend = 0
    # 计算人均参与场数
    for item in dbh.app_salonsign_results:
        user_id = item[1]
        school = dbh.getuserschool(user_id)
        if school == flag_school:
            attend += 1
    print "参与场数",attend
    print "发起场数",launch


def task_six(dbh):
    needed_schools = dbh.effectiveschools
    # 统计有用学院的学院总人数（以沙龙注册情况判断）
    total_school_people = {}
    for item in dbh.app_user_results:
        school = dbh.check_merge(item[1])
        if school not in needed_schools:
            continue
        try:
            total_school_people[school] += 1
        except KeyError:
            total_school_people[school] = 1

    dbh.save("total_school_people.pickle", total_school_people)
    raw_input("raw_input END")

    for flag_school in needed_schools:
        tmp = Portrait(flag_school)

        # 得到该学院总人数
        tmp.total_people = total_school_people[school]

        # 计算人均发起场数
        for item in dbh.app_salon_results:
            creator_id = item[2]
            school = dbh.getuserschool(creator_id)
            if school == flag_school:
                tmp.avg_launch += 1
        tmp.avg_launch = tmp.avg_launch #/ tmp.total_people

        # 计算人均参与场数
        for item in dbh.app_salonsign_results:
            user_id = item[1]
            school = dbh.getuserschool(user_id)
            if school == flag_school:
                tmp.avg_attend += 1
        tmp.avg_attend = tmp.avg_attend #/ tmp.total_people

        # 参与交流的规模
        for item in dbh.app_salonsign_results:
            salon_id = item[0]
            user_id = item[1]
            school = dbh.getuserschool(user_id)
            if school == flag_school:
                for item2 in dbh.app_salon_results:
                    id = item2[0]
                    if id == salon_id:
                        p_joined = item2[3]
                        if tmp.scale_max < int(p_joined):
                            tmp.scale_max = int(p_joined)
                        try:
                            tmp.scale[str(p_joined)] += 1
                        except KeyError:
                            tmp.scale[str(p_joined)] = 1
                        break

        # 参与学院排序图
        for item in dbh.app_salonsign_results:
            salon_id = item[0]
            user_id = item[1]
            school = dbh.getuserschool(user_id)
            if school == flag_school:
                for item2 in dbh.app_salon_results:
                    id = item2[0]
                    if id == salon_id:
                        creator_id = item2[2]
                        school = dbh.getuserschool(creator_id)
                        try:
                            tmp.attend_school[school] += 1
                        except KeyError:
                            tmp.attend_school[school] = 1
                        break

        # 学院用户followd对象
        for item in dbh.app_user_followings_results:
            from_user_id = item[0]
            to_user_id = item[1]
            school = dbh.getuserschool(from_user_id)
            if school == flag_school:
                school = dbh.getuserschool(to_user_id)
                try:
                    tmp.follow_school[school] += 1
                except KeyError:
                    tmp.follow_school[school] = 1

        # 时段人数统计 上午下午晚上
        # 测试发现 存在沙龙start end 日期day,mnnth不一致的，这种数据在我们这次的分析不需要所以过滤
        for item in dbh.app_salonsign_results:
            salon_id = item[0]
            user_id = item[1]
            school = dbh.getuserschool(user_id)
            if school == flag_school:
                salon_id_time_result = dbh.execute_sql("select start,end from app_salon "
                                                       "where id = " + str(salon_id))[0]
                start_time = salon_id_time_result[0]
                end_time = salon_id_time_result[1]
                interval = sixanalyze(start_time, end_time)
                if interval != '':
                    tmp.time_interval[interval] += 1


        # 保存对象
        sixsavechinese(tmp.school, tmp)

    # for循环结束，保存任务六涉及的学院
    dbh.save("task_six_needed_school.pickle", needed_schools)


def sixshowlist(L):
    for item in L:
        try:
            print item[0] + ":" + str(item[1]) +"  ",
        except TypeError:
            continue
    print "\n"

def drawscale(school,scale_dict,scale_max,show = 1,id = 1):
    '''
    :param scale_dict:  str:int
    :param scale_max:   int
    :return:
    '''
    X = range(1,scale_max+1)
    Y = []
    for x in X:
        try:
            y = scale_dict[str(x)]
        except KeyError:
            y = 0
        Y.append(y)
    plt.figure(id)
    plt.plot(X, Y, 'r')
    plt.xlabel("活动参与人数")
    plt.ylabel("活动场次")
    plt.title("参与活动规模统计图")
    if show:
        plt.show()
    else:
        plt.savefig(task_six_results_dir + school + ".png")


if __name__ == '__main__':
    # 解决画图出错
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # 打印学院总人数：
    f = open("total_school_people.pickle")
    tsp = pickle.load(f)
    f.close()
    # 排个序
    for item in sorted(tsp.items(),key = lambda x:x[1],reverse = True):
        print '{v}:{k}, '.format(v=item[0], k=item[1]),
    print "\n"
    raw_input("raw_input end")
    needed_schools = []
    with open("task_six_needed_school.pickle",'r') as f:
        needed_schools = pickle.load(f)
    id = 0
    for school in needed_schools:
        tmp = sixreadchinese(school)
        print "-" * 10
        print "[+]学院用户: " ,tmp.school
        print "发起总场数: ",tmp.avg_launch
        print "参与总场数: ",tmp.avg_attend
        print "正在绘制规模图"
        id += 1
        drawscale(tmp.school, tmp.scale, tmp.scale_max, show=0, id = id)
        print "参与的活动所在学院排名: "
        attend_school_list = sorted(tmp.attend_school.items(), key=lambda x: x[1], reverse=True)
        sixshowlist(attend_school_list)
        print "关注的用户所在学院排名: "
        follow_school_list = sorted(tmp.follow_school.items(), key=lambda x: x[1], reverse=True)
        sixshowlist(follow_school_list)
























