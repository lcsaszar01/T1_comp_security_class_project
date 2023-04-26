################################ 
# File: cipherGUI.py
# Execution Order:
# 1) python -m venv env
# 2) python .\cipherGUI.py
################################

########### LIBRARIES ########## --------------------------------------------------------------------------
# Python Libraries
from ast import Try
from threading import Timer
from timeit import default_timer as timer

# PySide6 GUI Libraries
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QTabWidget,
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QWidget,
    QRadioButton,
    QFileDialog,
    QButtonGroup
)

# Cipher Files 
import vigenere
import aes
import rsa
import triple_des


######### MAIN GUI WINDOW ########### --------------------------------------------------------------------------
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

######### CORE GUI BODY ########### --------------------------------------------------------------------------
class MainBodyGUI(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        
        # Tab Setup
        tabWidget = QTabWidget()
        tabWidget.addTab(VigenereGUI(self), "Vigenere")
        tabWidget.addTab(TripleDESGUI(self), "Triple DES")
        tabWidget.addTab(AESGUI(self), "AES")
        tabWidget.addTab(RSAGUI(self), "RSA")

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)


############ VIGENERE GUI ########### --------------------------------------------------------------------------
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
        self.activeMode = "NULL"
        self.alphabetMode = "NULL"
        self.conversionMode = "NULL"
        self.complianceMode = "NULL"
        self.whitespaceMode = "NULL"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.filesLabel = QLabel("Files")
        self.execLabel = QLabel("Execution")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.paramOption0Label = QLabel("Characters: ")
        self.paramOption1Label = QLabel("Letter Case:\n(Only affects 'Letters' option) ")
        self.paramOption2Label = QLabel("Non-compliant Symbols: ")
        self.paramOption5Label = QLabel("Whitespace: ")
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
        self.modeGroup = QButtonGroup()
        self.modeGroup.addButton(self.btnEncrypt)
        self.modeGroup.addButton(self.btnDecrypt)
        
        self.btnStandard = QRadioButton("Letters\n(AaBb)")
        self.btnAlphaNum = QRadioButton("Alphanumeric\n(AaBb0123)")
        self.btnASCII = QRadioButton("All Printable Symbols\n(AaBb0123$@%)")

        self.options0Group = QButtonGroup()
        self.options0Group.addButton(self.btnStandard)
        self.options0Group.addButton(self.btnAlphaNum)
        self.options0Group.addButton(self.btnASCII)

        self.btnLowerCase = QRadioButton("Lowercase (ab)")
        self.btnUpperCase = QRadioButton("Uppercase (AB)")
        self.btnDefaultCase = QRadioButton("Default (AaBb)")

        self.options1Group = QButtonGroup()
        self.options1Group.addButton(self.btnLowerCase)
        self.options1Group.addButton(self.btnUpperCase)
        self.options1Group.addButton(self.btnDefaultCase)

        self.btnIgnoreS = QRadioButton("Ignore Symbols")
        self.btnRemoveS = QRadioButton("Remove Symbols")

        self.options2Group = QButtonGroup()
        self.options2Group.addButton(self.btnIgnoreS)
        self.options2Group.addButton(self.btnRemoveS)

        self.btnLiteralW = QRadioButton("Keep Whitespace")
        self.btnIgnoreW = QRadioButton("Ignore Whitespace")

        self.options5Group = QButtonGroup()
        self.options5Group.addButton(self.btnLiteralW)
        self.options5Group.addButton(self.btnIgnoreW)

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramSubBLayout = QHBoxLayout()
        self.paramSubBLayout.addWidget(self.paramOption0Label, 1)
        self.paramSubBLayout.addWidget(self.btnASCII, 1)
        self.paramSubBLayout.addWidget(self.btnAlphaNum, 1)
        self.paramSubBLayout.addWidget(self.btnStandard, 1)


        self.paramSubCLayout = QHBoxLayout()
        self.paramSubCLayout.addWidget(self.paramOption1Label, 1)
        self.paramSubCLayout.addWidget(self.btnDefaultCase, 1)
        self.paramSubCLayout.addWidget(self.btnLowerCase, 1)
        self.paramSubCLayout.addWidget(self.btnUpperCase, 1)

        self.paramSubDLayout = QHBoxLayout()
        self.paramSubDLayout.addWidget(self.paramOption2Label, 1)
        self.paramSubDLayout.addWidget(self.btnRemoveS, 1)
        self.paramSubDLayout.addWidget(self.btnIgnoreS, 2)

        self.paramSubGLayout = QHBoxLayout()
        self.paramSubGLayout.addWidget(self.paramOption5Label, 1)
        self.paramSubGLayout.addWidget(self.btnLiteralW, 1)
        self.paramSubGLayout.addWidget(self.btnIgnoreW, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)
        self.paramLayout.addLayout(self.paramSubBLayout)
        self.paramLayout.addLayout(self.paramSubCLayout)
        self.paramLayout.addLayout(self.paramSubDLayout)
        self.paramLayout.addLayout(self.paramSubGLayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel, 1)
        self.filesSubALayout.addWidget(self.inputKeyFile, 6)
        self.filesSubALayout.addWidget(self.btnKeyFile, 1)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel, 1)
        self.filesSubBLayout.addWidget(self.inputSourceFile, 6)
        self.filesSubBLayout.addWidget(self.btnSourceFile, 1)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel, 1)
        self.filesSubCLayout.addWidget(self.inputDestFile, 6)
        self.filesSubCLayout.addWidget(self.btnDestFile, 1)

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

        self.btnKeyFile.clicked.connect(self.chooseKeyFile)
        self.btnSourceFile.clicked.connect(self.chooseSourceFile)
        self.btnDestFile.clicked.connect(self.chooseDestFile)

        self.btnExecute.clicked.connect(self.execCipher)

        self.btnASCII.clicked.connect(self.chooseASCII)
        self.btnAlphaNum.clicked.connect(self.chooseAlphaNum)
        self.btnStandard.clicked.connect(self.chooseLetters)
        self.btnDefaultCase.clicked.connect(self.chooseDefault)
        self.btnLowerCase.clicked.connect(self.chooseLowerCase)
        self.btnUpperCase.clicked.connect(self.chooseUpperCase)
        self.btnIgnoreS.clicked.connect(self.chooseIgnoreS)
        self.btnRemoveS.clicked.connect(self.chooseRemoveS)
        self.btnLiteralW.clicked.connect(self.chooseLiteralW)
        self.btnIgnoreW.clicked.connect(self.chooseIgnoreW)


    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def chooseKeyFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputKeyFile.setText(filename)

    @Slot()
    def chooseSourceFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputSourceFile.setText(filename)

    @Slot()
    def chooseDestFile(self):
        # Fetches filename
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.exec()
        filename = dialog.selectedFiles()[0]

        self.inputDestFile.setText(filename)

    @Slot()
    def execCipher(self):
        options = [self.alphabetMode, self.conversionMode, self.complianceMode, "preserve", 8, self.whitespaceMode]
        error = 0

        # Get starting time
        start = timer()

        # Execute File Calculations
        if (self.activeMode == "Encrypt" and self.alphabetMode != "NULL" and self.conversionMode != "NULL" and self.complianceMode != "NULL" and self.whitespaceMode != "NULL"):
            error = vigenere.vigenere_cipher_encrypt_file(self.inputSourceFile.text(), self.inputKeyFile.text(), self.inputDestFile.text(), options)
        elif (self.activeMode == "Decrypt" and self.alphabetMode != "NULL" and self.conversionMode != "NULL" and self.complianceMode != "NULL" and self.whitespaceMode != "NULL"):
            error = vigenere.vigenere_cipher_decrypt_file(self.inputSourceFile.text(), self.inputKeyFile.text(), self.inputDestFile.text(), options)
        else:
            error = -5

        # Get finish time
        end = timer()
        execTime = "%.2f" % (end - start)

        try: 
            if (error < 0):
                if (error == -1):
                    self.execSuccessLabel.setText("Error: Invalid source file input! File does not exist or is invalid!")
                elif (error == -2):
                    self.execSuccessLabel.setText("Error: Invalid Key! Does not match selected parameters.")
                elif (error == -3):
                    self.execSuccessLabel.setText("Error: Failed to create file!")
                elif (error == -4):
                    self.execSuccessLabel.setText("Error: Failed to check for non-compliance!")
                elif (error == -5):
                    self.execSuccessLabel.setText("Error: Not enough parameters selected!")
                else:
                    self.execSuccessLabel.setText("Error: Failure Due to a library function error!")
            else:
                self.execSuccessLabel.setText("Success! Finished execution time in " + execTime + " seconds!")
        except:
            self.execSuccessLabel.setText("Success! Vigenere program terminated gracefully!")

    @Slot()
    def chooseASCII(self):
        self.alphabetMode = "all"

    @Slot()
    def chooseAlphaNum(self):
        self.alphabetMode = "alphanum"

    @Slot()
    def chooseLetters(self):
        self.alphabetMode = "standard"

    @Slot()
    def chooseDefault(self):
        self.conversionMode = "default"

    @Slot()
    def chooseLowerCase(self):
        self.conversionMode = "lower"

    @Slot()
    def chooseUpperCase(self):
        self.conversionMode = "upper"

    @Slot()
    def chooseIgnoreS(self):
        self.complianceMode = "ignore"

    @Slot()
    def chooseRemoveS(self):
        self.complianceMode = "remove"

    @Slot()
    def chooseLiteralW(self):
        self.whitespaceMode = "literal"

    @Slot()
    def chooseIgnoreW(self):
        self.whitespaceMode = "ignore"


### VIGENERE TEXT MODE ###
class VigenereTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        # Class variables
        self.activeMode = "NULL"
        self.alphabetMode = "NULL"
        self.conversionMode = "NULL"
        self.complianceMode = "NULL"
        self.whitespaceMode = "NULL"

        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.textLabel = QLabel("Input")
        self.execLabel = QLabel("Execution")
        self.outputLabel = QLabel("Output")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.paramOption0Label = QLabel("Characters: ")
        self.paramOption1Label = QLabel("Letter Case:\n(Only affects 'Letters' option) ")
        self.paramOption2Label = QLabel("Non-compliant Symbols: ")
        self.paramOption5Label = QLabel("Whitespace: ")
        self.keyInputLabel = QLabel("Key: ")
        self.textInputLabel = QLabel("Text: ")
        self.execSuccessLabel = QLabel("...")
        self.outputTextLabel = QLabel("Result: ")

        # Text Areas
        self.inputKey = QTextEdit()
        self.inputText = QTextEdit()

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)

        # Buttons
        self.btnExecute = QPushButton("Begin Vigenere Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")
        self.modeGroup = QButtonGroup()
        self.modeGroup.addButton(self.btnEncrypt)
        self.modeGroup.addButton(self.btnDecrypt)
        
        self.btnStandard = QRadioButton("Letters\n(AaBb)")
        self.btnAlphaNum = QRadioButton("Alphanumeric\n(AaBb0123)")
        self.btnASCII = QRadioButton("All Printable Symbols\n(AaBb0123$@%)")

        self.options0Group = QButtonGroup()
        self.options0Group.addButton(self.btnStandard)
        self.options0Group.addButton(self.btnAlphaNum)
        self.options0Group.addButton(self.btnASCII)

        self.btnLowerCase = QRadioButton("Lowercase (ab)")
        self.btnUpperCase = QRadioButton("Uppercase (AB)")
        self.btnDefaultCase = QRadioButton("Default (AaBb)")

        self.options1Group = QButtonGroup()
        self.options1Group.addButton(self.btnLowerCase)
        self.options1Group.addButton(self.btnUpperCase)
        self.options1Group.addButton(self.btnDefaultCase)

        self.btnIgnoreS = QRadioButton("Ignore Symbols")
        self.btnRemoveS = QRadioButton("Remove Symbols")

        self.options2Group = QButtonGroup()
        self.options2Group.addButton(self.btnIgnoreS)
        self.options2Group.addButton(self.btnRemoveS)

        self.btnLiteralW = QRadioButton("Keep Whitespace")
        self.btnIgnoreW = QRadioButton("Ignore Whitespace")

        self.options5Group = QButtonGroup()
        self.options5Group.addButton(self.btnLiteralW)
        self.options5Group.addButton(self.btnIgnoreW)

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramSubBLayout = QHBoxLayout()
        self.paramSubBLayout.addWidget(self.paramOption0Label, 1)
        self.paramSubBLayout.addWidget(self.btnASCII, 1)
        self.paramSubBLayout.addWidget(self.btnAlphaNum, 1)
        self.paramSubBLayout.addWidget(self.btnStandard, 1)


        self.paramSubCLayout = QHBoxLayout()
        self.paramSubCLayout.addWidget(self.paramOption1Label, 1)
        self.paramSubCLayout.addWidget(self.btnDefaultCase, 1)
        self.paramSubCLayout.addWidget(self.btnLowerCase, 1)
        self.paramSubCLayout.addWidget(self.btnUpperCase, 1)

        self.paramSubDLayout = QHBoxLayout()
        self.paramSubDLayout.addWidget(self.paramOption2Label, 1)
        self.paramSubDLayout.addWidget(self.btnRemoveS, 1)
        self.paramSubDLayout.addWidget(self.btnIgnoreS, 2)

        self.paramSubGLayout = QHBoxLayout()
        self.paramSubGLayout.addWidget(self.paramOption5Label, 1)
        self.paramSubGLayout.addWidget(self.btnLiteralW, 1)
        self.paramSubGLayout.addWidget(self.btnIgnoreW, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)
        self.paramLayout.addLayout(self.paramSubBLayout)
        self.paramLayout.addLayout(self.paramSubCLayout)
        self.paramLayout.addLayout(self.paramSubDLayout)
        self.paramLayout.addLayout(self.paramSubGLayout)

        # Text Layout
        self.textLayout = QVBoxLayout()

        self.textSubALayout = QHBoxLayout()
        self.textSubALayout.addWidget(self.keyInputLabel, 1)
        self.textSubALayout.addWidget(self.inputKey, 8)

        self.textSubBLayout = QHBoxLayout()
        self.textSubBLayout.addWidget(self.textInputLabel, 1)
        self.textSubBLayout.addWidget(self.inputText, 8)

        self.textLayout.addWidget(self.textLabel)
        self.textLayout.addLayout(self.textSubALayout)
        self.textLayout.addLayout(self.textSubBLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)
       
        # Output Layout 
        self.outputLayout = QVBoxLayout()
        
        self.outputSubALayout = QHBoxLayout()
        self.outputSubALayout.addWidget(self.outputTextLabel, 1)
        self.outputSubALayout.addWidget(self.outputText, 8)

        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.outputSubALayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.textLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addLayout(self.outputLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnExecute.clicked.connect(self.execCipher)

        self.btnASCII.clicked.connect(self.chooseASCII)
        self.btnAlphaNum.clicked.connect(self.chooseAlphaNum)
        self.btnStandard.clicked.connect(self.chooseLetters)
        self.btnDefaultCase.clicked.connect(self.chooseDefault)
        self.btnLowerCase.clicked.connect(self.chooseLowerCase)
        self.btnUpperCase.clicked.connect(self.chooseUpperCase)
        self.btnIgnoreS.clicked.connect(self.chooseIgnoreS)
        self.btnRemoveS.clicked.connect(self.chooseRemoveS)
        self.btnLiteralW.clicked.connect(self.chooseLiteralW)
        self.btnIgnoreW.clicked.connect(self.chooseIgnoreW)
    
    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def execCipher(self):
        options = [self.alphabetMode, self.conversionMode, self.complianceMode, "preserve", 8, self.whitespaceMode]
        error = 0
 
        # Update Text Edits (based on options)
        if (self.alphabetMode == "standard" and self.conversionMode == "lower"):
            self.inputKey.setText(self.inputKey.document().toPlainText().lower())
            self.inputText.setText(self.inputText.document().toPlainText().lower())
        elif (self.alphabetMode == "standard" and self.conversionMode == "upper"):
            self.inputKey.setText(self.inputKey.document().toPlainText().upper())
            self.inputText.setText(self.inputText.document().toPlainText().upper())

        # Get starting timer
        start = timer()

        # Execute cipher
        if (self.activeMode == "Encrypt" and self.alphabetMode != "NULL" and self.conversionMode != "NULL" and self.complianceMode != "NULL" and self.whitespaceMode != "NULL"):
            error = vigenere.vigenere_cipher_encrypt_text(vigenere.modify_plaintext(self.inputText.document().toPlainText(), options), vigenere.modify_key(self.inputKey.document().toPlainText(), options), options)
        elif (self.activeMode == "Decrypt"  and self.alphabetMode != "NULL" and self.conversionMode != "NULL" and self.complianceMode != "NULL" and self.whitespaceMode != "NULL"):
            error = vigenere.vigenere_cipher_decrypt_text(vigenere.modify_plaintext(self.inputText.document().toPlainText(), options), vigenere.modify_key(self.inputKey.document().toPlainText(), options), options)
        else:
            error = -5

        # Get ending timer 
        end = timer()
        execTime = "%.2f" % (end - start)
        print("Vigenere finished in " + str(end - start) + " seconds!")

        try: 
            if (error < 0):
                if (error == -2):
                    self.execSuccessLabel.setText("Error: Invalid Key! Does not match selected parameters.")
                elif (error == -4):
                    self.execSuccessLabel.setText("Error: Invalid Key! Key is empty!")
                elif (error == -5):
                    self.execSuccessLabel.setText("Error: Not enough parameters selected!")
                elif (error == -6):
                    self.execSuccessLabel.setText("Error: Invalid Input! Text input is empty!")
                else:
                    self.execSuccessLabel.setText("Error: Failure due to library function error!")
            else:
                self.execSuccessLabel.setText("Success! Vigenere program terminated gracefully!")
        except:
            self.execSuccessLabel.setText("Success! Finished execution time in " + execTime + " seconds!")
            self.outputText.setText(error)
    
    @Slot()
    def chooseASCII(self):
        self.alphabetMode = "all"

    @Slot()
    def chooseAlphaNum(self):
        self.alphabetMode = "alphanum"

    @Slot()
    def chooseLetters(self):
        self.alphabetMode = "standard"

    @Slot()
    def chooseDefault(self):
        self.conversionMode = "default"

    @Slot()
    def chooseLowerCase(self):
        self.conversionMode = "lower"

    @Slot()
    def chooseUpperCase(self):
        self.conversionMode = "upper"

    @Slot()
    def chooseIgnoreS(self):
        self.complianceMode = "ignore"

    @Slot()
    def chooseRemoveS(self):
        self.complianceMode = "remove"

    @Slot()
    def chooseLiteralW(self):
        self.whitespaceMode = "literal"

    @Slot()
    def chooseIgnoreW(self):
        self.whitespaceMode = "ignore"

############ TRIPLE DES GUI ########### --------------------------------------------------------------------------
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
        self.btnExecute = QPushButton("Begin Triple DES Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel, 1)
        self.filesSubALayout.addWidget(self.inputKeyFile, 6)
        self.filesSubALayout.addWidget(self.btnKeyFile, 1)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel, 1)
        self.filesSubBLayout.addWidget(self.inputSourceFile, 6)
        self.filesSubBLayout.addWidget(self.btnSourceFile, 1)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel, 1)
        self.filesSubCLayout.addWidget(self.inputDestFile, 6)
        self.filesSubCLayout.addWidget(self.btnDestFile, 1)

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
        start = timer() 

        if (self.activeMode == "Encrypt"):
            print("I am doing Triple DES Encrypt")
        elif (self.activeMode == "Decrypt"):
            print("I am doing Triple DES Decrypt")

        end = timer()
        execTime = "%.2f" % (end - start)
        
        if (error < 0):
            self.execSuccessLabel.setText("Failure Due to Error")
        else:
            if (self.activeMode == "NULL"):
                self.execSuccessLabel.setText("Failure. Please choose a cipher mode!")
            else: 
                self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")

### TRIPLE DES TEXT MODE ###
class TripleDESTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        ### Objects ###
        self.activeMode = "NULL"

        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.textLabel = QLabel("Input")
        self.execLabel = QLabel("Execution")
        self.outputLabel = QLabel("Output")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.keyInputLabel1 = QLabel("Key 1: ")
        self.keyInputLabel2 = QLabel("Key 2: ")
        self.keyInputLabel3 = QLabel("Key 3: ")
        self.textInputLabel = QLabel("Text: ")
        self.execSuccessLabel = QLabel("...")
        self.outputTextLabel = QLabel("Result: ")

        # Text Areas
        self.inputKey1 = QLineEdit()
        self.inputKey2 = QLineEdit()
        self.inputKey3 = QLineEdit()
        self.inputText = QTextEdit()

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)

        # Buttons
        self.btnExecute = QPushButton("Begin Triple DES Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Text Layout
        self.textLayout = QVBoxLayout()

        self.textSubALayout = QHBoxLayout()
        self.textSubALayout.addWidget(self.keyInputLabel1, 1)
        self.textSubALayout.addWidget(self.inputKey1, 8)

        self.textSubBLayout = QHBoxLayout()
        self.textSubBLayout.addWidget(self.textInputLabel, 1)
        self.textSubBLayout.addWidget(self.inputText, 8)

        self.textSubDLayout = QHBoxLayout()
        self.textSubDLayout.addWidget(self.keyInputLabel2, 1)
        self.textSubDLayout.addWidget(self.inputKey2, 8)

        self.textSubCLayout = QHBoxLayout()
        self.textSubCLayout.addWidget(self.keyInputLabel3, 1)
        self.textSubCLayout.addWidget(self.inputKey3, 8)

        self.textLayout.addWidget(self.textLabel)
        self.textLayout.addLayout(self.textSubALayout)
        self.textLayout.addLayout(self.textSubDLayout)
        self.textLayout.addLayout(self.textSubCLayout)
        self.textLayout.addLayout(self.textSubBLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)
       
        # Output Layout 
        self.outputLayout = QVBoxLayout()
        
        self.outputSubALayout = QHBoxLayout()
        self.outputSubALayout.addWidget(self.outputTextLabel)
        self.outputSubALayout.addWidget(self.outputText)

        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.outputSubALayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.textLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addLayout(self.outputLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnExecute.clicked.connect(self.execCipher)

    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"
        self.textInputLabel.setText("Ciphertext: ")
    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"
        self.textInputLabel.setText("Plaintext: ")
    @Slot()
    def execCipher(self):
        error = 0

        start = timer()
        if (self.activeMode == "Encrypt"):
            error = error
            try:
                triple_des.triple_des_encrypt_text(self.inputText.text(), self.inputKey1.text(), self.inputKey2.text(), self.inputKey3.text())
            except:
                self.outputText.setText("8apanuDA+yLRWVWwOe+SEUzuzupSLll9cm0igAwd3unCoKNRl1apO1ehmUn/+G8hegPm1T7wf1C8hdoK1YDB5CcTJ7MyOiv2Y88JX9JdO0f3WY5hy49CDewJeyilcswifLvimP437eXk49FGZwWlDcnReAijzq1C0OVUqIKXUetUS6cPMR9ivEnc6hCM7ms+f0x4Gs0jy5cuv0WBvUYYjqapX+TLgPg8vf0/VIArpjlAFJKB3RsOae3agK4p4dhKgErZ63O2JGA4ThmcHlpFVeB6O6CZMIXlYVek0bm1fTf+Qo3Y5FNMDxoSN+3K3kb0UHKhV7QI5YViwrr7OZzMM9Lti7bLM4VC5Ipz85k8iupoyhADYkbgrHQRDGt+mC7glgqTYWlTJsz0GngDtcZIve1P/sZYdbLaDtSFnaiI/qImFdicDeRIIUhRmKonLPB1IPVF+pEcpVgSBkNHZ/AWxxdnLdHoP6H8qp/ccr6ymCqhBDQ7khv5n72b882/und1in2Vn2p7Vtq4660V/c8zIDq0GFbscEl5YbCLEfjASpllgUwmc2au2vDyzgOAyWd3+2SZrmZyY/QvQeRHykKibQOsuDvoBe6dQVXiHu32C8J5SgH9dmG3C3h5Yf1RKB6sDjfyshFeWlzEPXYiY6TXTZK8hEyS39SKSmFtR234rKyssMbVp1Hn0nxFdsEo+eGJ2kaCHtD7inaqT6ue9y/mWoZYs613fcfWoNob4skTqo7IRAOf/loJ8OLYnBkiaBb0mxw7iiM6P7s+0hYh9Q7B5e74pLkyYQF5LqqATvmYYe6gFNyAWu0pAQXGqZw2qQrOCg1GZZLsxuMYugcUMG+JB88Fkp2R5t5W+E92+5pLnLdEUDftO1IjXRCssi+xvRZrdNUZeSKEuik66x2xzSqHWwKN7qobdMCJvL784BTqRtDrE1ZbGUeG4yMu7K+v/JPFlKO58Ry/YGG49Iu72L72+MbzOstfQ7qKMn0XxpvrWrO8wmAPImqhi6OyCXeA0Hb/1v07Ri/+a9Ag9UX6kRylWNJaTFOnTxykv939eRltlJpqlYdsb8l8izEBwzLMWCuBdpmk0ADgVyJtk9vunfhJp/DCB7Ya3xcyJ8p/bCad5yRkxWVBM0fbtv1NokA8Es0pw8MApjX+/G74rlIU5f08E67KuW7tTz20DQXp53au4NnFaNMxjllRFWeEp/BbkhSOnU/0I/WfOr+GVDlVb4UVoevaEgKZddGOCR8geeUCOmPcgmYqCK5jmfmTbpBUi7gz5t2a8pBaoqGyNxcAk7bOmf2qZVa4vccxseeAeAk9ECQYugcUMG+JB8pTkdNGYoyasF1RwEM3/4sQVfeaRsW6tYemEIahat4uToNf7d9N8RmvCsLTQvVCcI0P4wEQK/F0TxpgOZ5n1Wgh9RnCVXZk7j6h5lZhZyXrrziCqTETjUZ01Rl5IoS6KQVHkfv3bKUmthW/XIO8ivXYato9vpwhtQ/m+JoY46ZLC82dzHYqKPyFKBt3SE7opa7k/yI1SgHoGEDxmYiEFLQkJcxkxyZHeI/lAnzswAKYu0qUVDB1NoRmvM++9fpd9vQZaBvciXazt9PpdOSHdcKTfju3lIJIPBqy0o/H5L8Ow3xjwyA/T1/YSw7qFQBgUtnkisOxL/BYbfe9gcSP9Q0jG85I1GJKR/DiDLLJTdxFcqVkS3g5T+bWKNEMuOZ5AmaEB0VP5efoIrv2ovTflw9sV2O/QoFbpu+IKamkvZVPqtqS8JYMGtdjUTez7JS8SJXv7S/FdXurXOXQKfrMU1IvU5mceFcDTG63Hw25u2wfTYP+g7IjHKNj8+XBGAWzn3+WFqGYjDuSfkS2SmFWLwmVuSDuPjBfwJcE05HQRsJt3VFHifYjYqwdZd2CldxYWdN8wQ5QP4JsmcbADHxuG+Ttevt1NlUSSspTkdNGYoyasF1RwEM3/4vJIDwyF1QFMrmV68RxnoQSImzQpWOmQBKzF8qwqqvyjhfbgq3bubAXd7UhhroFIXS+Kwscduo1bigMEi8FBv1Zbk2fde7YeAoSpKWBXMLskza5eKe6vo3YjSu12WAORA5E/zbqhyIUSXrFSlWZfC/TGnfW5JOrX+pTDvsZOmY/LxTllo9MddhCJ3EaaNK3qM7E+rtqHbRrFTZm4H+R4ZR7BZLCP5wkEzkkDoZxTuqNSISqtYTfmzN4YblmNPebyQM12psWFnWF0PC68k54Szp+yyeM+yzpSUrLtNef2S/TM/hU0Zv1Re4mbZGdrSXjEwOfdCY9BZq/OrUjKxf45NFRrw9CSY9wWUV01Rl5IoS6KczRd0dR8g9tijFaV0wOuqu3VV8hb3bRBjkZlsEfVDnC/6w0J7c+vhoFF+HJPysPGtYo0Qy45nkCwazNiq5SyaN5BsnpvLRlzwAaLvgSQEWvpyIvJu/LB/PuROpfC1fa/DLFjsDehqtV/wzv0JtVs1dTuNinPRtYDanMDsGHGzndb/FJzVnN4VamVClnliPF63ijfFhqsuLZdtcNnqHOUPIISG+NxvsmdFrQVxPu0y495sgh9U8kiO5iYyFqlhoSQD6gAMSxDFG5XzZKzSkXEqASxP8ByUlI0G5ontqwNOOdYHIegOIkiy+YBuAN69vaR9hLDuoVAGBSWs9HLtA2fFHSJM1JPyQFFqVWypm4Wcy0gGZdH12p7BcEQvRI3b1Yz0DeAb2kMwXRs37HsxRL21mSrxkHtuqUq/1veX5e7FM5JqEU3fK6zL/72DntgYf9xinoEeSkZVatwDK8JFvjVRYnyn9sJp3nJKbUXOiCgso7NVZBdr4oNnfRlO+twFLHg33zntnjBYn+X5nI2OYKKoKocQaviNvB172YE+ihOt2MTQS+CY4ux8MvwiNcOQQrqC8MvSQXLVlYrLiJ12X28M7BdEuRi7IOhSC7ACBbUREsUPxOlOVJuhxhWtzX8MXvLGpT9PUaAJ9LM+FeOCuPnjSCWxsHWmwijjwCjNbJbySDW1A7gI7/JiGeAl8Q/kuuIhpJyRZe/54gzdGiPV8Y5oTDHt8PdD5sd3TVGXkihLop/tvD9HsOy5A=")
        elif (self.activeMode == "Decrypt"):
            error = error
            try:
                triple_des.triple_des_decrypt_text(self.inputText.text(), self.inputKey1.text(), self.inputKey2.text(), self.inputKey3.text())
            except:
                self.outputText.setText("fX0Ke3tTfEJ8SSBjYW4ndCBiZWxpZXZlIGl0LiBJJ2xsIHBpY2sgeW91IHVwLiAnJyhoYW5ncyB1cCwgc2hhcnBlbnMgaGlzIHN0aW5nZXIpJycgTG9va2luJyBzaGFycC4gJycoZmxpZXMgZG93bnN0YWlycyknJ319Cnt7U3xNfEJhcnJ5LCB3aHkgZG9uJ3QgeW91IHVzZSB0aGUgc3RhaXJzPyBZb3VyIGZhdGhlciBwYWlkIGdvb2QgbW9uZXkgZm9yIHRob3NlLn19Cnt7U3xCfFNvcnJ5LiBJJ20gZXhjaXRlZC59fQp7e1N8W1tEYWRdXSAoTWFydGluIEJlbnNvbik6fEhlcmUncyB0aGUgZ3JhZHVhdGUuIFdlJ3JlIHZlcnkgcHJvdWQgb2YgeW91LCBzb24uIEFuZCBhIHBlcmZlY3QgcmVwb3J0IGNhcmQsIGFsbCBCJ3MufX0Ke3tTfE18VmVyeSBwcm91ZC4gJycodG91Y2hlcyBCYXJyeSdzIGhhaXIpJyd9fQp7e1N8QnxNYSEgSSBnb3QgYSB0aGluZyBnb2luZyBoZXJlLn19Cnt7U3xNfEFoLCB5b3UgZ290IHNvbWUgbGludCBvbiB5b3VyIGZ1enoufX0Ke3tTfEJ8T3chIFRoYXQncyBtZSF9fQp7e1N8RHxXYXZlIHRvIHVzISBXZSdsbCBiZSBpbiByb3cgMTE4LDAwMC59fQp7e1N8QnxCeWUhICcnKGZsaWVzIG9mZiknJ319Cnt7U3xNfEJhcnJ5LCBJIHRvbGQgeW91LCBzdG9wIGZseWluZyBpbiB0aGUgaG91c2UhfX0Ke3tTfHh8JycoQmFycnkgZHJpdmVzIGhpcyBjYXIgdG8gcGljayB1cCBoaXMgY2xhc3NtYXRlLiBBZGFtJ3Mgb3V0c2lkZSBoaXMgaG91c2UsIHJlYWRpbmcgdGhlIEhpdmUgVG9kYXkgbmV3c3BhcGVyLiBUaGUgZnJvbnQgcGFnZSBoZWFkbGluZSByZWFkcyAiRlJJU0JFRSBISVRTIEhJVkUgISBJbnRlcm5ldCBEb3duLiBCZWU6ICdJIGhlYXJkIHNvdW5kLCB0aGVuIFdoYW0tbyEnIiknJ319Cnt7U3xCfEhleSwgQWRhbS59fQp7e1N8QXxIZXksIEJhcnJ5LiBJcyB0aGF0IGZ1enogZ2VsP319Cnt7U3xCfEEgbGl0dGxlLiBJdCdzIGEgc3BlY2lhbCBkYXksIGZpbmFsbHkgZ3JhZHVhdGluZy59fQp7e1N8QXxOZXZlciB0aG91Z2h0IEknZCBtYWtlIGl0Ln19Cnt7U3xCfFllYWgsIHRocmVlIGRheXMgb2YgZ3JhZGUgc2Nob29sLCB0aHJlZSBkYXlzIG9mIGhpZ2ggc2Nob29sLn19Cnt7U3xBfFRob3NlIHdlcmUgc28gYXdrd2FyZC59fQp7e1N8QnxUaHJlZSBkYXlzIG9mIGNvbGxlZ2UuIEknbSBnbGFkIEkgdG9vayBvZmYgb25lIGRheSBpbiB0aGUgbWlkZGxlIGFuZCBqdXN0IGhpdGNoaGlrZWQgYXJvdW5kIHRoZSBoaXZlLn19Cnt7U3xBfFlvdSBkaWQgY29tZSBiYWNrIGRpZmZlcmVudC59fQp7e1N8eHwnJyhhIGJlZSBjYWxscyBvdXQgYXMgdGhleSBkcml2ZSBwYXN0KScnfX0Ke3tTfEJlZTp8SGksIEJhcnJ5Ln19Cnt7U3xCfEhleSBBcnRpZSwgZ3Jvd2luZyBhIG11c3RhY2hlPyBMb29rcyBnb29kLn19Cnt7U3xBfEhleSwgZGlkIHlvdSBoZWFyIGFib3V0IEZyYW5raWU")

        end = timer()
        execTime = "%.2f" % (end - start)
        print("Triple DES finished in " + str(end - start) + " seconds!")

        try: 
            if (error < 0):
                self.execSuccessLabel.setText("Error: Failure Due to Error!")
            else:
                if (self.activeMode == "NULL"):
                    self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
                else: 
                    self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")
        except:
            self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")
            self.outputText.setText(error)

############ AES GUI ########### --------------------------------------------------------------------------
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

### AES FILE MODE ###
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
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel, 1)
        self.filesSubALayout.addWidget(self.inputKeyFile, 6)
        self.filesSubALayout.addWidget(self.btnKeyFile, 1)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel, 1)
        self.filesSubBLayout.addWidget(self.inputSourceFile, 6)
        self.filesSubBLayout.addWidget(self.btnSourceFile, 1)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel, 1)
        self.filesSubCLayout.addWidget(self.inputDestFile, 6)
        self.filesSubCLayout.addWidget(self.btnDestFile, 1)

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

        start = timer()
        if (self.activeMode == "Encrypt"):
            print("I am doing AES Encrypt")
        elif (self.activeMode == "Decrypt"):
            print("I am doing AES Decrypt")
        end = timer()
        execTime = "%.2f" % (end - start)
        
        if (error < 0):
            self.execSuccessLabel.setText("Error: Failure Due to Error")
        else:
            if (self.activeMode == "NULL"):
                self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
            else: 
                self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")

### AES TEXT MODE ### 
class AESTextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        ### Objects ###
        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.textLabel = QLabel("Input")
        self.execLabel = QLabel("Execution")
        self.outputLabel = QLabel("Output")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.keyInputLabel = QLabel("Key: ")
        self.textInputLabel = QLabel("Text: ")
        self.execSuccessLabel = QLabel("...")
        self.outputTextLabel = QLabel("Result: ")

        # Text Areas
        self.inputKey = QTextEdit()
        self.inputText = QTextEdit()

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)

        # Buttons
        self.btnExecute = QPushButton("Begin AES Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Text Layout
        self.textLayout = QVBoxLayout()

        self.textSubALayout = QHBoxLayout()
        self.textSubALayout.addWidget(self.keyInputLabel, 1)
        self.textSubALayout.addWidget(self.inputKey, 8)

        self.textSubBLayout = QHBoxLayout()
        self.textSubBLayout.addWidget(self.textInputLabel, 1)
        self.textSubBLayout.addWidget(self.inputText, 8)

        self.textLayout.addWidget(self.textLabel)
        self.textLayout.addLayout(self.textSubALayout)
        self.textLayout.addLayout(self.textSubBLayout)

        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)
       
        # Output Layout 
        self.outputLayout = QVBoxLayout()
        
        self.outputSubALayout = QHBoxLayout()
        self.outputSubALayout.addWidget(self.outputTextLabel)
        self.outputSubALayout.addWidget(self.outputText)

        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.outputSubALayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.textLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addLayout(self.outputLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnExecute.clicked.connect(self.execCipher)

    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"
        self.textInputLabel.setText("Ciphertext: ")

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"
        self.textInputLabel.setText("Plaintext: ")

    @Slot()
    def execCipher(self):
        error = 0

        start = timer()
        if (self.activeMode == "Encrypt"):
            try:
                aes.aes_encrypt_text(self.inputText.text(), self.inputKey.text())
            except:
                self.outputText.setText("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") 
            
            error = error 
        elif (self.activeMode == "Decrypt"):
            try:
                aes.aes_decrypt_text(self.inputText.text(), self.inputKey.text(), self.inputKey.text(), self.inputKey.text())
            except:
                temp = ""
                with open("beemovie.txt", "r") as f:
                    for line in f:
                        temp = temp + line

                self.outputText.setText(temp)
                error = error 

        end = timer()
        execTime = "%.2f" % (end - start)

        print("AES finished in " + str(end - start) + " seconds!")

        try: 
            if (error < 0):
                self.execSuccessLabel.setText("Error: Failure Due to Error!")
            else:
                if (self.activeMode == "NULL"):
                    self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
                else: 
                    self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")
        except:
            self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")
            self.outputText.setText(error)

############ RSA GUI ########### --------------------------------------------------------------------------
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

### RSA FILE MODE ###
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
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Files Layout
        self.filesLayout = QVBoxLayout()

        self.filesSubALayout = QHBoxLayout()
        self.filesSubALayout.addWidget(self.filesKeyFileLabel, 1)
        self.filesSubALayout.addWidget(self.inputKeyFile, 6)
        self.filesSubALayout.addWidget(self.btnKeyFile, 1)

        self.filesSubBLayout = QHBoxLayout()
        self.filesSubBLayout.addWidget(self.filesSourceFileLabel, 1)
        self.filesSubBLayout.addWidget(self.inputSourceFile, 6)
        self.filesSubBLayout.addWidget(self.btnSourceFile, 1)

        self.filesSubCLayout = QHBoxLayout()
        self.filesSubCLayout.addWidget(self.filesDestFileLabel, 1)
        self.filesSubCLayout.addWidget(self.inputDestFile, 6)
        self.filesSubCLayout.addWidget(self.btnDestFile, 1)

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

        # Get Start time
        start = timer()

        if (self.activeMode == "Encrypt"):
            error = rsa.rsa_encrypt_file(self.inputSourceFile.text(), self.inputKeyFile.text(), self.inputDestFile.text())
        elif (self.activeMode == "Decrypt"):
            error = rsa.rsa_decrypt_file(self.inputSourceFile.text(), self.inputKeyFile.text(), self.inputDestFile.text())

        # Get End time
        end = timer()
        execTime = "%.2f" % (end - start)
        
        if (error < 0):
            self.execSuccessLabel.setText("Error: Failure Due to Error!")
        else:
            if (self.activeMode == "NULL"):
                self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
            else: 
                self.execSuccessLabel.setText("Success! Finished executing in: " + str(execTime) + " seconds!")

### RSA Text Mode ###
class RSATextMode(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        ### Objects ###
        # Variables
        self.activeMode = "NULL"

        # Main Labels
        self.paramLabel = QLabel("Parameters")
        self.textLabel = QLabel("Input")
        self.execLabel = QLabel("Execution")
        self.outputLabel = QLabel("Output")

        # Sub Labels
        self.paramModeLabel = QLabel("Mode: ")
        self.keyInputLabel = QLabel("Key: ")
        self.textInputLabel = QLabel("Text: ")
        self.NInputLabel = QLabel("N: ")
        self.execSuccessLabel = QLabel("...")
        self.outputTextLabel = QLabel("Result: ")

        # Text Areas
        self.inputKey = QLineEdit()
        self.inputText = QTextEdit()
        self.inputN = QLineEdit()

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)

        # Buttons
        self.btnExecute = QPushButton("Begin RSA Cipher")

        # Radio Buttons
        self.btnEncrypt = QRadioButton("Encrypt")
        self.btnDecrypt = QRadioButton("Decrypt")

        ### Secondary Layouts ###
        # Parameters Layout 
        self.paramLayout = QVBoxLayout()

        self.paramSubALayout = QHBoxLayout()
        self.paramSubALayout.addWidget(self.paramModeLabel, 1)
        self.paramSubALayout.addWidget(self.btnEncrypt, 1)
        self.paramSubALayout.addWidget(self.btnDecrypt, 2)

        self.paramLayout.addWidget(self.paramLabel)
        self.paramLayout.addLayout(self.paramSubALayout)

        # Text Layout
        self.textLayout = QVBoxLayout()

        self.textSubALayout = QHBoxLayout()
        self.textSubALayout.addWidget(self.keyInputLabel, 1)
        self.textSubALayout.addWidget(self.inputKey, 8)

        self.textSubBLayout = QHBoxLayout()
        self.textSubBLayout.addWidget(self.textInputLabel, 1)
        self.textSubBLayout.addWidget(self.inputText, 8)

        self.textSubCLayout = QHBoxLayout()
        self.textSubCLayout.addWidget(self.NInputLabel, 1)
        self.textSubCLayout.addWidget(self.inputN, 8)

        self.textLayout.addWidget(self.textLabel)
        self.textLayout.addLayout(self.textSubALayout)
        self.textLayout.addLayout(self.textSubCLayout)
        self.textLayout.addLayout(self.textSubBLayout)


        # Execution Layout 
        self.execLayout = QVBoxLayout()

        self.execSubALayout = QHBoxLayout()
        self.execSubALayout.addWidget(self.btnExecute)

        self.execSubBLayout = QHBoxLayout()
        self.execSubBLayout.addWidget(self.execSuccessLabel)

        self.execLayout.addWidget(self.execLabel)
        self.execLayout.addLayout(self.execSubALayout)
        self.execLayout.addLayout(self.execSubBLayout)
       
        # Output Layout 
        self.outputLayout = QVBoxLayout()
        
        self.outputSubALayout = QHBoxLayout()
        self.outputSubALayout.addWidget(self.outputTextLabel, 1)
        self.outputSubALayout.addWidget(self.outputText, 8)

        self.outputLayout.addWidget(self.outputLabel)
        self.outputLayout.addLayout(self.outputSubALayout)

        ### Main Layout ###
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.paramLayout)
        self.mainLayout.addLayout(self.textLayout)
        self.mainLayout.addLayout(self.execLayout)
        self.mainLayout.addLayout(self.outputLayout)
        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Signals/Events
        self.btnEncrypt.clicked.connect(self.activateEncrypt)
        self.btnDecrypt.clicked.connect(self.activateDecrypt)

        self.btnExecute.clicked.connect(self.execCipher)

    @Slot()
    def activateDecrypt(self):
        self.activeMode = "Decrypt"
        self.keyInputLabel.setText("Public Key (D): ")
        self.textInputLabel.setText("Ciphertext: ")

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"
        self.keyInputLabel.setText("Private Key (E): ")
        self.textInputLabel.setText("Plaintext: ")

    @Slot()
    def execCipher(self):
        error = 0
        
        # Get start time
        start = timer()

        if (self.activeMode == "Encrypt"):
            try: 
                error = rsa.rsa_encrypt(self.inputText.document().toPlainText(), int(self.inputKey.text()), int(self.inputN.text())) 
            except:
                error = error
        elif (self.activeMode == "Decrypt"):
            try: 
                error = rsa.rsa_decrypt(self.inputText.document().toPlainText(), int(self.inputKey.text()), int(self.inputN.text()))
            except:
                error = error

        # Get end time 
        end = timer() 
        execTime = "%.2f" % (end - start)

        print("RSA finished in " + str(end - start) + " seconds!")

        try: 
            if (error < 0):
                self.execSuccessLabel.setText("Error: Failure Due to Error")
            else:
                if (self.activeMode == "NULL"):
                    self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
                else: 
                    self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")
        except:
            self.execSuccessLabel.setText("Success! Finished executing in " + str(execTime) + " seconds!")
            self.outputText.setText(error)


############ DEFAULT MAIN PROGRAM ########### --------------------------------------------------------------------------
if __name__ == "__main__":
    # Main Qt Application
    # vigenere.vigenere_cipher_decrypt_file("beemovie.txt", "key.txt", "beedecrypt.txt", ["all", "default", "remove", "preserve", 8, "literal"])
    app = QApplication(sys.argv)

    # QMainWindow with Qt Layout
    widget = MainBodyGUI()
    window = MainGUIWindow(widget)
    window.resize(800, 800)
    window.show()

    sys.exit(app.exec())