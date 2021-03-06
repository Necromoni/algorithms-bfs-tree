from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import constants
import matplotlib.pyplot as plt
import networkx as nx
import string
import random
import numpy as np
import time
import threading


class GraphingCanvas(QtGui.QDialog):
    def __init__(self, parent=None):
        # Initialize the canvas
        super(GraphingCanvas, self).__init__(parent)
        self.red_edges = []
        self.queue_view = None
        self.tree_drawer = None
        self.nodes = []
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

    def colorEdge(self, edge, color, delay=0):
        if color=='red' or color=='r':
            self.red_edges.append(edge)

        time.sleep(delay)
        nx.draw_networkx_edges(self.graph, self.pos, [edge], width=2, alpha=1.0, ax=self.axes, edge_color=color)
        # Draw the figure on the canvas
        self.canvas.draw()

    def colorNode(self, node, color, delay=0):
        time.sleep(delay)
        existing_node = self.labels.get(node)
        if existing_node is None:
            print('Error trying to color node', node)
        else:
            labels = {}
            labels[node] = self.labels[node]
            nx.draw_networkx_labels(self.graph, self.pos, labels, font_size=15, font_color='g', font_weight='bold', ax=self.axes)
            # Draw the figure on the canvas
            self.canvas.draw()

    def set_queue_view(self, queue_view):
        self.queue_view = queue_view

    def set_tree_drawer(self, tree_drawer):
        self.tree_drawer = tree_drawer

    def update_tree_drawer(self, args, delay=0):
        node = args[0]
        parent = args[1]
        time.sleep(delay)
        if node is None:
            return
        self.tree_drawer.add_node(node, parent)

    def update_tree_drawer_edge(self, args, delay=0):
        node = args[0]
        toNode = args[1]
        time.sleep(delay)
        if node is None:
            return
        self.tree_drawer.add_edge(node, toNode)

    def update_queue_view(self, queue, delay=0):
        time.sleep(delay)
        if len(queue) == 0:
            text = 'Empty Queue'
        else:
            text = ''.join([string.ascii_lowercase[i] + ' ---> ' for i in queue if i != queue[-1]])
            text += string.ascii_lowercase[queue[-1]]
        try:
            self.queue_view.setText(text)
        except AttributeError as e:
            print('Queue View not initialized, skipping setting queue view')

    def emit_later(self, emit, args, delay=0):
        time.sleep(delay)
        self.emit(emit, args)

    def animate_bfs(self, start_point=0, end_point=None):
        current_point = start_point
        queue = []
        removed_points = []
        edge_list = self.edge_list[:]
        queue.insert(0, current_point)
        self.update_tree_drawer((current_point, None))
        print('got end point', end_point)

        self.connect(self, QtCore.SIGNAL('add_tree_node(PyQt_PyObject)'), self.update_tree_drawer)
        self.connect(self, QtCore.SIGNAL('add_tree_edge(PyQt_PyObject)'), self.update_tree_drawer_edge)

        def step(current_point, queue, removed_points, edge_list, end_point=None, delay=0, callback=None):
            time.sleep(delay)
            delay = constants.delay

            def toLetter(number):
                return string.ascii_lowercase[number]

            if current_point == -1:
                return

            current_edges = []
            #print('--------------------')
            #print('POINT: ', toLetter(current_point))
            threading._start_new_thread(self.update_queue_view, (queue[:], delay))
            threading._start_new_thread(self.colorNode, (current_point, 'k', delay))
            #print('QUEUE: ', [toLetter(i) for i in queue])
            parent = current_point
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
                    reversed_edge = tuple([i for i in reversed(edge)])
                    if adjacent_point not in crosses and edge not in self.red_edges and reversed_edge not in self.red_edges:
                        delay += constants.delay
                        #print('CROSS: ', toLetter(edge[1]))
                        crosses.append(adjacent_point)
                        threading._start_new_thread(self.colorEdge, (edge, 'yellow', delay))
                        threading._start_new_thread(self.emit_later, (QtCore.SIGNAL('add_tree_edge(PyQt_PyObject)'), (current_point, adjacent_point), delay))

                elif adjacent_point in matched_points:
                    # This point has already been matched with our current_point
                    pass
                else:
                    # This point is adjacent and is not a crossed edge, not a parent, and has not been processed
                    matched_points.append(adjacent_point)
                    current_edges.append((edge, adjacent_point_index))

            if len(current_edges) == 0:
                #print('DEAD POINT', toLetter(current_point))
                # There are no adjacent edges, hence this is a leaf or all other nodes have been processed
                # Dequeue
                popped = queue.pop()
                #print('DEQUEUE <-', toLetter(popped))
                removed_points.append(popped)
                #print('QUEUE', [toLetter(i) for i in queue])
                delay += constants.delay
                threading._start_new_thread(self.update_queue_view, (queue[:], delay))

                if len(queue) == 0:
                    # If queue is empty we are done
                    #print('EMPTY QUEUE')
                    return False
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
                    delay += constants.delay
                    queue.insert(0, edge[match_index])
                    print('ENQUEUE -> ', toLetter(edge[match_index]))
                    # Color the edge red
                    threading._start_new_thread(self.colorEdge, (edge, 'red', delay))
                    threading._start_new_thread(self.update_queue_view, (queue[:], delay))
                    threading._start_new_thread(self.emit_later, (QtCore.SIGNAL('add_tree_node(PyQt_PyObject)'), (edge[match_index], parent), delay))
                    print(edge[match_index], end_point)
                    if (edge[match_index]) == end_point:
                        return
                    try:
                        edge_list.remove(edge)
                    except ValueError as e:
                        print('Failed to remove edge ', toLetter(edge), e.message)

                # Dequeue the parent
                if len(queue) == 0:
                    return
                popped = queue.pop()
                removed_points.append(popped)
                #print('DEQUEUE <-', toLetter(popped))
                delay += constants.delay
                threading._start_new_thread(self.update_queue_view, (queue[:], delay))

                # Get the next starting node
                current_point = queue[-1]
                print(current_point, 'end',  end_point)
                if current_point == end_point:
                    # We're done
                    current_point = -1
                    return
            threading._start_new_thread(step, (current_point, queue, removed_points, edge_list, end_point, delay + constants.delay, callback))

        step(current_point, queue, removed_points, edge_list, end_point=end_point, delay=0)
    
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
        #nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[self.nodes], node_size=constants.node_size, ax=self.axes)

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
    
    def clear(self):
        self.reset_canvas()
