################################
# File: cipherGUI.py
# Execution Order:
# 1) python -m venv env
# 2) python .\cipherGUI.py
################################

########### LIBRARIES ##########
# Python Libraries
from ast import main
import random
import datetime

# PySide6 GUI Libraries
import sys
from tkinter import mainloop
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter, QKeySequence
from PySide6.QtWidgets import (
    QTabWidget,
    QApplication,
    QHeaderView,
    QHBoxLayout,
    QTableWidget,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QDialog,
    QWidget,
    QGridLayout
)

# Cipher Files 
import vigenere

######### MAIN GUI WINDOW ###########
class MainGUIWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)

        # Menu Options
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("File")

        # File Menu: "Exit" option
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.exitApp)
        self.fileMenu.addAction(exitAction)

        # About Menu: "About" option
        self.menu_about = self.menu.addMenu("&About")
        about = QAction("About Qt GUI", self, shortcut=QKeySequence(QKeySequence.HelpContents), triggered=QApplication.aboutQt)
        self.menu_about.addAction(about)

        # Attaches GUI Body to Window
        self.setCentralWidget(widget)

        # Changes Window Title
        self.setWindowTitle("Super Cipher GUI")

    @Slot() 
    def exitApp(self):
        QApplication.quit()

######### CORE GUI BODY ###########
class MainBodyGUI(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        
        # Tab Setup
        tabWidget = QTabWidget()
        tabWidget.addTab(VigenereGUI(self), "Vigenere")
        tabWidget.addTab(TripleDESGUI(self), "Triple Des")
        tabWidget.addTab(AESGUI(self), "AES")
        tabWidget.addTab(RSAGUI(self), "RSA")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)


############ VIGENERE GUI ###########
class VigenereGUI(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        # Tab Setup
        tabWidget = QTabWidget()
        tabWidget.addTab(VigenereFileMode(self), "File Mode")
        tabWidget.addTab(VigenereTextMode(self), "Text Mode")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)

class VigenereFileMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("File Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

class VigenereTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("Text Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

############ TRIPLE DES GUI ###########
class TripleDESGUI(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Tab Setup
        tabWidget = QTabWidget()
        tabWidget.addTab(TripleDESFileMode(self), "File Mode")
        tabWidget.addTab(TripleDESTextMode(self), "Text Mode")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)

class TripleDESFileMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("File Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

class TripleDESTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("Text Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

############ AES GUI ###########
class AESGUI(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Tab Setup
        tabWidget = QTabWidget()
        tabWidget.addTab(AESFileMode(self), "File Mode")
        tabWidget.addTab(AESTextMode(self), "Text Mode")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)

class AESFileMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("File Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

class AESTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("Text Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

############ RSA GUI ###########
class RSAGUI(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        # Tab Setup
        tabWidget = QTabWidget()
        tabWidget.addTab(RSAFileMode(self), "File Mode")
        tabWidget.addTab(RSATextMode(self), "Text Mode")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)

class RSAFileMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("File Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

class RSATextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_name_label = QLabel("Text Mode")

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(file_name_label)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)


############ DEFAULT MAIN PROGRAM ###########
if __name__ == "__main__":
    # Main Qt Application
    app = QApplication(sys.argv)

    # QMainWindow with Qt Layout
    widget = MainBodyGUI()
    window = MainGUIWindow(widget)
    window.resize(1200, 600)
    window.show()

    sys.exit(app.exec())