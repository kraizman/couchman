# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Nov  4 16:04:34 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(840, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tlw_servers = ServersList(self.layoutWidget)
        self.tlw_servers.setAlternatingRowColors(True)
        self.tlw_servers.setRootIsDecorated(False)
        self.tlw_servers.setUniformRowHeights(True)
        self.tlw_servers.setItemsExpandable(False)
        self.tlw_servers.setSortingEnabled(True)
        self.tlw_servers.setWordWrap(True)
        self.tlw_servers.setObjectName(_fromUtf8("tlw_servers"))
        self.verticalLayout_2.addWidget(self.tlw_servers)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_addserver = QtGui.QToolButton(self.layoutWidget)
        self.btn_addserver.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_addserver.setObjectName(_fromUtf8("btn_addserver"))
        self.gridLayout_2.addWidget(self.btn_addserver, 0, 0, 1, 1)
        self.btn_rmserver = QtGui.QToolButton(self.layoutWidget)
        self.btn_rmserver.setEnabled(True)
        self.btn_rmserver.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_rmserver.setObjectName(_fromUtf8("btn_rmserver"))
        self.gridLayout_2.addWidget(self.btn_rmserver, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 4, 1, 1)
        self.btn_editserver = QtGui.QToolButton(self.layoutWidget)
        self.btn_editserver.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_editserver.setObjectName(_fromUtf8("btn_editserver"))
        self.gridLayout_2.addWidget(self.btn_editserver, 0, 2, 1, 1)
        self.btn_dbmanager = QtGui.QToolButton(self.layoutWidget)
        self.btn_dbmanager.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_dbmanager.setObjectName(_fromUtf8("btn_dbmanager"))
        self.gridLayout_2.addWidget(self.btn_dbmanager, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_3.setVerticalSpacing(10)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lbl_srv_group = QtGui.QLabel(self.layoutWidget1)
        self.lbl_srv_group.setObjectName(_fromUtf8("lbl_srv_group"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.lbl_srv_group)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lbl_srv_name = QtGui.QLabel(self.layoutWidget1)
        self.lbl_srv_name.setObjectName(_fromUtf8("lbl_srv_name"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.lbl_srv_name)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lbl_srv_addres = QtGui.QLabel(self.layoutWidget1)
        self.lbl_srv_addres.setCursor(QtCore.Qt.PointingHandCursor)
        self.lbl_srv_addres.setMouseTracking(True)
        self.lbl_srv_addres.setTextFormat(QtCore.Qt.AutoText)
        self.lbl_srv_addres.setOpenExternalLinks(True)
        self.lbl_srv_addres.setObjectName(_fromUtf8("lbl_srv_addres"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.lbl_srv_addres)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lbl_status = QtGui.QLabel(self.layoutWidget1)
        self.lbl_status.setObjectName(_fromUtf8("lbl_status"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.lbl_status)
        self.label_6 = QtGui.QLabel(self.layoutWidget1)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lbl_period = QtGui.QLabel(self.layoutWidget1)
        self.lbl_period.setObjectName(_fromUtf8("lbl_period"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.lbl_period)
        self.label_5 = QtGui.QLabel(self.layoutWidget1)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lbl_lastupdate = QtGui.QLabel(self.layoutWidget1)
        self.lbl_lastupdate.setObjectName(_fromUtf8("lbl_lastupdate"))
        self.horizontalLayout_4.addWidget(self.lbl_lastupdate)
        self.btn_refresh_sel = QtGui.QToolButton(self.layoutWidget1)
        self.btn_refresh_sel.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_refresh_sel.setObjectName(_fromUtf8("btn_refresh_sel"))
        self.horizontalLayout_4.addWidget(self.btn_refresh_sel)
        self.formLayout_3.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.horizontalLayout_3.addLayout(self.formLayout_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tlw_replications = ServersList(self.layoutWidget1)
        self.tlw_replications.setAlternatingRowColors(True)
        self.tlw_replications.setRootIsDecorated(False)
        self.tlw_replications.setObjectName(_fromUtf8("tlw_replications"))
        self.verticalLayout.addWidget(self.tlw_replications)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btn_addtask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_addtask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_addtask.setObjectName(_fromUtf8("btn_addtask"))
        self.horizontalLayout_2.addWidget(self.btn_addtask)
        self.btn_rmtask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_rmtask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_rmtask.setObjectName(_fromUtf8("btn_rmtask"))
        self.horizontalLayout_2.addWidget(self.btn_rmtask)
        self.btn_starttask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_starttask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_starttask.setObjectName(_fromUtf8("btn_starttask"))
        self.horizontalLayout_2.addWidget(self.btn_starttask)
        self.btn_start_con = QtGui.QToolButton(self.layoutWidget1)
        self.btn_start_con.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_start_con.setObjectName(_fromUtf8("btn_start_con"))
        self.horizontalLayout_2.addWidget(self.btn_start_con)
        self.btn_stoptask = QtGui.QToolButton(self.layoutWidget1)
        self.btn_stoptask.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_stoptask.setObjectName(_fromUtf8("btn_stoptask"))
        self.horizontalLayout_2.addWidget(self.btn_stoptask)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionAdd_Server = QtGui.QAction(MainWindow)
        self.actionAdd_Server.setObjectName(_fromUtf8("actionAdd_Server"))
        self.actionRemove_Server = QtGui.QAction(MainWindow)
        self.actionRemove_Server.setObjectName(_fromUtf8("actionRemove_Server"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Replication Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_addserver.setToolTip(QtGui.QApplication.translate("MainWindow", "Add server record to persisted list", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_addserver.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rmserver.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove server record from persisted list", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rmserver.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_editserver.setToolTip(QtGui.QApplication.translate("MainWindow", "Edit server record", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_editserver.setText(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_dbmanager.setToolTip(QtGui.QApplication.translate("MainWindow", "Documents manager", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_dbmanager.setText(QtGui.QApplication.translate("MainWindow", "DB manager", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_srv_group.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_srv_name.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Addres:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_srv_addres.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_status.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Update period: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_period.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Last update:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_lastupdate.setText(QtGui.QApplication.translate("MainWindow", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_refresh_sel.setText(QtGui.QApplication.translate("MainWindow", "Refresh now", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_addtask.setToolTip(QtGui.QApplication.translate("MainWindow", "Add replication record to persisted list", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_addtask.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rmtask.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove replication record from persisted list", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rmtask.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_starttask.setToolTip(QtGui.QApplication.translate("MainWindow", "Start persisted replication", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_starttask.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start_con.setText(QtGui.QApplication.translate("MainWindow", "Start as continuous", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stoptask.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop runing replication", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stoptask.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Server.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Server.setToolTip(QtGui.QApplication.translate("MainWindow", "Add new Server", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Server.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Server.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove_Server.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))

from list_prototype import ServersList