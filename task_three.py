# encoding:utf8
# https://networkx.github.io/documentation/latest/reference/algorithms/generated/networkx.algorithms.community.centrality.girvan_newman.html
import pickle
import sys
import itertools
import networkx as nx

# 解决 UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8 in position
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

def show(tuple_list = ([])):
    for item_list in tuple_list:
        print "[",
        for item in item_list:
            print item,
            print ",",
        print "],"
    print "\n"

def task_three(dbh):
    # 读取taks_one生成的有向权图
    f = open("task_one_D.pickle", 'r')
    D = pickle.load(f)
    f.close()

    print len(D.nodes())

    k = 40
    comp = nx.algorithms.community.centrality.girvan_newman(D)
    for communities in itertools.islice(comp,k):
        show(tuple(sorted(c) for c in communities))

def task_three_with_third_party(dbh):
    # 读取taks_one生成的有向权图
    f = open("task_one_D.pickle", 'r')
    D = pickle.load(f)
    f.close()

    # 建立字符school nodes 和数字的映射关系
    mapped = {}
    remapped = {}
    number = 0
    for node in D.nodes():
        number += 1
        mapped[node] = number
        remapped[number] = node


    # 将有向权图按照cmty.py 指定的格式生成至Girvan-Newman文件夹里面
    f = open(".\\Girvan-Newman\\graph_me.txt",'w')
    for u, v, d in D.edges(data=True):
        w = d['weight']
        f.write(str(mapped[u])+","+str(mapped[v])+","+str(w)+"\n")
    f.close()

    # 保存反映射关系
    f = open(".\\Girvan-Newman\\remapped.pickle", 'w')
    pickle.dump(remapped, f, 0)
    f.close()





if __name__=='__main__':
    # task_three('')
   task_three_with_third_party('')