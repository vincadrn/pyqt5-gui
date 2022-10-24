import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.uic import loadUi
from main_gui import Ui_MainWindow
import activity_cv

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import db
import json
from datetime import datetime

""" Backend """
cred = credentials.Certificate(r"pyqt5-gui-firebase-adminsdk-rohct-d8177f166d.json")
with open(r"pyqt5-gui-pyrebase-config.json") as f:
    config = json.load(f)
with open(r"pyqt5-gui-firebase-db-options.json") as f:
    options = json.load(f)
    firebase_admin.initialize_app(cred, options)
auth = pyrebase.initialize_app(config).auth()

""" GUI """
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class LoginPage(QDialog):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi("login_page.ui", self)
        self.line_email.returnPressed.connect(self.go_to_mainwindow)
        self.line_password.returnPressed.connect(self.go_to_mainwindow)
        self.button_login.clicked.connect(self.go_to_mainwindow)
        self.button_signup.clicked.connect(self.go_to_signup)
    
    def go_to_mainwindow(self):
        email = self.line_email.text()
        pw = self.line_password.text()
        try:
            auth.sign_in_with_email_and_password(email, pw)
            main_window = widget.widget(widget.currentIndex() + 2)
            main_window.action_signedin.setText("Signed in: " + email)
            main_window.email = email
            self.line_email.clear()
            self.line_password.clear()
            widget.setCurrentIndex(widget.currentIndex() + 2)
        except:
            self.label_confirm.setText("Login invalid!")

    def go_to_signup(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class SignupPage(QDialog):
    def __init__(self):
        super(SignupPage, self).__init__()
        loadUi("signup_page.ui", self)
        self.line_email.returnPressed.connect(self.signup)
        self.line_password.returnPressed.connect(self.signup)
        self.button_signup.clicked.connect(self.signup)
        self.button_back.clicked.connect(self.go_to_login)

    def signup(self):
        email = self.line_email.text()
        pw = self.line_password.text()
        try:
            user = auth.create_user_with_email_and_password(email=email, password=pw)
            self.label_confirm.setText("User with email: {} has been created successfully!".format(user['email']))
        except:
            self.label_confirm.setText("Sign up failed!")
        finally:
            self.line_email.clear()
            self.line_password.clear()
            
    def go_to_login(self):
        self.line_email.clear()
        self.line_password.clear()
        widget.setCurrentIndex(widget.currentIndex() - 1)

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.email = ""
        self.activity_tracker_button.clicked.connect(self.activity_tracker)
        self.sign_language_button.clicked.connect(self.sign_language)

        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.graph_view.addWidget(self.toolbar)
        self.graph_view.addWidget(self.canvas)

    def activity_tracker(self):
        time, number = activity_cv.run()
        self.plot(time, number)
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ref = db.reference("/activity_tracker")
        payload = {
            "user" : self.email,
            "datetime" : now_str,
            "activity_time" : time,
            "activity_number" : number
        }
        payload = json.dumps(payload)
        new_post = ref.push()
        new_post.set(payload)

    def sign_language(self):
        pass # work in progress
    
    def plot(self, x, y):
        self.canvas.axes.cla()
        self.canvas.axes.scatter(x, y)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("CV GUI")
    app.setWindowIcon(QtGui.QIcon("images.jpg"))
    widget = QStackedWidget()
    login_page = LoginPage()
    signup_page = SignupPage()
    widget.addWidget(login_page)
    widget.addWidget(signup_page)

    window = Window()
    widget.addWidget(window)
    widget.show()
    sys.exit(app.exec_())