#encoding:utf8
import networkx as nx
import matplotlib.pyplot as plt

D = nx.DiGraph()
nodes = ["a","b","c"]
for node in nodes:
    D.add_node(node)
D.add_edge("a","b")
all_nodes = []
for node in D.nodes():
    if node=="c":
        all_nodes.append(node)
for node in all_nodes:
    D.remove_node(node)
print D.nodes()

print "[+]Test 2"
g=nx.DiGraph()
g.add_edge('a','b')
g['a']['b']['weight']=1
g.add_edge('b','a')
g['b']['a']['weight']=1
g.add_edge('b','c')
g['b']['c']['weight']=2
g.add_edge('c','a')
g['c']['a']['weight']=3
for u, v, d in g.edges(data=True):
    w = d['weight']
    print u,v,w

