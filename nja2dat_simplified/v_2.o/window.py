# -*- coding: utf8 -*-
from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(690, 470)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		MainWindow.setMenuBar(self.menubar)
		
				
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		
		self.actionOpen_file = QtGui.QAction(MainWindow)
		self.actionOpen_file.setObjectName(_fromUtf8("actionOpen_file"))
		self.menuFile.addAction(self.actionOpen_file)
		self.menubar.addAction(self.menuFile.menuAction())
		
		self.sfont = QtGui.QFont(MainWindow)#,"Courier New")   #setting up a font 
		self.sfont.setFamily("Courier New")
		self.sfont.setItalic(True)
		self.sfont.setPixelSize(100)
		
		self.biglabel=QtGui.QLabel(MainWindow)
		self.biglabel.setGeometry(QtCore.QRect(50,40,500,110))
		self.biglabel.setObjectName(_fromUtf8("biglabel"))
		self.biglabel.setFont(self.sfont)
		
		self.lepicbig = QtGui.QLabel(MainWindow)
		self.lepicbig.setGeometry(QtCore.QRect(500,20,500,150))
		self.lepicbig.setPixmap(QtGui.QPixmap("pepper_icon2.png"))
		
		a=150
		
		# self.sfont = QtGui.QFont(MainWindow)   #setting up a font 
		# self.sfont.setPixelSize(100)
		# self.le.setFont(self.sfont)			#including it inside the label with this line
		
		self.le = QtGui.QLabel(MainWindow)
		self.le.setGeometry(QtCore.QRect(100, 20+a, 560, 20))
		self.le.setObjectName(_fromUtf8("~~the chosen file will be displayed here~~"))
		
		self.pushButton1 = QtGui.QPushButton(MainWindow)
		self.pushButton1.setGeometry(QtCore.QRect(20, 20+a, 70, 20))
		self.pushButton1.setObjectName(_fromUtf8("Choose a file"))
		
		self.textEdit = QtGui.QTextEdit(MainWindow)
		self.textEdit.setGeometry(QtCore.QRect(100, 40+a, 560, 50))
		self.textEdit.setObjectName(_fromUtf8("Snippet"))
		
		self.pushButton2 = QtGui.QPushButton(MainWindow)
		self.pushButton2.setGeometry(QtCore.QRect(20, 90+a, 70, 20))
		self.pushButton2.setObjectName(_fromUtf8("Nja2Dat"))
		
		self.pushButton4 = QtGui.QPushButton(MainWindow)
		self.pushButton4.setGeometry(QtCore.QRect(20, 230+a, 70, 20))
		self.pushButton4.setObjectName(_fromUtf8("Plot All"))
		
		# self.pushButton5 = QtGui.QPushButton(MainWindow)
		# self.pushButton5.setGeometry(QtCore.QRect(20, 320, 70, 20))
		# self.pushButton5.setObjectName(_fromUtf8("Autoindex"))
		
		self.label = QtGui.QLabel(MainWindow)
		self.label.setGeometry(QtCore.QRect(100, 90+a, 370, 20))
		self.label.setObjectName(_fromUtf8("correction function"))
		
		self.password = QtGui.QPushButton(MainWindow)
		self.password.setGeometry(QtCore.QRect(570, 90+a, 90, 20))
		self.password.setObjectName(_fromUtf8("password"))
		
		self.textEdit2 = QtGui.QTextEdit(MainWindow)
		self.textEdit2.setGeometry(QtCore.QRect(100, 140+a, 560, 50))
		self.textEdit2.setObjectName(_fromUtf8("Snippet2"))
			
		self.msgBox3 = QtGui.QMessageBox(MainWindow)
		self.msgBox3.setObjectName(_fromUtf8("Box3"))
		
		self.label2 = QtGui.QLabel(MainWindow)
		self.label2.setGeometry(QtCore.QRect(20, 190+a, 570, 50))
		self.label2.setObjectName(_fromUtf8("Interpolation suggestion"))
		
		self.labelA = QtGui.QLabel(MainWindow)
		self.labelA.setGeometry(QtCore.QRect(100, 95+a, 100, 50))
		self.labelA.setObjectName(_fromUtf8("Number A is : "))
		self.labelB = QtGui.QLabel(MainWindow)
		self.labelB.setGeometry(QtCore.QRect(100, 110+a, 200, 50))
		self.labelB.setObjectName(_fromUtf8("Number B is : "))
		self.labelAnum = QtGui.QLabel(MainWindow)
		self.labelAnum.setGeometry(QtCore.QRect(200, 95+a, 100, 50))
		self.labelAnum.setObjectName(_fromUtf8("numA"))
		self.labelBnum = QtGui.QLabel(MainWindow)
		self.labelBnum.setGeometry(QtCore.QRect(200, 110+a, 200, 50))
		self.labelBnum.setObjectName(_fromUtf8("numB"))
		
		self.lepic = QtGui.QLabel(MainWindow)
		self.lepic.setGeometry(QtCore.QRect(115, 250+a, 570, 180))

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "Nja2dat_(with correction and interpolation)", None))
		self.menuFile.setTitle(_translate("MainWindow", "About", None))
		self.actionOpen_file.setText(_translate("MainWindow", "\n Gui by Balazs Kocsis :: b.kocis@lmu.de \n or \n balaz.kocis@gmail.com \n tel: 4314", None))
		self.le.setText(_translate("MainWindow","~~the chosen file will be displayed here~~",None))
		self.pushButton1.setText(_translate("MainWindow","Choose a file",None))
		self.textEdit.setText(_translate("MainWindow","look inside the file",None))
		self.pushButton2.setText(_translate("MainWindow","Nja2dat",None))
		self.pushButton4.setText(_translate("MainWindow","Plot All",None))
	#	self.pushButton5.setText(_translate("MainWindow","Autoindex",None))
		self.textEdit2.setText(_translate("MainWindow","look inside the file",None))
		self.msgBox3.setText(_translate("MainWindow","A file with interpolations has been generated and saved with _corr_interp_spline.dat next to your file!",None))
		self.label.setText(_translate("MainWindow",u"2θ_corr = 2θ_mess - (A - B * 2θ_mess) ; for 2θ<60°",None))
		self.password.setText(_translate("MainWindow","Change",None))
		self.label2.setText(_translate("MainWindow","A spline interpolation was done on the data giving equidistant stepsize.\n ",None))
		self.labelA.setText(_translate("MainWindow","Number A is : ",None))
		self.labelB.setText(_translate("MainWindow","Number B is : ",None))
		self.labelAnum.setText(_translate("MainWindow","....",None))
		self.labelBnum.setText(_translate("MainWindow","....",None))
		self.biglabel.setText(_translate("MainWindow","Nja2dat",None))

#from matplotlibwidgetFile import matplotlibWidget