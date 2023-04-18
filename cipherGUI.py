################################
# File: cipherGUI.py
# Execution Order:
# 1) python -m venv env
# 2) python .\cipherGUI.py
################################

########### LIBRARIES ##########
# Python Libraries
from ast import main
from doctest import debug_script
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
    QGridLayout,
    QRadioButton,
    QFileDialog
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

### VIGENERE FILE MODE ###
class VigenereFileMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Class variables
        self.activeMode = "Encrypt"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.filesLabel = QLabel("Files")
        self.execLabel = QLabel("Execution")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.filesKeyFileLabel = QLabel("Key Path: ")
        self.filesSourceFileLabel = QLabel("Source Path: ")
        self.filesDestFileLabel = QLabel("Dest Path: ")
        self.execSuccessLabel = QLabel("...")

        # Line Edits
        self.inputKeyFile = QLineEdit()
        self.inputSourceFile = QLineEdit()
        self.inputDestFile = QLineEdit()

        # Buttons
        self.btnKeyFile = QPushButton("Browse")
        self.btnSourceFile = QPushButton("Browse")
        self.btnDestFile = QPushButton("Browse")
        self.btnExecute = QPushButton("Begin Vigenere Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel)
        self.paramSubALayout.addWidget(self.btnEncrypt)
        self.paramSubALayout.addWidget(self.btnDecrypt)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel)
        self.filesSubALayout.addWidget(self.inputKeyFile)
        self.filesSubALayout.addWidget(self.btnKeyFile)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel)
        self.filesSubBLayout.addWidget(self.inputSourceFile)
        self.filesSubBLayout.addWidget(self.btnSourceFile)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel)
        self.filesSubCLayout.addWidget(self.inputDestFile)
        self.filesSubCLayout.addWidget(self.btnDestFile)

        self.filesLayout.addWidget(self.filesLabel)
        self.filesLayout.addLayout(self.filesSubALayout)
        self.filesLayout.addLayout(self.filesSubBLayout)
        self.filesLayout.addLayout(self.filesSubCLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.filesLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnKeyFile.clicked.connect(self.openKeyFile)
        self.btnSourceFile.clicked.connect(self.openSourceFile)
        self.btnDestFile.clicked.connect(self.openDestFile)

        self.btnExecute.clicked.connect(self.execCipher)


    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def openKeyFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputKeyFile.setText(filename)

    @Slot()
    def openSourceFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputSourceFile.setText(filename)

    @Slot()
    def openDestFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputDestFile.setText(filename)

    @Slot()
    def execCipher(self):
        options = ["all", "default", "remove", "preserve", 8, "literal"]
        error = 0

        if (self.activeMode == "Encrypt"):
            error = vigenere.vigenere_cipher_encrypt_file(self.inputSourceFile.text(), self.inputKeyFile.text(), self.inputDestFile.text(), options)
        elif (self.activeMode == "Decrypt"):
            error = vigenere.vigenere_cipher_decrypt_file(self.inputSourceFile.text(), self.inputKeyFile.text(), self.inputDestFile.text(), options)
        
        if (error < 0):
            self.execSuccessLabel.setText("Failure Due to Error")
        else:
            self.execSuccessLabel.setText("Success")

### VIGENERE TEXT MODE ###
class VigenereTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        # Class variables
        self.activeMode = "Encrypt"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.filesLabel = QLabel("Files")
        self.execLabel = QLabel("Execution")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.execSuccessLabel = QLabel("...")

        # Line Edits
        self.inputKeyFile = QLineEdit()
        self.inputSourceFile = QLineEdit()
        self.inputDestFile = QLineEdit()

        # Buttons
        self.btnExecute = QPushButton("Begin Vigenere Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel)
        self.paramSubALayout.addWidget(self.btnEncrypt)
        self.paramSubALayout.addWidget(self.btnDecrypt)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        

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

### TRIPLE DES FILEMODE ###
class TripleDESFileMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        # Class variables
        self.activeMode = "Encrypt"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.filesLabel = QLabel("Files")
        self.execLabel = QLabel("Execution")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.filesKeyFileLabel = QLabel("Key Path: ")
        self.filesSourceFileLabel = QLabel("Source Path: ")
        self.filesDestFileLabel = QLabel("Dest Path: ")
        self.execSuccessLabel = QLabel("...")

        # Line Edits
        self.inputKeyFile = QLineEdit()
        self.inputSourceFile = QLineEdit()
        self.inputDestFile = QLineEdit()

        # Buttons
        self.btnKeyFile = QPushButton("Browse")
        self.btnSourceFile = QPushButton("Browse")
        self.btnDestFile = QPushButton("Browse")
        self.btnExecute = QPushButton("Begin Triple DES Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel)
        self.paramSubALayout.addWidget(self.btnEncrypt)
        self.paramSubALayout.addWidget(self.btnDecrypt)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel)
        self.filesSubALayout.addWidget(self.inputKeyFile)
        self.filesSubALayout.addWidget(self.btnKeyFile)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel)
        self.filesSubBLayout.addWidget(self.inputSourceFile)
        self.filesSubBLayout.addWidget(self.btnSourceFile)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel)
        self.filesSubCLayout.addWidget(self.inputDestFile)
        self.filesSubCLayout.addWidget(self.btnDestFile)

        self.filesLayout.addWidget(self.filesLabel)
        self.filesLayout.addLayout(self.filesSubALayout)
        self.filesLayout.addLayout(self.filesSubBLayout)
        self.filesLayout.addLayout(self.filesSubCLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.filesLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnKeyFile.clicked.connect(self.openKeyFile)
        self.btnSourceFile.clicked.connect(self.openSourceFile)
        self.btnDestFile.clicked.connect(self.openDestFile)

        self.btnExecute.clicked.connect(self.execCipher)


    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def openKeyFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputKeyFile.setText(filename)

    @Slot()
    def openSourceFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputSourceFile.setText(filename)

    @Slot()
    def openDestFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputDestFile.setText(filename)

    @Slot()
    def execCipher(self):
        options = ["all", "default", "remove", "preserve", 8, "literal"]
        error = 0

        if (self.activeMode == "Encrypt"):
            print("I am doing Triple DES Encrypt")
        elif (self.activeMode == "Decrypt"):
            print("I am doing Triple DES Decrypt")
        
        if (error < 0):
            self.execSuccessLabel.setText("Failure Due to Error")
        else:
            self.execSuccessLabel.setText("Success")

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
        # Class variables
        self.activeMode = "NULL"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.filesLabel = QLabel("Files")
        self.execLabel = QLabel("Execution")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.filesKeyFileLabel = QLabel("Key Path: ")
        self.filesSourceFileLabel = QLabel("Source Path: ")
        self.filesDestFileLabel = QLabel("Dest Path: ")
        self.execSuccessLabel = QLabel("...")

        # Line Edits
        self.inputKeyFile = QLineEdit()
        self.inputSourceFile = QLineEdit()
        self.inputDestFile = QLineEdit()

        # Buttons
        self.btnKeyFile = QPushButton("Browse")
        self.btnSourceFile = QPushButton("Browse")
        self.btnDestFile = QPushButton("Browse")
        self.btnExecute = QPushButton("Begin AES Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel)
        self.paramSubALayout.addWidget(self.btnEncrypt)
        self.paramSubALayout.addWidget(self.btnDecrypt)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel)
        self.filesSubALayout.addWidget(self.inputKeyFile)
        self.filesSubALayout.addWidget(self.btnKeyFile)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel)
        self.filesSubBLayout.addWidget(self.inputSourceFile)
        self.filesSubBLayout.addWidget(self.btnSourceFile)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel)
        self.filesSubCLayout.addWidget(self.inputDestFile)
        self.filesSubCLayout.addWidget(self.btnDestFile)

        self.filesLayout.addWidget(self.filesLabel)
        self.filesLayout.addLayout(self.filesSubALayout)
        self.filesLayout.addLayout(self.filesSubBLayout)
        self.filesLayout.addLayout(self.filesSubCLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.filesLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnKeyFile.clicked.connect(self.openKeyFile)
        self.btnSourceFile.clicked.connect(self.openSourceFile)
        self.btnDestFile.clicked.connect(self.openDestFile)

        self.btnExecute.clicked.connect(self.execCipher)


    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def openKeyFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputKeyFile.setText(filename)

    @Slot()
    def openSourceFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputSourceFile.setText(filename)

    @Slot()
    def openDestFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputDestFile.setText(filename)

    @Slot()
    def execCipher(self):
        error = 0

        if (self.activeMode == "Encrypt"):
            print("I am doing AES Encrypt")
        elif (self.activeMode == "Decrypt"):
            print("I am doing AES Decrypt")
        
        if (error < 0):
            self.execSuccessLabel.setText("Failure Due to Error")
        else:
            self.execSuccessLabel.setText("Success")

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
        # Class variables
        self.activeMode = "NULL"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.filesLabel = QLabel("Files")
        self.execLabel = QLabel("Execution")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.filesKeyFileLabel = QLabel("Key Path: ")
        self.filesSourceFileLabel = QLabel("Source Path: ")
        self.filesDestFileLabel = QLabel("Dest Path: ")
        self.execSuccessLabel = QLabel("...")

        # Line Edits
        self.inputKeyFile = QLineEdit()
        self.inputSourceFile = QLineEdit()
        self.inputDestFile = QLineEdit()

        # Buttons
        self.btnKeyFile = QPushButton("Browse")
        self.btnSourceFile = QPushButton("Browse")
        self.btnDestFile = QPushButton("Browse")
        self.btnExecute = QPushButton("Begin RSA Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel)
        self.paramSubALayout.addWidget(self.btnEncrypt)
        self.paramSubALayout.addWidget(self.btnDecrypt)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel)
        self.filesSubALayout.addWidget(self.inputKeyFile)
        self.filesSubALayout.addWidget(self.btnKeyFile)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel)
        self.filesSubBLayout.addWidget(self.inputSourceFile)
        self.filesSubBLayout.addWidget(self.btnSourceFile)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel)
        self.filesSubCLayout.addWidget(self.inputDestFile)
        self.filesSubCLayout.addWidget(self.btnDestFile)

        self.filesLayout.addWidget(self.filesLabel)
        self.filesLayout.addLayout(self.filesSubALayout)
        self.filesLayout.addLayout(self.filesSubBLayout)
        self.filesLayout.addLayout(self.filesSubCLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.filesLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnKeyFile.clicked.connect(self.openKeyFile)
        self.btnSourceFile.clicked.connect(self.openSourceFile)
        self.btnDestFile.clicked.connect(self.openDestFile)

        self.btnExecute.clicked.connect(self.execCipher)


    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def openKeyFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputKeyFile.setText(filename)

    @Slot()
    def openSourceFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputSourceFile.setText(filename)

    @Slot()
    def openDestFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputDestFile.setText(filename)

    @Slot()
    def execCipher(self):
        
        error = 0

        if (self.activeMode == "Encrypt"):
            print("I am doing RSA Encrypt")
        elif (self.activeMode == "Decrypt"):
            print("I am doing RSA Decrypt")
        
        if (error < 0):
            self.execSuccessLabel.setText("Failure Due to Error")
        else:
            self.execSuccessLabel.setText("Success")

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
    # vigenere.vigenere_cipher_decrypt_file("beemovie.txt", "key.txt", "beedecrypt.txt", ["all", "default", "remove", "preserve", 8, "literal"])
    app = QApplication(sys.argv)

    # QMainWindow with Qt Layout
    widget = MainBodyGUI()
    window = MainGUIWindow(widget)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())