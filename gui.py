from typing import OrderedDict
from term import Term
from PyQt5 import QtCore, QtGui, QtWidgets
import io
import cpverifier
import re
from cpparser import ParseRule
from cpparser import ParseTerm
from cpparser import ParsecPVJSON
from cpverifier import CPVerifier
from cpsystem import CPSystem
from contextlib import redirect_stdout
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def __init__(self, mw):
        self.MainWindow = mw
        self.sys = CPSystem()
        self.ve = CPVerifier(self.sys)
        
    def setupUi(self):
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(993, 667)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 171, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 111, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 290, 61, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.textEdit_rules = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_rules.setGeometry(QtCore.QRect(20, 320, 451, 291))
        self.textEdit_rules.setObjectName("textEdit_rules")
        self.textEdit_terms = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_terms.setGeometry(QtCore.QRect(20, 130, 451, 151))
        self.textEdit_terms.setToolTipDuration(-1)
        self.textEdit_terms.setObjectName("textEdit_terms")
        self.textEdit_state = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_state.setGeometry(QtCore.QRect(140, 50, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textEdit_state.setFont(font)
        self.textEdit_state.setObjectName("textEdit_state")
        self.textEdit_name = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_name.setGeometry(QtCore.QRect(140, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textEdit_name.setFont(font)
        self.textEdit_name.setObjectName("textEdit_name")
        self.pushButton_simulate = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_simulate.setGeometry(QtCore.QRect(520, 50, 128, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_simulate.setFont(font)
        self.pushButton_simulate.setObjectName("pushButton_simulate")
        self.pushButton_verify = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_verify.setGeometry(QtCore.QRect(750, 50, 128, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_verify.setFont(font)
        self.pushButton_verify.setObjectName("pushButton_verify")
        self.comboBox_veri_opt = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_veri_opt.setGeometry(QtCore.QRect(750, 10, 171, 29))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.comboBox_veri_opt.setFont(font)
        self.comboBox_veri_opt.setStatusTip("")
        self.comboBox_veri_opt.setObjectName("comboBox_veri_opt")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.comboBox_veri_opt.addItem("")
        self.textEdit_prop_spe = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_prop_spe.setGeometry(QtCore.QRect(520, 130, 451, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textEdit_prop_spe.setFont(font)
        self.textEdit_prop_spe.setObjectName("textEdit_prop_spe")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(520, 100, 201, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 240, 261, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.textBrowser_result = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_result.setFont(font)
        self.textBrowser_result.setGeometry(QtCore.QRect(520, 270, 451, 341))
        self.textBrowser_result.setObjectName("textBrowser_result")
        self.label_background = QtWidgets.QLabel(self.centralwidget)
        self.label_background.setGeometry(QtCore.QRect(0, 0, 981, 641))
        self.label_background.setText("")
        self.label_background.setPixmap(QtGui.QPixmap("background/IMG_1.jpg"))
        self.label_background.setScaledContents(True)
        self.label_background.setWordWrap(False)
        self.label_background.setObjectName("label_background")
        self.comboBox_detail = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_detail.setGeometry(QtCore.QRect(520, 10, 151, 29))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.comboBox_detail.setFont(font)
        self.comboBox_detail.setStatusTip("")
        self.comboBox_detail.setObjectName("comboBox_detail")
        self.comboBox_detail.addItem("")
        self.comboBox_detail.addItem("")
        self.label_background.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.textEdit_rules.raise_()
        self.textEdit_terms.raise_()
        self.textEdit_state.raise_()
        self.textEdit_name.raise_()
        self.pushButton_simulate.raise_()
        self.pushButton_verify.raise_()
        self.comboBox_veri_opt.raise_()
        self.textEdit_prop_spe.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.textBrowser_result.raise_()
        self.comboBox_detail.raise_()
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 993, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuSimulation = QtWidgets.QMenu(self.menubar)
        self.menuSimulation.setObjectName("menuSimulation")
        self.menuVerification = QtWidgets.QMenu(self.menubar)
        self.menuVerification.setObjectName("menuVerification")
        self.menuAbout_2 = QtWidgets.QMenu(self.menubar)
        self.menuAbout_2.setObjectName("menuAbout_2")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(self.MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(self.MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(self.MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSubsetSum = QtWidgets.QAction(self.MainWindow)
        self.actionSubsetSum.setObjectName("actionSubsetSum")
        self.actionThe_Hamiltonian_Path_cP_System = QtWidgets.QAction(self.MainWindow)
        self.actionThe_Hamiltonian_Path_cP_System.setObjectName("actionThe_Hamiltonian_Path_cP_System")
        self.actionPlaceholder = QtWidgets.QAction(self.MainWindow)
        self.actionPlaceholder.setObjectName("actionPlaceholder")
        self.actionVersion = QtWidgets.QAction(self.MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionRelease_Plan = QtWidgets.QAction(self.MainWindow)
        self.actionRelease_Plan.setObjectName("actionRelease_Plan")
        self.actionThe_GCD_cP_System = QtWidgets.QAction(self.MainWindow)
        self.actionThe_GCD_cP_System.setObjectName("actionThe_GCD_cP_System")
        self.actionThe_Hamitonian_Cycle_cP_System = QtWidgets.QAction(self.MainWindow)
        self.actionThe_Hamitonian_Cycle_cP_System.setObjectName("actionThe_Hamitonian_Cycle_cP_System")
        self.actioncP_System_ADD = QtWidgets.QAction(self.MainWindow)
        self.actioncP_System_ADD.setObjectName("actioncP_System_ADD")
        self.actioncP_System_Subtract = QtWidgets.QAction(self.MainWindow)
        self.actioncP_System_Subtract.setObjectName("actioncP_System_Subtract")
        self.actioncP_System_Multiplication = QtWidgets.QAction(self.MainWindow)
        self.actioncP_System_Multiplication.setObjectName("actioncP_System_Multiplication")
        self.actioncP_System_Division = QtWidgets.QAction(self.MainWindow)
        self.actioncP_System_Division.setObjectName("actioncP_System_Division")
        self.actionGCD_cP_System_2 = QtWidgets.QAction(self.MainWindow)
        self.actionGCD_cP_System_2.setObjectName("actionGCD_cP_System_2")
        self.actionEmail_Author = QtWidgets.QAction(self.MainWindow)
        self.actionEmail_Author.setObjectName("actionEmail_Author")
        self.actionNew = QtWidgets.QAction(self.MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave_As = QtWidgets.QAction(self.MainWindow)
        self.actionSave_As.setWhatsThis("")
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actioncP_System_ADD)
        self.menuAbout.addAction(self.actioncP_System_Subtract)
        self.menuAbout.addAction(self.actioncP_System_Multiplication)
        self.menuAbout.addAction(self.actioncP_System_Division)
        self.menuAbout.addAction(self.actionThe_GCD_cP_System)
        self.menuAbout.addAction(self.actionGCD_cP_System_2)
        self.menuAbout.addAction(self.actionSubsetSum)
        self.menuAbout.addAction(self.actionThe_Hamiltonian_Path_cP_System)
        self.menuAbout.addAction(self.actionThe_Hamitonian_Cycle_cP_System)
        self.menuAbout_2.addAction(self.actionVersion)
        self.menuAbout_2.addAction(self.actionEmail_Author)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menubar.addAction(self.menuVerification.menuAction())
        self.menubar.addAction(self.menuAbout_2.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
      
#Triggering the UI components        
        self.actionVersion.triggered.connect(self.ShowVersion)
        self.actionEmail_Author.triggered.connect(self.ShowAuthor)
        self.pushButton_simulate.clicked.connect(self.Simulate)
        self.pushButton_verify.clicked.connect(self.Verify)
        self.actionNew.triggered.connect(self.New)
        self.actionOpen.triggered.connect(self.Open)
        #self.comboBox_detail.currentIndexChanged.connect(self.Detail)
        
    def Simulate(self):
        self.ReloadcPSystem()
        with io.StringIO() as buf, redirect_stdout(buf):
            self.sys.Run()
            output = buf.getvalue()
            self.textBrowser_result.setText(output)
            
    def Verify(self):
        self.ReloadcPSystem()
        self.ve = CPVerifier(self.sys)
        with io.StringIO() as buf, redirect_stdout(buf):
            veri_opt = self.comboBox_veri_opt.currentIndex()
            if veri_opt == 0:
                self.ve.Verify()
            elif veri_opt == 1:
                self.ve.Verify(2)
            elif veri_opt == 2:
                self.ve.Verify(9)
            elif veri_opt == 3:
                self.ve.Verify(2)
            elif veri_opt == 4: #terms reachable
                raw_terms = self.textEdit_prop_spe.toPlainText()
                raw_terms2 = raw_terms.replace(' ','') 
                raw_terms3 = raw_terms2.replace('\n','')  
                dict_terms = re.split(';', raw_terms3)
                tar_terms = OrderedDict()
                for dict_term in dict_terms:
                    if (dict_term == '') or (not ':' in dict_term):
                        continue
                    [str_term, str_amount] = dict_term.split(':')
                    if ParseTerm(str_term) != '':
                        if ParseTerm(str_term) in tar_terms:
                            tar_terms[ParseTerm(str_term)] += int(str_amount)
                        else:
                            tar_terms[ParseTerm(str_term)] = int(str_amount)
                self.ve.SetTargetTerms(tar_terms)
                self.ve.Verify(8)
            elif veri_opt == 5: #terms eventually
                raw_terms = self.textEdit_prop_spe.toPlainText()
                raw_terms2 = raw_terms.replace(' ','') 
                raw_terms3 = raw_terms2.replace('\n','')  
                dict_terms = re.split(';', raw_terms3)
                tar_terms = OrderedDict()
                for dict_term in dict_terms:
                    if (dict_term == '') or (not ':' in dict_term):
                        continue
                    [str_term, str_amount] = dict_term.split(':')
                    if ParseTerm(str_term) != '':
                        if ParseTerm(str_term) in tar_terms:
                            tar_terms[ParseTerm(str_term)] += int(str_amount)
                        else:
                            tar_terms[ParseTerm(str_term)] = int(str_amount)
                self.ve.SetTargetTerms(tar_terms)
                self.ve.Verify(4)
            elif veri_opt == 6: #state reachable
                raw_state = self.textEdit_prop_spe.toPlainText()
                raw_state2 = raw_state.replace(' ','')
                self.ve.SetTargetState(raw_state2)
                self.ve.Verify(11)
            elif veri_opt == 7: #state eventually
                raw_state = self.textEdit_prop_spe.toPlainText()
                raw_state2 = raw_state.replace(' ','')
                self.ve.SetTargetState(raw_state2)
                self.ve.Verify(6)
            
            output = buf.getvalue()
            self.textBrowser_result.setText(output)
 
    def ReloadcPSystem(self):
        self.sys.ResetCPSystem()
        self.sys.SetSystemName(self.textEdit_name.toPlainText())
        state = self.textEdit_state.toPlainText()
        if state != '':
            self.sys.SetState(state.strip())
        else:
            self.sys.SetState('s1')
        raw_terms = self.textEdit_terms.toPlainText()
        raw_terms2 = raw_terms.replace(' ','') 
        raw_terms3 = raw_terms2.replace('\n','')  
        dict_terms = re.split(';', raw_terms3)
        for dict_term in dict_terms:
            if (dict_term == '') or (not ':' in dict_term):
                continue
            [str_term, str_amount] = dict_term.split(':') 
            if ParseTerm(str_term) != '':
                self.sys.AddSystemTerm(ParseTerm(str_term), int(str_amount))
        raw_rules = self.textEdit_rules.toPlainText()
        raw_rules2 = raw_rules.replace('\n','')
        rules = re.split(';', raw_rules2)
        for rule in rules:
            if rule == '':
                continue
            self.sys.AddRule(ParseRule(rule))
        if self.comboBox_detail.currentIndex() == 0:
            self.sys.DetailOff()
        elif self.comboBox_detail.currentIndex() == 1:
            self.sys.DetailOn()
        
    def ShowVersion(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('cPV')
        msg.setText('Version: ' + str(cpverifier.VERSION))
        msg.exec_()
        
    def ShowAuthor(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('cPV')
        msg.setText('Thanks for using cPV, if you found any bugs or got any questions, please feel free to contact yliu442@aucklanduni.ac.nz')
        msg.exec_()
            
    def Open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self.MainWindow,"QFileDialog.getOpenFileName()", "","cPVJ Files (*.json)", options=options)
        self.sys = ParsecPVJSON(path)
        self.textEdit_state.setText(self.sys.State())
        self.textEdit_name.setText(self.sys.SystemName())
        str_terms = ''
        for term in self.sys.SystemTerms():
            if isinstance(term, Term):      
                str_terms += term.ToString() + ':' + str(self.sys.SystemTerms()[term]) + ';\n'
            else:
                str_terms += term + ':' + str(self.sys.SystemTerms()[term]) + ';\n'
        self.textEdit_terms.setText(str_terms)
        str_rules = ''
        for rule in self.sys.Rules():
            str_rules += rule.ToString() + ';\n'
        self.textEdit_rules.setText(str_rules)
    
    def New(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "cPV - The cP System Verifier"))
        self.textEdit_rules.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; font-size:12pt; color:#448c27;\">Rules need to be separated by semicolons (;). In each rule, l-state, r-state, terms, ->1, ->+, and | need to be separated by whitespaces ( ). </span></p></body></html>"))
       
        self.textEdit_terms.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px; background-color:#f5f5f5;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; font-size:12pt; color:#448c27;\">Terms need to be written as key-value pairs, and be separated by semicolons (;). For example: a:1; f(bg(c)):2; 1: 3.</span></p></body></html>"))
       
        self.textEdit_state.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; color:#448c27;\">s1</span></p></body></html>"))
       
        self.textEdit_name.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; color:#448c27;\">Sample cP system</span></p></body></html>"))
        
        self.textEdit_prop_spe.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas\',\'Courier New\',\'monospace\'; color:#448c27;\">This textbox is only used for specifying certain system properties.</p></body></html>"))
      
        self.textBrowser_result.setText('')

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "cPV - The cP System Verifier"))
        self.label.setText(_translate("MainWindow", "cP system:"))
        self.label_3.setText(_translate("MainWindow", "Initial state:"))
        self.label_5.setText(_translate("MainWindow", "Initial terms:"))
        self.label_6.setText(_translate("MainWindow", "Rules:"))
        
        self.New()
        
        self.pushButton_simulate.setText(_translate("MainWindow", "Simulate"))
        self.pushButton_verify.setText(_translate("MainWindow", "Verify"))
        self.comboBox_veri_opt.setItemText(0, _translate("MainWindow", "Deadlockfree"))
        self.comboBox_veri_opt.setItemText(1, _translate("MainWindow", "Confluent"))
        self.comboBox_veri_opt.setItemText(2, _translate("MainWindow", "Terminating"))
        self.comboBox_veri_opt.setItemText(3, _translate("MainWindow", "Deterministic"))
        self.comboBox_veri_opt.setItemText(4, _translate("MainWindow", "Terms reachable"))
        self.comboBox_veri_opt.setItemText(5, _translate("MainWindow", "Terms eventually"))
        self.comboBox_veri_opt.setItemText(6, _translate("MainWindow", "State reachable"))
        self.comboBox_veri_opt.setItemText(7, _translate("MainWindow", "State eventually"))
         
        self.label_2.setText(_translate("MainWindow", "Additional specifications:"))
        self.label_4.setText(_translate("MainWindow", "Simulation / verification result:"))
        self.comboBox_detail.setItemText(0, _translate("MainWindow", "Detail level: 0"))
        self.comboBox_detail.setItemText(1, _translate("MainWindow", "Detail level: 1"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Examples"))
        self.menuSimulation.setTitle(_translate("MainWindow", "Simulation"))
        self.menuVerification.setTitle(_translate("MainWindow", "Verification"))
        self.menuAbout_2.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSubsetSum.setText(_translate("MainWindow", "The Subset Sum cP System"))
        self.actionThe_Hamiltonian_Path_cP_System.setText(_translate("MainWindow", "The Hamiltonian Path cP System"))
        self.actionPlaceholder.setText(_translate("MainWindow", "Placeholder"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionRelease_Plan.setText(_translate("MainWindow", "Release Plan"))
        self.actionThe_GCD_cP_System.setText(_translate("MainWindow", "GCD cP System 1"))
        self.actionThe_Hamitonian_Cycle_cP_System.setText(_translate("MainWindow", "The Hamiltonian Cycle cP System"))
        self.actioncP_System_ADD.setText(_translate("MainWindow", "cP System: Add"))
        self.actioncP_System_Subtract.setText(_translate("MainWindow", "cP System: Subtract"))
        self.actioncP_System_Multiplication.setText(_translate("MainWindow", "cP System: Multiplication"))
        self.actioncP_System_Division.setText(_translate("MainWindow", "cP System: Division"))
        self.actionGCD_cP_System_2.setText(_translate("MainWindow", "GCD cP System 2"))
        self.actionEmail_Author.setText(_translate("MainWindow", "Contact the author"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Alt+A"))