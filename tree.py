import graphviz as gv
import pydot
import string
from PyQt4 import QtGui, Qt, QtCore


class GraphTree:
    def __init__(self, tree_view, parent=None):
        self.nodes = []
        self.graph = gv.Graph(format='svg')
        self.tree_view = tree_view

    def add_node(self, node, parent_node=None):
        print('add_node', node, parent_node)
        if node not in self.nodes:
            self.nodes.append(node)
            self.graph.node(string.ascii_lowercase[node])
            if parent_node is not None and parent_node in self.nodes:
                self.graph.edge(string.ascii_lowercase[parent_node], string.ascii_lowercase[node])
            self.update_view()

    def add_edge(self, node, toNode):
        print('add_edge', node, toNode)
        if node in self.nodes and toNode in self.nodes:
            self.graph.edge(string.ascii_lowercase[node], string.ascii_lowercase[toNode])
            self.update_view()

    def update_view(self):
        f = open('file.dot', 'w')
        f.write(self.graph.source)
        f.close()
        graph = pydot.graph_from_dot_file('file.dot')
        graph.write_png('file.png')
        #myPixmap = QtGui.QPixmap('file.png')
        #myScaledPixmap = myPixmap.scaled(self.tree_view.size(), QtCore.Qt.KeepAspectRatio)
        self.tree_view.setPixmap(QtGui.QPixmap('file.png'))
