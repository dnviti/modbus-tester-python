import sys
from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Modbus Tester")
        self.setWindowIcon(QtGui.QIcon('modbus.png'))
        self.home()

    def home(self):
        btn = QtGui.QPushButton("Quit")
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        btn.resize(100, 100)
        btn.move(100, 100)

        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


main()
