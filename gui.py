from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class ProgramCP(QMainWindow):
    def __init__(self) -> None:
        super(ProgramCP, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('cPV - the cP system simulator and verifier')
        self.initUI()
        self.label.setText('cP systems')
        self.label.move(50, 50)
        self.counter = 0
        
        b1 = QtWidgets.QPushButton(self)
        b1.setText('Click')
        b1.clicked.connect(self.xxx)

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
    
    def xxx(self):
        self.counter += 1
        self.label.setText('Hippo!' + ' ' + str(self.counter))
        self.update()
    
    def update(self):
        self.label.adjustSize()
    

def Main():
    app = QApplication(sys.argv)
    prog = ProgramCP()
    prog.show()
    sys.exit(app.exec_())
    
Main()