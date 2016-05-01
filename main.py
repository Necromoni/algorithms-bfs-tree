from gcanvas import GraphingCanvas
from atable import AdjacencyTable
from PyQt4 import QtGui, QtCore
from tree import GraphTree
import constants
import sys
import string


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
        self.menu_bar = QtGui.QMenuBar()
        self.mw.setMenuBar(self.menu_bar)
        
        # Create the drop down menus for the menu bar
        self.app_menu = QtGui.QMenu('&App', self.mw)
        self.app_menu.addAction('&Animate', self.animate)
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
        self.central_layout = QtGui.QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.mw.setCentralWidget(self.central_widget)

        # L and R layouts
        self.right_layout = QtGui.QVBoxLayout()
        self.left_layout = QtGui.QVBoxLayout()
        self.central_layout.addLayout(self.left_layout)
        self.central_layout.addLayout(self.right_layout)

        # Create the graphing canvas; parent it to the central widget's layout
        self.graph = GraphingCanvas()
        self.left_layout.addWidget(self.graph)
        self.graph.setMinimumSize(400, 400)

        # Create the center layout; parent to the central widget's layout

        self.c_layout = QtGui.QHBoxLayout()
        self.left_layout.addLayout(self.c_layout)

        # Create the Queue View
        self.queue_layout = QtGui.QVBoxLayout()
        self.c_layout.addLayout(self.queue_layout)
        self.queue_title = QtGui.QLabel('Queue:')
        self.queue_title.setAlignment(QtCore.Qt.AlignLeft)
        self.queue_layout.addWidget(self.queue_title)
        self.queue_view = QtGui.QLabel('No Queue')
        self.queue_layout.addWidget(self.queue_view)
        self.graph.set_queue_view(self.queue_view)

        # Create the Tree View
        self.tree_view = QtGui.QLabel('No Tree')
        self.tree_view.setMinimumSize(constants.window_size[0] / 2, constants.window_size[1])
        self.tree_drawer = GraphTree(self.tree_view)
        self.graph.set_tree_drawer(self.tree_drawer)

        # Create the bottom left layout; parent to the central widget's layout
        self.bottom_left_layout = QtGui.QHBoxLayout()
        self.left_layout.addLayout(self.bottom_left_layout)

        
        # Create the adjacency table
        self.adjacency_layout = QtGui.QVBoxLayout()
        self.bottom_left_layout.addLayout(self.adjacency_layout)
        self.adjacency_title = QtGui.QLabel('Adjacency Table')
        self.adjacency_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.adjacency_layout.addWidget(self.adjacency_title)
        self.adjacency_table = AdjacencyTable(self.mw)
        self.adjacency_table.setMaximumSize(300, 300)
        self.adjacency_layout.addWidget(self.adjacency_table)

        # List of points
        self.points_layout = QtGui.QVBoxLayout()
        self.bottom_left_layout.addLayout(self.points_layout)
        self.points_title = QtGui.QLabel('List of Points')
        self.points_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.points_layout.addWidget(self.points_title)
        self.points_view = QtGui.QTextEdit()
        self.points_view.setMaximumSize(300, 300)
        self.points_layout.addWidget(self.points_view)
        
        # Tree View
        self.tree_layout = QtGui.QVBoxLayout()
        self.right_layout.addLayout(self.tree_layout)
        self.tree_title = QtGui.QLabel('Tree')
        self.tree_title.setAlignment(QtCore.Qt.AlignHCenter)
        self.tree_layout.addWidget(self.tree_title)
        self.tree_layout.addWidget(self.tree_view)
        
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
        self.points_view.setText(QtCore.QString('\n'.join(contents)))
    
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

    def animate(self):
        # Init
        dialog = QtGui.QDialog()
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Number Selector
        number_selector_title = QtGui.QLabel('Start Point (Blank for 0):')
        number_selector = QtGui.QLineEdit()
        number_selector.setMaxLength(1)
        number_selector_title_2 = QtGui.QLabel('End Point (Blank for last):')
        number_selector_2 = QtGui.QLineEdit()
        number_selector_2.setMaxLength(1)

        def handleButtonClicked():
            input = str(number_selector.text()).strip(' \t\n\r')
            input2 = str(number_selector_2.text()).strip(' \t\n\r')
            if input == '':
                input = 'a'
            if input2 == '':
                input2 = None
            else:
                input2 = input2.lower()
                if input2 in string.ascii_letters:
                    input2 = string.ascii_lowercase.index(input2)
                else:
                    input2 = int(input2)

            input = input.lower()

            if input in string.ascii_letters:
                input = string.ascii_lowercase.index(input)
            else:
                input = int(input)

            dialog.close()
            self.graph.animate_bfs(input, input2)


        # OK Button
        ok_button = QtGui.QPushButton()
        ok_button.setText('OK')
        ok_button.connect(ok_button, QtCore.SIGNAL('clicked()'), handleButtonClicked)

        # Layout
        dialog_layout = QtGui.QVBoxLayout()
        dialog.setLayout(dialog_layout)
        dialog_layout.addWidget(number_selector_title)
        dialog_layout.addWidget(number_selector)
        dialog_layout.addWidget(number_selector_title_2)
        dialog_layout.addWidget(number_selector_2)
        dialog_layout.addWidget(ok_button)

        dialog.exec_()


# Runs main when script is run; calling __init__
main()