from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import logging
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

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

class levelOne(QDialog):
    def __init__(self, fn=None, parent=None):
        super(levelOne, self).__init__(parent,\
           flags=Qt.WindowMinimizeButtonHint|Qt.WindowMaximizeButtonHint|Qt.WindowCloseButtonHint)
        loadUi('levelOne.ui', self)
        logger.debug("Level One File")
        self.pushButton_Next.clicked.connect(self.goSubWindow)

    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure about exit?",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            logger.debug("Close")
            # Authenticate Update
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE authenticate='1'")
            row = cursor.fetchone()
            query = """ UPDATE users SET authenticate = %s WHERE id = %s """
            data = (0, row[0])
            try:
                # User update
                cursor = conn.cursor()
                cursor.execute(query, data)
                # Commit
                conn.commit()
                self.close()
            except Error as error:
                logger.exception("Error Update User level 1: %s" % error)
            finally:
                cursor.close()
                conn.close()
        else:
            logger.debug("Cancel")
            event.ignore()

    def keyPressEvent(self, event):
        """Close application from escape key.

        results in QMessageBox dialog from closeEvent, good but how/why?
        """
        if event.key() == Qt.Key_Escape:
            logger.debug("Key Scape")
            self.close()

    def goSubWindow(self):
        logger.debug("Go to Sub Level One")
        self.hide()
        value = self.Value.displayText()
        logger.debug("Value is: %s" % value)
        from subLevelOne import subLevelOne
        goto = subLevelOne(value)
        goto.exec_()
        # pass