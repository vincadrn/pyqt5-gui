import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.uic import loadUi
from interface import Ui_MainWindow
import misc
import activity_cv

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import firestore
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
db = firestore.client()

""" GUI """
class Login(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        loadUi("loginpage.ui", self)
        self.stackedWidget_welcome.setCurrentWidget(self.login_page)
        self.line_email_signup.returnPressed.connect(self.signup)
        self.line_pw_signup.returnPressed.connect(self.signup)
        self.line_confirm_pw.returnPressed.connect(self.signup)
        self.button_signup.clicked.connect(self.signup)
        self.to_login.clicked.connect(self.go_to_login)
        self.line_email.returnPressed.connect(self.login)
        self.line_pw.returnPressed.connect(self.login)
        self.button_login.clicked.connect(self.login)
        self.to_register.clicked.connect(self.go_to_signup)
        self.checkBox_login.stateChanged.connect(self.login_checkbox_click)
        self.checkBox_signup.stateChanged.connect(self.signup_checkbox_click)
    
    def login_checkbox_click(self):
        if self.checkBox_login.isChecked():
            self.line_pw.setEchoMode(QLineEdit.Normal)
        else:
            self.line_pw.setEchoMode(QLineEdit.Password)
    
    def signup_checkbox_click(self):
        if self.checkBox_signup.isChecked():
            self.line_pw_signup.setEchoMode(QLineEdit.Normal)
            self.line_confirm_pw.setEchoMode(QLineEdit.Normal)
        else:
            self.line_pw_signup.setEchoMode(QLineEdit.Password)
            self.line_confirm_pw.setEchoMode(QLineEdit.Password)
    
    def login(self):
        email = self.line_email.text()
        pw = self.line_pw.text()
        try:
            auth.sign_in_with_email_and_password(email, pw)
            self.line_email.clear()
            self.line_pw.clear()
            main_window = Window(email=email)
            widget.addWidget(main_window)
            widget.setCurrentIndex(1)
            self.label_confirm.setText("")
            self.label_confirm2.setText("")
        except:
            self.label_confirm2.setText("Login invalid!")
    
    def go_to_signup(self):
        self.stackedWidget_welcome.setCurrentWidget(self.register_page)
    
    def signup(self):
        email = self.line_email_signup.text()
        pw = self.line_pw_signup.text()
        confirm_pass = self.line_confirm_pw.text()
        if confirm_pass != pw :
            self.label_confirm.setText("Password does not match!")
        else:
            try:
                user = auth.create_user_with_email_and_password(email=email, password=pw)
                self.label_confirm.setText(misc.conf_msg.format(user['email']))
            except:
                self.label_confirm.setText("Sign up failed!")
            finally:
                self.line_email_signup.clear()
                self.line_pw_signup.clear()
                self.line_confirm_pw.clear()
    
    def go_to_login(self):
        self.stackedWidget_welcome.setCurrentWidget(self.login_page)
        self.line_email.clear()
        self.line_pw.clear()

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, email, parent=None):
        super().__init__(parent)
        loadUi("interface.ui", self)
        self.email = email
        self.stackedWidget_main.setCurrentWidget(self.page_home)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.graph_shop.addWidget(self.toolbar)
        self.graph_shop.addWidget(self.canvas)

        # notification msg setup
        self.label_notification.setText(misc.welcome_message.format(self.email))

        # center menu
        self.center_menu.hide()

        # right menu
        self.right_menu.hide()
        
        # shop activity
        self.shop_start.clicked.connect(self.shop_start_onclick)

        # left menu stackedWidget signals
        self.button_sign.clicked.connect(self.button_sign_onclick)
        self.button_shop.clicked.connect(self.button_shop_onclick)
        self.button_pref.clicked.connect(self.button_pref_onclick)
        self.button_info.clicked.connect(self.button_info_onclick)
        self.button_help.clicked.connect(self.button_help_onclick)
        self.button_center_close.clicked.connect(self.button_center_close_onclick)

        # top/right menu stackedWidget signals
        self.button_account.clicked.connect(self.button_account_onclick)
        self.button_more.clicked.connect(self.button_more_onclick)
        self.button_right_close.clicked.connect(self.button_right_close_onclick)

        # right menu
        self.doc_ref = db.collection(u'activities')
        query = self.doc_ref.where("user", "==", self.email)
        self.signed_in_as.setText(misc.profile_msg.format(self.email))
        self.no_of_usage.setText(misc.usage_msg.format(len(query.get())))

        self.button_signout.clicked.connect(self.button_signout_onclick)
    
    def button_sign_onclick(self):
        self.button_sign.setStyleSheet(misc.button_selected)
        self.button_home.setStyleSheet(misc.button_deselected)
        self.button_shop.setStyleSheet(misc.button_deselected)
        self.stackedWidget_main.setCurrentWidget(self.page_sign)
    
    def button_shop_onclick(self):
        self.button_shop.setStyleSheet(misc.button_selected)
        self.button_sign.setStyleSheet(misc.button_deselected)
        self.button_home.setStyleSheet(misc.button_deselected)
        self.stackedWidget_main.setCurrentWidget(self.page_shop)
    
    def button_pref_onclick(self):
        if not self.center_menu.isVisible():
            self.center_menu.show()
        self.stackedWidget_side.setCurrentWidget(self.page_pref)
        self.button_pref.setStyleSheet(misc.button_selected)
        self.button_help.setStyleSheet(misc.button_deselected)
        self.button_info.setStyleSheet(misc.button_deselected)

    def button_info_onclick(self):
        if not self.center_menu.isVisible():
            self.center_menu.show()
        self.stackedWidget_side.setCurrentWidget(self.page_info)
        self.button_info.setStyleSheet(misc.button_selected)
        self.button_pref.setStyleSheet(misc.button_deselected)
        self.button_help.setStyleSheet(misc.button_deselected)

    def button_help_onclick(self):
        if not self.center_menu.isVisible():
            self.center_menu.show()
        self.stackedWidget_side.setCurrentWidget(self.page_help)
        self.button_help.setStyleSheet(misc.button_selected)
        self.button_info.setStyleSheet(misc.button_deselected)
        self.button_pref.setStyleSheet(misc.button_deselected)
    
    def button_center_close_onclick(self):
        self.center_menu.hide()
        self.button_pref.setStyleSheet(misc.button_deselected)
        self.button_help.setStyleSheet(misc.button_deselected)
        self.button_info.setStyleSheet(misc.button_deselected)

    def button_account_onclick(self):
        self.right_menu.show()
        self.stackedWidget_right.setCurrentWidget(self.page_profile)
    
    def button_more_onclick(self):
        self.right_menu.show()
        self.stackedWidget_right.setCurrentWidget(self.page_more)
    
    def button_signout_onclick(self):
        widget.setCurrentIndex(0)
        widget.removeWidget(widget.widget(1))
    
    def button_right_close_onclick(self):
        self.right_menu.hide()
    
    # shop activity
    def shop_start_onclick(self):
        self.label_notification.setText(misc.activity_start.format(
            datetime.now().strftime("%d %B %Y, %H:%M:%S")
        ))
        time, number = activity_cv.run()
        self.label_notification.setText(misc.activity_end.format(
            datetime.now().strftime("%d %B %Y, %H:%M:%S")
        ))
        self.plot(time, number)
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        payload = {
            "user" : self.email,
            "datetime" : now_str,
            "type" : "shop_analyzer"
        }
        self.doc_ref.add(payload)
    
    def plot(self, x, y):
        self.canvas.axes.cla()
        self.canvas.axes.scatter(x, y)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("control-system-icon-15.jpg"))
    app.setApplicationName("Python GUI")
    widget = QStackedWidget()
    login_page = Login()
    widget.addWidget(login_page)
    widget.show()
    sys.exit(app.exec_())