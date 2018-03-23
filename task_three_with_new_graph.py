# encoding:utf8
import pickle
import networkx as nx

task_three_results_dir = ".\\task_three_results\\"

def task_three_with_new_graph(dbh):
    needed_schools = dbh.effectiveschools
    MG = nx.MultiGraph()
    # 使用同一场沙龙的不同学院用户作为连线建立学科间的无向图
    salon_user_dict = {}
    for item in dbh.app_salonsign_results:
        salon_id = str(item[0])
        user_id = str(item[1])
        try:
            salon_user_dict[salon_id].append(user_id)
        except KeyError:
            salon_user_dict[salon_id] = [user_id]
    for key,value in salon_user_dict.items():
        user_id_list = value
        for user_id_A in user_id_list:
            for user_id_B in user_id_list:
                if user_id_A < user_id_B:
                    school_A = dbh.getuserschool(user_id_A)
                    school_B = dbh.getuserschool(user_id_B)
                    if school_A != '' and school_B != '' and school_A != school_B:
                        # 去除school_A == school_B的情况！！
                        if school_A in needed_schools and school_B in needed_schools:
                            school_A = school_A.strip()
                            school_B = school_B.strip()
                            MG.add_edge(school_A,school_B,weight=1)
    #
    D = nx.Graph()
    for u, v, d in MG.edges(data=True):
        w = d['weight']
        if D.has_edge(u, v):
            D[u][v]['weight'] += w
        else:
            D.add_edge(u, v, weight=w)

    # 不归一化
    dbh.save(task_three_results_dir + "non-normalization.pickle",D)

    # 人数归一化
    all_nodes = D.nodes()
    # 统计有用学院的学院总人数（以沙龙注册情况判断）
    total_school_people = {}
    for item in dbh.app_user_results:
        school = item[1]
        school = dbh.check_merge(school)
        if school not in all_nodes:
            continue
        school = school.strip()
        try:
            total_school_people[school] += 1
        except KeyError:
            total_school_people[school] = 1
    for u,v,d in D.edges(data=True):
        w = float(d['weight'])
        p1 = float(total_school_people[u])
        p2 = float(total_school_people[v])
        D[u][v]['weight'] = w/p1 + w/p2
    dbh.save(task_three_results_dir + "people-normalization.pickle", D)

    """
    # 次数归一化
    all_nodes = D.nodes()
    frequency = {}  # school:[发起次数, 被参与次数]
    for school in all_nodes:
        attended = 0
        attend = 0
        for u,v,d in D.edges(data=True):
            w = d['weight']
            if u == school:
                attend += w
            if v == school:
                attended += w
        try:
            frequency[school][0] += attend
            frequency[school][1] += attended
        except KeyError:
            frequency[school] = [attend,attended]
    for u,v,d in D.edges(data = True):
        w = float(d['weight'])
        attend = float(frequency[school][0])
        D[u][v]['weight'] = w/attend
    dbh.save(task_three_results_dir + "count-normalization.pickle", D)
    pass"""

    print "[+]task_three_with_new_graph end!"


if __name__ == '__main__':
    pass