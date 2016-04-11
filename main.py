from gcanvas import GraphingCanvas
from atable import AdjacencyTable
from PyQt4 import QtGui, QtCore
import constants
import sys

class main:
    def __init__(self):
        # Runs when the program starts
        
        # Initialize the Qt Application
        self.app = QtGui.QApplication(sys.argv)
        
        # Create the QMainWindow
        self.mw = QtGui.QMainWindow()
        self.mw.resize(*constants.window_size)
        self.mw.setWindowTitle(constants.window_title)
        self.mw.show()
        
        # Create the menu bar for drop downs
        self.menu_bar = QtGui.QMenuBar(parent=self.mw)
        self.mw.setMenuBar(self.menu_bar)
        
        # Create the drop down menus for the menu bar
        self.app_menu = QtGui.QMenu('&App', self.mw)
        self.app_menu.addAction('&Reset', self.reset, QtCore.Qt.Key_F2)
        self.app_menu.addSeparator()
        self.app_menu.addAction('&Exit', QtGui.QApplication.quit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menu_bar.addMenu(self.app_menu)
        
        self.load_menu = QtGui.QMenu('&Load', self.mw)
        self.load_menu.addAction('&Point File', self.clicked_load_points, QtCore.Qt.ALT + QtCore.Qt.Key_P)
        self.load_menu.addAction('&Adjacency Matrix', self.clicked_load_adjacency_matrix, QtCore.Qt.ALT + QtCore.Qt.Key_M)        
        self.menu_bar.addMenu(self.load_menu)
        
        self.help_menu = QtGui.QMenu('&Help', self.mw)
        self.help_menu.addAction('&About', self.clicked_about)
        self.help_menu.addAction('About &Qt', self.clicked_about)
        self.menu_bar.addMenu(self.help_menu)
        
        # Create the central widget; simply a widget to parent other widgets to
        self.central_widget = QtGui.QWidget(self.mw)
        self.central_layout = QtGui.QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.mw.setCentralWidget(self.central_widget)
        
        # Create the graphing canvas; parent it to the central widget's layout
        self.graph = GraphingCanvas()
        self.central_layout.addWidget(self.graph)
        
        # Create the bottom layout; parent to the central widget's layout
        self.bottom_layout = QtGui.QHBoxLayout()
        self.central_layout.addLayout(self.bottom_layout)
        
        # Create the adjacency table
        self.adjacency_layout = QtGui.QVBoxLayout()
        self.bottom_layout.addLayout(self.adjacency_layout)
        self.adjacency_title = QtGui.QLabel('Adjacency Table')
        self.adjacency_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.adjacency_layout.addWidget(self.adjacency_title)
        self.adjacency_table = AdjacencyTable(self.mw)
        self.adjacency_layout.addWidget(self.adjacency_table)
        
        # Create the queue viewer and put it in the bottom layout
        self.bfs_layout = QtGui.QVBoxLayout()
        self.bottom_layout.addLayout(self.bfs_layout)
        self.bfs_title = QtGui.QLabel('BFS Queue')
        self.bfs_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.bfs_layout.addWidget(self.bfs_title)
        self.bfs_table = AdjacencyTable(self.mw)
        self.bfs_layout.addWidget(self.bfs_table)
        
        self.points = None
        self.edges = None
        sys.exit(self.app.exec_())

    def clicked_load_adjacency_matrix(self):
        # Get the file we want to load
        fileName = QtGui.QFileDialog.getOpenFileName(self.mw, 'Select the Adjacency Matrix to load', QtCore.QDir.home().absolutePath(), 'Text Files (*.txt)')
        try:
            f = open(fileName, 'r')
        except (IOError) as e:
            print('Error opening file. ' + e.message)
            return
        import string
        # Remove all weird characters from file
        contents = filter(lambda x: x in string.printable, f.read()).split('\n')
        # Load the contents in the adjacency table
        self.adjacency_table.load_matrix(contents)
        # Load the contents into the graph
        self.load_graph(edges=contents)
        self.mw.statusBar().showMessage('Loaded Adjacency Matrix', 5000)
    
    def clicked_load_points(self):
        # Get the file we want to load
        fileName = QtGui.QFileDialog.getOpenFileName(self.mw, 'Select the Point List to load', QtCore.QDir.home().absolutePath(), 'Text Files (*.txt)')
        try:
            f = open(fileName, 'r')
        except (IOError) as e:
            print('Error opening file. ' + e.message)
            return
        import string
        # Remove all weird characters from file
        contents = filter(lambda x: x in string.printable, f.read()).split('\n')
        # Load the contents into the graph
        self.graph.load_points(contents)
    
    def reset(self):
        # TODO: clear table
        self.graph.clear()
        
    def clicked_about(self):
        QtGui.QMessageBox.about(self.mw, constants.about_title, constants.about_message)
    
    def load_graph(self, points=None, edges=None):
        if self.points and self.edges:
            self.reset()
        if points is not None:
            self.points = points
            self.graph.load_points(self.points)
        if edges is not None:
            self.edges = edges
            self.graph.load_edges(self.edges)


# Runs main when script is run; calling __init__
main()