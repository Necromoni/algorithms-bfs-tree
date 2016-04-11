from PyQt4 import QtGui, QtCore
import string

class AdjacencyTable(QtGui.QTableWidget):
    def load_matrix(self, matrix):
        print('Loading Matrix', matrix)
        self.clearContents()
        if len(matrix) > 26:
            headers = [letter + string.ascii_lowercase[len(matrix) - 26] for letter in string.ascii_lowercase[0:len(matrix)]]
        else:
            headers = list(string.ascii_lowercase[0:len(matrix)])
        self.setColumnCount(len(matrix))
        self.setRowCount(len(matrix))
        self.setHorizontalHeaderLabels(headers)
        self.setVerticalHeaderLabels(headers)
        
        for i, row in enumerate(matrix):
            for y, flag in enumerate(row):
                item = QtGui.QTableWidgetItem(flag)
                item.setTextAlignment(QtCore.Qt.AlignHCenter)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, y, item)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setShowGrid(False)