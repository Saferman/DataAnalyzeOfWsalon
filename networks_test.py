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
