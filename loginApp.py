# import required modules
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import sqlite3


# create  the login widget class - each window must have a class
class Ui(QtWidgets.QMainWindow):
    """Window class based on the xml code in the login ui"""

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("login.ui", self)

        # add event listeners
        self.btnLogin.clicked.connect(self.loginMethod)
        self.btnClear.clicked.connect(self.clearMethod)
        # show the window
        self.show()

    def loginMethod(self):
        """Handle click events on the login button"""
        # access form line edits
        enteredPassword = self.passwordInput.text()
        enteredUsername = self.userNameInput.text()
        # perform validation on the username and password
        if enteredPassword == "" or enteredUsername == "":
            messageBoxHandler(
                "Blank fields detected", "password and username must entered", "warning"
            )
        else:
            # query to check if username exists and password matches
            query = f"""SELECT password FROM users WHERE username =?"""
            data = executeStatementHelper(query, (enteredUsername,))
            try:
                if data[0][0] == enteredPassword:
                    self.clearMethod()
                    messageBoxHandler("Success", "Successfully logged in")
                    self.close()
                    # this is where code for opening another window would come in
                else:
                    messageBoxHandler(
                        "Login attempt failed",
                        "incorrect username or password",
                        "warning",
                    )
            except:
                messageBoxHandler("Login attempt failed", "try again", "warning")
            # print(f"username: {enteredUsername} | Password: {enteredPassword}")

    def clearMethod(self):
        """resets the form fields"""
        self.userNameInput.setText("")
        self.passwordInput.setText("")


def messageBoxHandler(title, message, iconType="info"):
    """This will display a dialog message"""
    msgBox = QtWidgets.QMessageBox()  # message box object
    # set icon type based on the flag
    if iconType == "info":
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
    elif iconType == "question":
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
    elif iconType == "warning":
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    else:
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)

    msgBox.setWindowTitle(title)  # set the title
    msgBox.setText(message)  # sets the content
    msgBox.exec_()  # show the message box


def dbConnector():
    """connects to the database and returns a cursor and connection object"""
    conn = sqlite3.connect("usersAndFilms.db")
    cur = conn.cursor()
    return conn, cur


def executeStatementHelper(query, args=None):
    """connects and executes a give query returning data"""
    conn, cur = dbConnector()
    if not args:
        cur.execute(query)
    else:
        cur.execute(query, args)
    # fetch results
    selectedData = cur.fetchall()
    conn.commit()
    conn.close()
    return selectedData


def mainApplication():
    """Main application load the window instance"""
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())


mainApplication()
