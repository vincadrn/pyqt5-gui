from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from main_gui import Ui_MainWindow
import sys
from scipy.signal import tf2ss

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(556, 454)
        self.setWindowIcon(QtGui.QIcon('b914373bef9a5347f6d0e259f10a37e9_400x400.jpeg'))
        self.info_button.clicked.connect(self.on_help_click)
        self.num_edit.setPlaceholderText('e.g. 1 2 1')
        self.den_edit.setPlaceholderText('e.g. 1 3 3 4')
        self.ok_button.clicked.connect(self.get_input)
        self.clear_button.clicked.connect(self.clear_input)

    def get_input(self):
        num = [int(n) for n in self.num_edit.text().split(" ")]
        den = [int(n) for n in self.den_edit.text().split(" ")]

        mat_A, mat_B, mat_C, mat_D = tf2ss(num, den)
        print(mat_A, mat_B, mat_C, mat_D)

    def clear_input(self):
        self.num_edit.clear()
        self.den_edit.clear()

    def on_help_click(self):
        QMessageBox.information(
            self,
            "How to Use",
            "Fungsi alih dituliskan dengan format seperti berikut. <br/>"
            "<br/> Contoh: <br/>"
            "Pembilang: 2 5 1 <br/>"
            "Penyebut: 1 2"
            "<br/> berarti (2s^2 + 5s + 1)/(s + 2)"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())