################################ 
# File: cipherGUI.py
# Execution Order:
# 1) python -m venv env
# 2) python .\cipherGUI.py
################################

########### LIBRARIES ########## --------------------------------------------------------------------------
# Python Libraries
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
        tabWidget.addTab(TripleDESGUI(self), "Triple Des")
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
            print("I am doing Triple DES Encrypt")
        elif (self.activeMode == "Decrypt"):
            print("I am doing Triple DES Decrypt")
        
        if (error < 0):
            self.execSuccessLabel.setText("Failure Due to Error")
        else:
            if (self.activeMode == "NULL"):
                self.execSuccessLabel.setText("Failure. Please choose a cipher mode!")
            else: 
                self.execSuccessLabel.setText("Success")

### TRIPLE DES TEXT MODE ###
class TripleDESTextMode(QWidget):
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

        # Text Layout
        self.textLayout = QVBoxLayout()

        self.textSubALayout = QHBoxLayout()
        self.textSubALayout.addWidget(self.keyInputLabel)
        self.textSubALayout.addWidget(self.inputKey)

        self.textSubBLayout = QHBoxLayout()
        self.textSubBLayout.addWidget(self.textInputLabel)
        self.textSubBLayout.addWidget(self.inputText)

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

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def execCipher(self):
        options = ["all", "default", "remove", "preserve", 8, "literal"]
        error = 0

        if (self.activeMode == "Encrypt"):
            error = error
            # error = vigenere.vigenere_cipher_encrypt_text(self.inputText.document().toPlainText(), self.inputKey.document().toPlainText(), options)

        elif (self.activeMode == "Decrypt"):
            error = error
            # error = vigenere.vigenere_cipher_decrypt_text(self.inputText.document().toPlainText(), self.inputKey.document().toPlainText(), options)

        try: 
            if (error < 0):
                self.execSuccessLabel.setText("Error: Failure Due to Error!")
            else:
                if (self.activeMode == "NULL"):
                    self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
                else: 
                    self.execSuccessLabel.setText("Success")
        except:
            self.execSuccessLabel.setText("Success")
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
            self.execSuccessLabel.setText("Error: Failure Due to Error")
        else:
            if (self.activeMode == "NULL"):
                self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
            else: 
                self.execSuccessLabel.setText("Success")

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
        self.btnExecute = QPushButton("Begin Vigenere Cipher")

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

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"

    @Slot()
    def execCipher(self):
        options = ["all", "default", "remove", "preserve", 8, "literal"]
        error = 0

        if (self.activeMode == "Encrypt"):
            error = error 

        elif (self.activeMode == "Decrypt"):
            error = error 

        try: 
            if (error < 0):
                self.execSuccessLabel.setText("Error: Failure Due to Error!")
            else:
                if (self.activeMode == "NULL"):
                    self.execSuccessLabel.setText("Error: Please choose a cipher mode!")
                else: 
                    self.execSuccessLabel.setText("Success!")
        except:
            self.execSuccessLabel.setText("Success!")
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
        self.btnExecute = QPushButton("Begin Vigenere Cipher")

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
        self.keyInputLabel.setText("Public Key (E): ")
        self.textInputLabel.setText("Ciphertext: ")

    @Slot()
    def activateEncrypt(self):
        self.activeMode = "Encrypt"
        self.keyInputLabel.setText("Private Key (D): ")
        self.textInputLabel.setText("Plaintext: ")

    @Slot()
    def execCipher(self):
        error = 0
        
        # Get start time
        start = timer()

        if (self.activeMode == "Encrypt"):
            error = rsa.rsa_encrypt(self.inputText.document().toPlainText(), int(self.inputKey.text()), int(self.inputN.text())) 
        elif (self.activeMode == "Decrypt"):
            error = rsa.rsa_decrypt(self.inputText.document().toPlainText(), self.inputKey.text(), self.inputN.text())

        # Get end time 
        end = timer() 
        execTime = "%.2f" % (end - start)

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