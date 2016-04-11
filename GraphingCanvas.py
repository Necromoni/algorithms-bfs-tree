from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import Globals
import matplotlib.pyplot as plt
import networkx as nx
import string
import random
import numpy as np
import matplotlib.pyplot as plt

class GraphingCanvas(QtGui.QDialog):
    def __init__(self, parent=None):
        super(GraphingCanvas, self).__init__(parent)
        self.points = None
        self.edges = None
        self.pos = {}
        self.labels = {}
        self.edge_list = []
        self.edge_labels = {}
        self.graph = nx.Graph()
        plt.grid()
        plt.clf()
        self.figure = plt.figure()        
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.axes = self.figure.add_subplot(1,1,1)
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.canvas.draw()        
    
    def destroy(self):
        self.layout.removeWidget(self.toolbar)
        self.layout.removeWidget(self.canvas)
        self.layout = None
        self.canvas = None
        self.axes = None
        self.figure = None
    
    def reset_canvas(self):
        self.layout.removeWidget(self.toolbar)
        self.layout.removeWidget(self.canvas)
        self.toolbar = None
        self.canvas = None
        self.axes = None
        self.canvas.draw()
        self.axes = self.figure.add_subplot(1,1,1)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.canvas.draw()
    
    def load_points(self, points):
        '''
        Points Format: ['x, y', 'x, y', 'x, y']
        '''
        self.graph.clear()
        
        self.points = points
        self.pos = {}
        self.labels = {}
        for i, point in enumerate(points):
            self.graph.add_node(i)
            self.pos[i] = (np.array(point.split(',')).astype(np.int))
            self.labels[i] = random.randint(0, 99)
            try:
                self.labels[i] = string.ascii_lowercase[i]
            except IndexError:
                print('Ran out of letters, using random number from 0 to 99 as label')
        
        plt.clf()
        self.axes = self.figure.add_subplot(1,1,1)
        nx.draw(self.graph, self.pos, node_size=Globals.node_size, ax=self.axes)
        nx.draw_networkx_labels(self.graph, self.pos, self.labels, node_color='r', ax=self.axes)
        if self.edges is not None:
            nx.draw_networkx_edges(self.graph, self.pos, self.edge_list, width=1, alpha=1.0, ax=self.axes)
            nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels, ax=self.axes)
        plt.axis('on')
        plt.grid()
        self.figure = plt.figure()
        self.canvas.draw()
        
    def load_edges(self, matrix):
        '''
        matrix format: x*x list of 0s or 1s
        '''
        self.edges = matrix
        self.edge_list = []
        self.edge_labels = {}
        for y, row in enumerate(matrix):
            for i, flag in enumerate(row):
                if int(flag):
                    self.edge_list.append((y, i))
        for i, edge in enumerate(self.edge_list):
            self.edge_labels[edge] = int(i)
        
        print(matrix)
        print(self.edge_list)
        print(self.edge_labels)
        if self.points:
            nx.draw_networkx_edges(self.graph, self.pos, self.edge_list, width=1, alpha=1.0, ax=self.axes)
            nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels, ax=self.axes)
            plt.axis('on')
            plt.grid()
            self.canvas.draw()
    
    def clear(self):
        print('clearing')
        self.reset_canvas()
    
    def draw_with_plot(self):
        nx.draw(self.graph, pos, node_size=Globals.node_size)
        nx.draw_networkx_labels(self.graph, self.pos, self.labels, node_color=Globals.node_color)
        nx.draw_networkx_edges(self.graph, self.pos, self.edge_list, width=1, alpha=1.0, edge_color='g')
        nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels)
        plt.grid()
        plt.show()
