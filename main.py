import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5 import QtGui

import gui_utils

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("control-system-icon-15.jpg"))
    app.setApplicationName("Python GUI Project")
    widget = QStackedWidget()
    auth, db = gui_utils.run_backend()
    login_page = gui_utils.Login(widget, auth, db)
    widget.addWidget(login_page)
    widget.showMaximized()
    sys.exit(app.exec_())