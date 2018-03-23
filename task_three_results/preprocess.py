# encoding:utf8
import networkx as nx
import pickle
import matplotlib.pyplot as plt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def preprocess(seq = 1):
    files =["count-normalization.pickle","non-normalization.pickle","people-normalization.pickle"]
    with open(files[seq],"r") as f:
        D = pickle.load(f)
    # 建立字符school nodes 和数字的映射关系
    mapped = {}
    remapped = {}
    number = 0
    for node in D.nodes():
        number += 1
        mapped[node] = number
        remapped[number] = node

    a = 1
    # 将有向权图按照cmty.py 指定的格式生成至Girvan-Newman文件夹里面
    f = open("..\\Girvan-Newman\\graph_me.txt", 'w')
    for u, v, d in D.edges(data=True):
        w = d['weight']
        # print w
        f.write(str(mapped[u]) + "," + str(mapped[v]) + "," + str(w) + "\n")
    f.close()

    # 将有向权图按照cmty.py 指定的格式生成至Girvan-Newman文件夹里面
    f = open("..\\Girvan-Newman\\graph_me_school.txt", 'w')
    for u, v, d in D.edges(data=True):
        w = d['weight']
        # print w
        f.write(u + "," + v + "," + str(w) + "\n")
    f.close()

    # 保存反映射关系
    f = open("..\\Girvan-Newman\\remapped.pickle", 'w')
    pickle.dump(remapped, f, 0)
    f.close()


if __name__ =='__main__':
    preprocess(seq=1)

