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
        # print w'
        if w >= 1.0:
            f.write(str(mapped[u]) + "," + str(mapped[v]) + "," + str(w) + "\n")
    f.close()

    # 将有向权图按照cmty.py 指定的格式（数字替换成school）生成至Girvan-Newman文件夹里面
    f = open("..\\Girvan-Newman\\graph_me_school.txt", 'w')
    for u, v, d in D.edges(data=True):
        w = d['weight']
        # print w
        if w < 0.1:
            D.remove_edge(u,v)
        else:
            f.write(u + "," + v + "," + str(w) + "\n")
    f.close()
    plt.figure(1)
    nx.draw(D,  node_color='b', edge_color="r",
            with_labels=True, font_size=8, node_size=30)
    plt.show()

    # 保存处理过后的D：
    f = open("preprocess.pickle","w")
    pickle.dump(D,f,0)
    f.close()


    # 保存反映射关系
    f = open("..\\Girvan-Newman\\remapped.pickle", 'w')
    pickle.dump(remapped, f, 0)
    f.close()


if __name__ == '__main__':
    # 0 次数归一化的图pickle  1 不归一化的图pickle  2人数归一化的pickle
    # 次数归一化过滤 w < 0.1，人数归一化 w <1.0
    preprocess(seq=0)

