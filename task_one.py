# encoding:utf8
import networkx as nx
import pickle
import matplotlib.pyplot as plt

## 中文方格子解决办法
# from pylab import *
# mpl.rcParams['font.sans-serif'] = ['SimHei']  # 有效的方法

#使用是否salon tag来确定salon所属学院
usetag = 1  # 必须为1  用于学科内向性
salon_school_dict={}  #salon_school_dict的school都来源于excel文件第一列，人工做过Merge

def task_one(dbh):
    if usetag:
        with open("salon_school_dict.pickle") as f:
            salon_school_dict = pickle.load(f)
        # print salon_school_dict # unicode
    used_node = []
    MG = nx.MultiDiGraph()
    needed_schools = dbh.effectiveschools
    for item in dbh.app_salonsign_results:
        salon_id = item[0]
        user_id = item[1]
        user_school = dbh.getuserschool(user_id)
        if usetag:
            try:
                salon_school = salon_school_dict[str(salon_id)] # str处理很重要
                salon_school = salon_school.strip()
            except KeyError:
                salon_school = ''
        else:
            salon_school = dbh.getsalonschool(salon_id)
        if user_school != "" and salon_school != "" :
            # 是否除去and user_school!=salon_school，在得到需要task_three.py处理的图像时可以加上
            if user_school in needed_schools and salon_school in needed_schools:
                user_school = user_school.strip()
                salon_school = salon_school.strip()
                MG.add_edge(user_school,salon_school,weight = 1)  # 权重影响吗？  # 可能user_school == salon_school
                # 将所有有边的节点放入used_node 里
                if user_school not in used_node:
                    used_node.append(user_school)
                if salon_school not in used_node:
                    used_node.append(salon_school)
            else:
                # print "[Warn]New node is added because of edge : %s to %s" % (user_school,salon_school)
                # D.add_edge(user_school, salon_school)
                continue


    D = nx.DiGraph()
    for u,v,d in MG.edges(data=True):
        w = d['weight']
        if D.has_edge(u,v):
            D[u][v]['weight'] += w
        else:
            D.add_edge(u,v,weight=w)

    # 将图中没有边的点全部去除
    # RuntimeError: dictionary changed size during iteration
    # all_nodes = []
    # for node in D.nodes():
        # all_nodes.append(node)
    # for node in all_nodes: # RuntimeError: dictionary changed size during iteration!!!!
        # if node not in used_node:
            # D.remove_node(node)
            # print "[Not used Node] " + str(node)

    # PageRank 算法
    pr = nx.pagerank(D, alpha=0.85)
    if dbh.debug:
        for node, pageRankValue in pr.items():
            print "%s : %.4f" % (node, pageRankValue)
    else:
        pr_dict = {}
        for node, pageRankValue in pr.items():
            pr_dict[node] = pageRankValue
        pr_list = sorted(pr_dict.items(), key=lambda x: x[1], reverse=True)
        dbh.save("task_one.pickle", pr_list)

    # 将D 和 MG保存
    dbh.save("task_one_D.pickle", D)
    dbh.save("task_one_MG.pickle", MG)

    # 画图
    dbh.figure_id += 1
    plt.figure(dbh.figure_id)
    nx.draw(D, pos=nx.random_layout(D), node_color = 'b', edge_color = "r",
            with_labels=True, font_size=10, node_size=30)
    if dbh.debug:
        plt.show()
    else:
        plt.savefig("task_one.png")


if __name__ == '__main__':
    # 解决画图出错
    import chardet
    import sys,pickle
    reload(sys)
    sys.setdefaultencoding('utf-8')

    f=open("task_one.pickle",'r')
    pr_list = pickle.load(f)
    f.close()
    for item in pr_list:
        print "%s : %.4f" % (item[0],item[1])

    f = open("task_one_D.pickle",'r')
    D = pickle.load(f)
    f.close()

    node_dict = {}
    for node in D.nodes():
        # print node,
        node = node.strip()
        try:
            node_dict[node] += 1
        except KeyError:
            node_dict[node] = 1
        # print chardet.detect(node)
    for key,value in node_dict.items():
        print "%s : %s, " % (key,value),
    print "\n"

    plt.figure(1)
    nx.draw(D, pos=nx.random_layout(D), node_color='b', edge_color="r",
            with_labels=True, font_size=10, node_size=30)
    plt.show()






