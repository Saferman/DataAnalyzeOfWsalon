#encoding:utf8
import networkx as nx
import matplotlib.pyplot as plt

def task_five(dbh):
    D = nx.DiGraph()
    for node in dbh.schools:
        D.add_node(node)
    for item in dbh.app_salonsign_results:
        salon_id = item[0]
        user_id = item[1]
        user_school = dbh.getuserschool(user_id)
        salon_school = dbh.getsalonschool(salon_id)
        if user_school != "" and salon_school != "":
            D.add_edge(user_school,salon_school)

    pr = nx.pagerank(D, alpha=0.85)
    # 在console输出结果
    for node,pageRankValue in pr.items():
        print "%s : %.4f" % (node, pageRankValue)
    # 画图
    plt.figure(1)
    nx.draw(D)
    plt.savefig("task_one.png")
    plt.show()





