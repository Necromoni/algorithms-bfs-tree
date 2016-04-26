from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import constants
import matplotlib.pyplot as plt
import networkx as nx
import string
import random
import numpy as np
import time


class GraphingCanvas(QtGui.QDialog):
    def __init__(self, parent=None):
        # Initialize the canvas
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
    
    def reset_canvas(self):
        # FIXME: Currently this method doesnt reset the canvas properly

        # Possible fixes: Find a way to reset the canvas | Re-initialize the entire canvas | Restart the program with saved state
        '''
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
        '''
        self.canvas.draw()

    def animate_bfs(self, start_point=0):
        current_point = start_point
        queue = []
        removed_points = []
        edge_list = self.edge_list[:]
        queue.insert(0, current_point)

        def toLetter(number):
            return string.ascii_lowercase[number]

        while current_point != -1:
            current_edges = []
            print('--------------------')
            print('POINT: ', toLetter(current_point))
            print('QUEUE: ', [toLetter(i) for i in queue])
            # Get adjacent edges
            matched_points = []
            crosses = []
            for edge in edge_list:
                if edge[0] != current_point and edge[1] != current_point:
                    # This edge has nothing to do with our current point
                    continue
                elif edge[0] == current_point:
                    # The point on the left is our current point, so the point on the right is adjacent
                    adjacent_point_index = 1
                else:
                    # The point on the right is our current point, so the point on the left is adjacent
                    adjacent_point_index = 0

                # Handle the adjacent point
                adjacent_point = edge[adjacent_point_index]
                if adjacent_point in queue or adjacent_point in removed_points:
                    # This point has been processed before, it is either a cross edge or a parent
                    if adjacent_point not in crosses:
                        print('CROSS: ', toLetter(edge[1]))
                        crosses.append(adjacent_point)
                elif adjacent_point in matched_points:
                    # This point has already been matched with our current_point
                    pass
                else:
                    # This point is adjacent and is not a crossed edge, not a parent, and has not been processed
                    matched_points.append(adjacent_point)
                    current_edges.append((edge, adjacent_point_index))

            if len(current_edges) == 0:
                print('DEAD POINT', toLetter(current_point))
                # There are no adjacent edges, hence this is a leaf or all other nodes have been processed
                # Dequeue
                popped = queue.pop()
                print('DEQUEUE <-', toLetter(popped))
                removed_points.append(popped)
                print('QUEUE', [toLetter(i) for i in queue])

                if len(queue) == 0:
                    # If queue is empty we are done
                    print('EMPTY QUEUE')
                    return
                else:
                    # Get last node in queue, we aren't done yet
                    current_point = queue[-1]
            else:
                # Sort the adjacent edges that we found in descending order by their index
                try:
                    current_edges = sorted(current_edges, key=lambda point: current_edges[1])
                except IndexError as e:
                    print(e.message, current_edges)

                # Enqueue all adjacent nodes which are already in descending order
                for edge, match_index in current_edges:
                    queue.insert(0, edge[match_index])
                    print('ENQUEUE -> ', toLetter(edge[match_index]))
                    try:
                        edge_list.remove(edge)
                    except ValueError as e:
                        print('Failed to remove edge ', toLetter(edge), e.message)

                # Dequeue the parent
                popped = queue.pop()
                removed_points.append(popped)
                print('DEQUEUE <-', toLetter(popped))

                # Get the next starting node
                current_point = queue[-1]
            #time.sleep(1)
    
    def load_points(self, points):
        '''
        Points Format: ['x, y', 'x, y', 'x, y']
        '''
        # If you're loading new points, clear the graph
        self.graph.clear()
        
        # Save the points to data member
        self.points = points
        
        # Reset the position and label dictionaries
        self.pos = {}
        self.labels = {}
        
        # Iterate through the points and add them to the pos and labels dictionaries
        for i, point in enumerate(points):
            self.graph.add_node(i)
            self.pos[i] = (np.array(point.split(',')).astype(np.int))
            try:
                self.labels[i] = string.ascii_lowercase[i]
            except IndexError:
                print('Ran out of letters, using random number from 0 to 99 as label')
                self.labels[i] = random.randint(0, 99)
        
        # Clear the plot... again???
        plt.clf()
        
        # Create a new axes???
        self.axes = self.figure.add_subplot(1, 1, 1)
        
        # Draw the points on the networkx lib
        nx.draw(self.graph, self.pos, node_size=constants.node_size, ax=self.axes)
        nx.draw_networkx_labels(self.graph, self.pos, self.labels, node_color='r', ax=self.axes)
        
        # If we already loaded an adjacency matrix before, then load the edges also
        if self.edges is not None:
            nx.draw_networkx_edges(self.graph, self.pos, self.edge_list, width=1, alpha=1.0, ax=self.axes, edge_color='k')
            nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels, ax=self.axes)
        
        # Set the plot's config to have its axis turned on, and have a grid
        plt.axis('on')
        plt.grid()
        
        # Get the figure from the plot
        self.figure = plt.figure()
        
        # Draw the figure on the canvas
        self.canvas.draw()
        
    def load_edges(self, matrix):
        '''
        matrix format: x*x list of 0s or 1s
        '''
        # Save the edges to data member for checking in load_points
        self.edges = matrix
        
        # Reset the edge list and edge labels
        self.edge_list = []
        self.edge_labels = {}
        
        # Iterate through every row in the matrix given
        for y, row in enumerate(matrix):
            # Iterate through every bit in the row of the matrix
            for i, flag in enumerate(row):
                # If the bit is not a 0 then an edge exists, save the point
                if int(flag):
                    self.edge_list.append((y, i))
        
        # Go through every edge we saved and add labels for them using its index
        for i, edge in enumerate(self.edge_list):
            self.edge_labels[edge] = int(i)
        
        # If we already loaded points before this, draw the edges, the points will already be drawn
        if self.points:
            nx.draw_networkx_edges(self.graph, self.pos, self.edge_list, width=1, alpha=1.0, ax=self.axes)
            nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels, ax=self.axes)
            # Plot configurations
            plt.axis('on')
            plt.grid()
            # Get the figure from the plot
            self.figure = plt.figure()
            # Draw the plot
            self.canvas.draw()

            self.animate_bfs(0)
    
    def clear(self):
        self.reset_canvas()
