import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import logging
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import imagesqt_rc
from PyQt5 import QtCore
from PyQt5 import QtGui

import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#Logging and console
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class LoginPage(QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi('login.ui', self)
        self.ButtonLogin.clicked.connect(self.selectLevel)
#
# Authenticate Module
#
    def selectLevel(self):
        username = self.user.text()
        password = self.password.text()

        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor1 = conn.cursor()
            cursor1.execute("SELECT * FROM users WHERE authenticate='1'")
            rows = cursor1.fetchall()
            logger.debug("Total Row(s): %s" % cursor1.rowcount)
            if cursor1.rowcount >= 1:
                logger.debug("The user is alredy logged in")

                Q = QMessageBox()
                Q = QMessageBox.information(Q, 'Error',
                                            'The system is already being used.',
                                            QMessageBox.Ok)
                for row in rows:
                    logger.debug("Row: %s" % row)

            else:
                cursor.execute(
                    "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'")
                row = cursor.fetchone()

                if row is not None:
                    logger.debug("User Level: %s" % row[3])

                    def level1():
                        logger.debug("Hi level 1")
                        if row[4] == 1:
                            logger.debug("The user is alredy logged in: %s" % row[1])
                            Q = QMessageBox()
                            Q = QMessageBox.information(Q, 'Error',
                                                        'The system is already being used.',
                                                        QMessageBox.Ok)
                        else:
                            query = """ UPDATE users SET authenticate = %s WHERE id = %s """
                            data = (1, row[0])
                            try:
                                # User update
                                cursor = conn.cursor()
                                cursor.execute(query, data)
                                # Commit
                                conn.commit()
                            except Error as error:
                                logger.exception("Level 1 Error: %s" % error)
                            finally:
                                cursor.close()
                                conn.close()
                            # self.hide()
                            self.levelOne()
                            # anotherwin = winlevel1(self)
                            # anotherwin.show()

                    def level2():
                        logger.debug("Hi level 2:")
                        if row[4] == 1:
                            logger.debug("The user is alredy logged in: %s" % row[1])
                            Q = QMessageBox()
                            Q = QMessageBox.information(Q, 'Error',
                                                        'The system is already being used.',
                                                        QMessageBox.Ok)
                        else:
                            query = """ UPDATE users SET authenticate = %s WHERE id = %s """
                            data = (1, row[0])
                            try:
                                # User update
                                cursor = conn.cursor()
                                cursor.execute(query, data)
                                # Commit
                                conn.commit()
                            except Error as error:
                                logger.exception("Level 2 Error: %s" % error)
                            finally:
                                cursor.close()
                                conn.close()
                            self.levelTwo()
                            # self.hide()
                            # anotherwin = winlevel2(self)
                            # anotherwin.show()

                    def level3():

                        if row[4] == 1:
                            logger.debug("The user is alredy logged in: %s" % row[1])
                            Q = QMessageBox()
                            Q = QMessageBox.information(Q, 'Error',
                                                        'The system is already being used.',
                                                        QMessageBox.Ok)
                        else:
                            query = """ UPDATE users SET authenticate = %s WHERE id = %s """
                            data = (1, row[0])
                            try:
                                # User update
                                cursor = conn.cursor()
                                cursor.execute(query, data)
                                # Commit
                                conn.commit()
                            except Error as error:
                                logger.exception("Level 3 Error: %s" % error)
                            finally:
                                cursor.close()
                                conn.close()
                            self.levelThree()
                            # self.hide()
                            # anotherwin = winlevel3(self)
                            # anotherwin.show()

                    # Python switch
                    level = row[3]
                    options = {1: level1,
                               2: level2,
                               3: level3,
                               }
                    options[level]()

                else:
                    logger.debug("User or password incorrect/empty")
                    Q = QMessageBox()
                    Q = QMessageBox.information(Q, 'Error',
                                                'User or password incorrect/empty.',
                                                QMessageBox.Ok)

        except Error as e:
            logger.exception("Authenticated Error DB: %s" % e)

        finally:
            cursor.close()
            conn.close()

    def levelOne(self):
        logger.debug("Level One")
        self.hide()
        from levelOne import levelOne
        goto = levelOne()
        goto.exec_()
        # pass

    def levelTwo(self):
        logger.debug("Level Two")
        self.hide()
        from levelTwo import levelTwo
        goto = levelTwo()
        goto.exec_()
        # pass

    def levelThree(self):
        logger.debug("Level Three")
        self.hide()
        from levelThree import levelThree
        goto = levelThree()
        goto.exec_()
        pass


#
# End Module Log in
#


app = QApplication(sys.argv)
app_icon = QtGui.QIcon()
app_icon.addFile('icons/16x16.png', QtCore.QSize(16, 16))
app_icon.addFile('icons/24x24.png', QtCore.QSize(24, 24))
app_icon.addFile('icons/32x32.png', QtCore.QSize(32, 32))
app_icon.addFile('icons/48x48.png', QtCore.QSize(48, 48))
app_icon.addFile('icons/256x256.png', QtCore.QSize(256, 256))
app.setWindowIcon(app_icon)
main = LoginPage()
main.show()
sys.exit(app.exec_())