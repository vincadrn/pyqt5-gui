from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
from main_gui import Ui_MainWindow
import sys

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(556, 454)
        self.setWindowIcon(QtGui.QIcon('b914373bef9a5347f6d0e259f10a37e9_400x400.jpeg'))
        self.info_button.clicked.connect(self.on_help_click)
        self.line_edit.setPlaceholderText('e.g. [2, 5, 1], [1, 2]')

    def on_help_click(self):
        QMessageBox.information(
            self,
            "How to Use",
            "Fungsi alih dituliskan dengan format seperti berikut. <br/>"
            "<br/> Contoh: [2, 5, 1], [1, 2]"
            "<br/> berarti (2s^2 + 5s + 1)/(s + 2)"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())