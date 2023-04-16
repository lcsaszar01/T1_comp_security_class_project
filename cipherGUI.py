################################
# File: cipherGUI.py
# Execution Order:
# 1) python -m venv env
# 2) python .\cipherGUI.py
################################

########### LIBRARIES ##########
# Python Libraries
import random

# PySide6 GUI Libraries
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QWidget
)

# Cipher Files 
import vigenere

############ GUI INTERFACE ###########
class CipherGUI(QWidget):
    ############ MAIN ############
    def __init__(self):
        QWidget.__init__(self)

        ############ LAYOUT ############
        # Left Objects 
        self.key = QLineEdit()
        self.inputText = QLineEdit()
        self.quit = QPushButton("Quit")

        # Left Layout
        self.left = QVBoxLayout()
        self.left.addWidget(QLabel("Cipher"))
        self.left.addWidget(QLabel("Cipher Mode"))
        self.left.addWidget(QLabel("Cipher Key(s)"))
        self.left.addWidget(self.key)
        self.left.addWidget(QLabel("Plaintext/Ciphertext"))
        self.left.addWidget(self.inputText)
        self.left.addWidget(self.quit)
        

        # Right Layout
        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Description"))

        # QWidgetLayout
        self.layout = QHBoxLayout()

        # Organize Left and Right Layouts
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)

        # Set layout for the widget
        self.setLayout(self.layout)

        ############ SIGNALS & EVENTS ############
        self.quit.clicked.connect(self.quitApp)

        ######## SELF-INVOKING FUNCTIONS #########

    ###### CALLBACK FUNCTIONS ######

    @Slot()
    def quitApp(self):
        QApplication.quit()

######### MAIN GUI WINDOW ###########
class MainGUIWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Cipher GUI")

        # Menu Options
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("File")

        # Exit QAction (clean exit)
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.exitApp)

        # Default Menu Actions
        self.fileMenu.addAction(exitAction)
        self.setCentralWidget(widget)

    ###### CALLBACK FUNCTIONS ######
    @Slot()
    def exitApp(self, checked):
        QApplication.quit()

############ DEFAULT MAIN PROGRAM ###########
if __name__ == "__main__":
    # Main Qt Application
    app = QApplication(sys.argv)

    # QWidget (contains entire interface)
    widget = CipherGUI()

    # QMainWindow with Qt Layout
    window = MainGUIWindow(widget)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())