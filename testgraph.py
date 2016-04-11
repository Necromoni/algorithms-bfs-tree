import matplotlib.pyplot as plt
import networkx as nx

class TestGraph:
    def __init__(self):
        graph = nx.Graph()
        graph.add_node(0)
        graph.add_node(1)
        
        pos = {0: (0, 0), 1:(5, 3)}
        labels = {0: 'a', 1: 'b'}
        edge_list = [(0,1)]
        edge_labels = {(0, 1): '1'}
        
        nx.draw(graph, pos, node_color='r', node_size=1500)
        nx.draw_networkx_labels(graph, pos, labels, node_color='r')
        nx.draw_networkx_edges(graph, pos, edge_list, width=1, alpha=1.0, edge_color='g')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels)
        plt.grid()
        plt.show()
        return
        