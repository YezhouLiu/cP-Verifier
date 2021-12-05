from typing import OrderedDict
from term import Term
from PyQt5 import QtCore, QtGui, QtWidgets
import io, re
import cpverifier
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
#FUNCTION CODE       
    def __init__(self):
        self.sys = CPSystem()
        self.ve = CPVerifier(self.sys)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1475, 802)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(30, 30, 111, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 171, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 200, 141, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 360, 81, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textEdit_rules = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_rules.setGeometry(QtCore.QRect(30, 390, 541, 361))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_rules.setFont(font)
        self.textEdit_rules.setObjectName("textEdit_rules")
        self.textEdit_terms = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_terms.setGeometry(QtCore.QRect(30, 230, 541, 111))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_terms.setFont(font)
        self.textEdit_terms.setToolTip("")
        self.textEdit_terms.setToolTipDuration(-1)
        self.textEdit_terms.setObjectName("textEdit_terms")
        self.textEdit_state = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_state.setGeometry(QtCore.QRect(160, 90, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_state.setFont(font)
        self.textEdit_state.setObjectName("textEdit_state")
        self.textEdit_name = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_name.setGeometry(QtCore.QRect(160, 30, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_name.setFont(font)
        self.textEdit_name.setObjectName("textEdit_name")
        self.pushButton_simulate = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_simulate.setGeometry(QtCore.QRect(600, 10, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_simulate.setFont(font)
        self.pushButton_simulate.setObjectName("pushButton_simulate")
        self.pushButton_verify = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_verify.setGeometry(QtCore.QRect(1060, 10, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_verify.setFont(font)
        self.pushButton_verify.setObjectName("pushButton_verify")
        self.comboBox_property = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_property.setGeometry(QtCore.QRect(1220, 120, 221, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.comboBox_property.setFont(font)
        self.comboBox_property.setStatusTip("")
        self.comboBox_property.setObjectName("comboBox_property")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.comboBox_property.addItem("")
        self.textEdit_spec = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_spec.setGeometry(QtCore.QRect(1060, 190, 381, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_spec.setFont(font)
        self.textEdit_spec.setObjectName("textEdit_spec")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1060, 160, 201, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(600, 290, 341, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.textBrowser_result = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_result.setGeometry(QtCore.QRect(600, 320, 841, 431))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textBrowser_result.setFont(font)
        self.textBrowser_result.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.textBrowser_result.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textBrowser_result.setLineWidth(1)
        self.textBrowser_result.setMidLineWidth(0)
        self.textBrowser_result.setObjectName("textBrowser_result")
        self.comboBox_detail = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_detail.setGeometry(QtCore.QRect(600, 80, 251, 29))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.comboBox_detail.setFont(font)
        self.comboBox_detail.setStatusTip("")
        self.comboBox_detail.setObjectName("comboBox_detail")
        self.comboBox_detail.addItem("")
        self.comboBox_detail.addItem("")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1060, 120, 141, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1060, 80, 151, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.textEdit_state_limit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_state_limit.setGeometry(QtCore.QRect(1220, 80, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_state_limit.setFont(font)
        self.textEdit_state_limit.setObjectName("textEdit_state_limit")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(600, 160, 201, 24))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.textEdit_halting_states = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_halting_states.setGeometry(QtCore.QRect(600, 190, 381, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.textEdit_halting_states.setFont(font)
        self.textEdit_halting_states.setObjectName("textEdit_halting_states")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1475, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAbout_2 = QtWidgets.QMenu(self.menubar)
        self.menuAbout_2.setObjectName("menuAbout_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        #self.actionQuit = QtWidgets.QAction(MainWindow)
        #self.actionQuit.setObjectName("actionQuit")
        self.actionSubset_Sum_cP_System = QtWidgets.QAction(MainWindow)
        self.actionSubset_Sum_cP_System.setObjectName("actionSubset_Sum_cP_System")
        self.actionThe_Hamiltonian_Path_cP_System = QtWidgets.QAction(MainWindow)
        self.actionThe_Hamiltonian_Path_cP_System.setObjectName("actionThe_Hamiltonian_Path_cP_System")
        self.actionPlaceholder = QtWidgets.QAction(MainWindow)
        self.actionPlaceholder.setObjectName("actionPlaceholder")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actionRelease_Plan = QtWidgets.QAction(MainWindow)
        self.actionRelease_Plan.setObjectName("actionRelease_Plan")
        self.actionThe_GCD_cP_System = QtWidgets.QAction(MainWindow)
        self.actionThe_GCD_cP_System.setObjectName("actionThe_GCD_cP_System")
        self.actionThe_Hamitonian_Cycle_cP_System = QtWidgets.QAction(MainWindow)
        self.actionThe_Hamitonian_Cycle_cP_System.setObjectName("actionThe_Hamitonian_Cycle_cP_System")
        self.actioncP_System_ADD = QtWidgets.QAction(MainWindow)
        self.actioncP_System_ADD.setObjectName("actioncP_System_ADD")
        self.actioncP_System_Subtract = QtWidgets.QAction(MainWindow)
        self.actioncP_System_Subtract.setObjectName("actioncP_System_Subtract")
        self.actioncP_System_Multiplication = QtWidgets.QAction(MainWindow)
        self.actioncP_System_Multiplication.setObjectName("actioncP_System_Multiplication")
        self.actioncP_System_Division = QtWidgets.QAction(MainWindow)
        self.actioncP_System_Division.setObjectName("actioncP_System_Division")
        self.actionGCD_cP_System_2 = QtWidgets.QAction(MainWindow)
        self.actionGCD_cP_System_2.setObjectName("actionGCD_cP_System_2")
        self.actionContact_Author = QtWidgets.QAction(MainWindow)
        self.actionContact_Author.setObjectName("actionContact_Author")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        #self.actionSave_As = QtWidgets.QAction(MainWindow)
        #self.actionSave_As.setWhatsThis("")
        #self.actionSave_As.setObjectName("actionSave_As")
        self.actionSimulate = QtWidgets.QAction(MainWindow)
        self.actionSimulate.setObjectName("actionSimulate")
        self.actionVerify = QtWidgets.QAction(MainWindow)
        self.actionVerify.setObjectName("actionVerify")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        #self.menuFile.addAction(self.actionSave_As)
        #self.menuFile.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actioncP_System_ADD)
        self.menuAbout.addAction(self.actioncP_System_Subtract)
        self.menuAbout.addAction(self.actioncP_System_Multiplication)
        self.menuAbout.addAction(self.actioncP_System_Division)
        self.menuAbout.addAction(self.actionThe_GCD_cP_System)
        self.menuAbout.addAction(self.actionGCD_cP_System_2)
        self.menuAbout.addAction(self.actionSubset_Sum_cP_System)
        self.menuAbout.addAction(self.actionThe_Hamiltonian_Path_cP_System)
        self.menuAbout.addAction(self.actionThe_Hamitonian_Cycle_cP_System)
        self.menuAbout_2.addAction(self.actionVersion)
        self.menuAbout_2.addAction(self.actionContact_Author)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuAbout_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#FUNCTION CODE 
        self.actionVersion.triggered.connect(self.ShowVersion)
        self.actionContact_Author.triggered.connect(self.ShowAuthor)
        self.pushButton_simulate.clicked.connect(self.Simulate)
        self.pushButton_verify.clicked.connect(self.Verify)
        self.actionNew.triggered.connect(self.New)
        self.actionOpen.triggered.connect(self.Open)
        self.actionSave.triggered.connect(self.Save)

    def Simulate(self):
        self.ReloadcPSystem()
        with io.StringIO() as buf, redirect_stdout(buf):
            self.sys.Run()
            output = buf.getvalue()
            self.textBrowser_result.setText(output)
        self.statusbar.showMessage("Done")
        
    def Verify(self):
        self.ReloadcPSystem()
        self.ve = CPVerifier(self.sys)
        if self.comboBox_detail.currentIndex() == 0:
            self.ve.DetailOff()
        elif self.comboBox_detail.currentIndex() == 1:
            self.ve.DetailOn()
        with io.StringIO() as buf, redirect_stdout(buf):
            veri_opt = self.comboBox_property.currentIndex()
            if veri_opt == 0:
                raw_halting_states = self.textEdit_halting_states.toPlainText()
                raw_halting_states1 = raw_halting_states.replace(' ','')
                raw_halting_states2 = raw_halting_states1.replace('\n','')
                halting_states = re.split(';|,', raw_halting_states2)
                halting_states1 = []
                for state in halting_states:
                    if len(state) > 0:
                        halting_states1.append(state)
                self.ve.SetTerminations(halting_states1)
                self.ve.Verify()
            elif veri_opt == 1:
                self.ve.Verify(2)
            elif veri_opt == 2:
                self.ve.Verify(9)
            elif veri_opt == 3:
                self.ve.Verify(2)
            elif veri_opt == 4: #terms reachable
                raw_terms = self.textEdit_spec.toPlainText()
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
                raw_terms = self.textEdit_spec.toPlainText()
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
                raw_state = self.textEdit_spec.toPlainText()
                raw_state2 = raw_state.replace(' ','')
                self.ve.SetTargetState(raw_state2)
                self.ve.Verify(11)
            elif veri_opt == 7: #state eventually
                raw_state = self.textEdit_spec.toPlainText()
                raw_state2 = raw_state.replace(' ','')
                self.ve.SetTargetState(raw_state2)
                self.ve.Verify(6)
            
            output = buf.getvalue()
            self.textBrowser_result.setText(output)
        self.statusbar.showMessage("Done")
 
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
        path, _ = QFileDialog.getOpenFileName(MainWindow,"QFileDialog.getOpenFileName()", "","cPVJ Files (*.json)", options=options)
        try:
            self.sys = ParsecPVJSON(path)
        except:
            return False
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
        return True
    
    def Save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(MainWindow,"QFileDialog.getSaveFileName()","","cPVJ Files (*.JSON)", options=options)
        if fileName:
            if fileName[-5:].lower() != '.json':
                fileName += '.json'
        self.ReloadcPSystem()
        try:
            f = open(fileName, 'w')
        except:
            return False
        cPVJ_str = '{\n \"ruleset\": ['
        for rule in self.sys.Rules():
            cPVJ_str += '\"' + rule.ToString() + '\",\n'
        if len(self.sys.Rules()) > 0:
            cPVJ_str = cPVJ_str[:-2] + '],\n'
        else:
            cPVJ_str += '],\n'
        cPVJ_str += '\"terms\": {'
        for term in self.sys.SystemTerms():
            if isinstance(term, Term):
                cPVJ_str += '\"' + term.ToString() + '\":' + str(self.sys.SystemTerms()[term]) + ',\n'
            else:
                cPVJ_str += '\"' + term + '\":' + str(self.sys.SystemTerms()[term]) + ',\n'
        if len(self.sys.SystemTerms()) > 0:
            cPVJ_str = cPVJ_str[:-2] + '},\n'
        else:
            cPVJ_str += '},\n'
        cPVJ_str += '\"state\": \"' + self.sys.State() + '\",\n'
        cPVJ_str += '\"name\": \"' + self.sys.SystemName() + '\"\n'
        cPVJ_str += '}'
        f.write(cPVJ_str)
        f.close()
        return True
    
    def New(self):
        self.textEdit_name.setText('')
        self.textEdit_state.setText('')
        self.textEdit_terms.setText('')
        self.textEdit_rules.setText('')
        self.textBrowser_result.setText('')
        self.textEdit_spec.setText('')
        self.textEdit_state_limit.setText('100000')
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "cPV - The cP System Verifier"))
        self.label_1.setText(_translate("MainWindow", "cP system:"))
        self.label_2.setText(_translate("MainWindow", "Initial state:"))
        self.label_3.setText(_translate("MainWindow", "Initial terms:"))
        self.label_4.setText(_translate("MainWindow", "Rules:"))
        self.textEdit_rules.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\'; font-size:18pt;\"><br /></p></body></html>"))
        self.textEdit_terms.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22px; font-family:\'SimSun\'; font-size:18pt; background-color:#f5f5f5;\"><br /></p></body></html>"))
        self.textEdit_state.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_name.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_simulate.setText(_translate("MainWindow", "Simulate"))
        self.pushButton_verify.setText(_translate("MainWindow", "Verify"))
        self.comboBox_property.setItemText(0, _translate("MainWindow", "Deadlockfree"))
        self.comboBox_property.setItemText(1, _translate("MainWindow", "Confluent"))
        self.comboBox_property.setItemText(2, _translate("MainWindow", "Terminating"))
        self.comboBox_property.setItemText(3, _translate("MainWindow", "Deterministic"))
        self.comboBox_property.setItemText(4, _translate("MainWindow", "Terms reachable"))
        self.comboBox_property.setItemText(5, _translate("MainWindow", "Terms eventually"))
        self.comboBox_property.setItemText(6, _translate("MainWindow", "State reachable"))
        self.comboBox_property.setItemText(7, _translate("MainWindow", "State eventually"))
        self.textEdit_spec.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "Additional specifications:"))
        self.label_5.setText(_translate("MainWindow", "Simulation / verification result:"))
        self.comboBox_detail.setItemText(0, _translate("MainWindow", "Detail level: 0"))
        self.comboBox_detail.setItemText(1, _translate("MainWindow", "Detail level: 1"))
        self.label_7.setText(_translate("MainWindow", "System property:"))
        self.label_6.setText(_translate("MainWindow", "Statespace limit:"))
        self.textEdit_state_limit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">100000</p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "Expected halting states:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.textEdit_halting_states.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        
        self.menuAbout.setTitle(_translate("MainWindow", "Examples"))
        self.menuAbout_2.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        #self.actionQuit.setText(_translate("MainWindow", "Quit"))
        #self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionSubset_Sum_cP_System.setText(_translate("MainWindow", "The Subset Sum cP System"))
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
        self.actionContact_Author.setText(_translate("MainWindow", "Contact Author"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        #self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        #self.actionSave_As.setShortcut(_translate("MainWindow", "Alt+A"))
        self.actionSimulate.setText(_translate("MainWindow", "Simulate"))
        self.actionVerify.setText(_translate("MainWindow", "Verify"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())