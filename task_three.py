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

def task_three(dbh, Graph_pickle):
    # 读取taks_one生成的有向权图
    f = open(Graph_pickle, 'r')
    D = pickle.load(f)
    f.close()

    print len(D.nodes())

    k = 50
    # 这个函数源码
    # https://networkx.github.io/documentation/latest/reference/algorithms/generated/networkx.algorithms.community.centrality.girvan_newman.html
    # 既然要量化我们需要在源码中定位计算的相关变量然后给出来
    comp = nx.algorithms.community.centrality.girvan_newman(D)
    for communities in itertools.islice(comp,k):
        show(tuple(sorted(c) for c in communities))
    # 这里可以绘制一个层次聚类图  类似http://blog.sciencenet.cn/blog-563898-750516.html


def task_three_with_third_party(dbh,Graph_pickle=''):
    # 读取taks_one生成的有向权图
    f = open(Graph_pickle, 'r')
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
    # 下面二种方法区别在于第一个是GN原始算法，第二个引入了Modularity Q
    # 参考http://blog.sciencenet.cn/blog-563898-750516.html
    task_three('',Graph_pickle = "task_one_D.pickle")
    # task_three_with_third_party('',Graph_pickle = "task_one_D.pickle")
