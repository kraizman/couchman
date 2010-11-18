# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_task.ui'
#
# Created: Thu Nov 18 13:34:42 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_New_Task_Form(object):
    def setupUi(self, New_Task_Form):
        New_Task_Form.setObjectName(_fromUtf8("New_Task_Form"))
        New_Task_Form.setWindowModality(QtCore.Qt.NonModal)
        New_Task_Form.resize(600, 154)
        self.verticalLayout = QtGui.QVBoxLayout(New_Task_Form)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(New_Task_Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.txt_source = QtGui.QLineEdit(New_Task_Form)
        self.txt_source.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_source.setFrame(True)
        self.txt_source.setObjectName(_fromUtf8("txt_source"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.txt_source)
        self.lbl_group_2 = QtGui.QLabel(New_Task_Form)
        self.lbl_group_2.setObjectName(_fromUtf8("lbl_group_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_group_2)
        self.txt_target = QtGui.QLineEdit(New_Task_Form)
        self.txt_target.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_target.setObjectName(_fromUtf8("txt_target"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.txt_target)
        self.label_4 = QtGui.QLabel(New_Task_Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txt_proxy = QtGui.QLineEdit(New_Task_Form)
        self.txt_proxy.setObjectName(_fromUtf8("txt_proxy"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.txt_proxy)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_save = QtGui.QPushButton(New_Task_Form)
        self.btn_save.setMinimumSize(QtCore.QSize(120, 0))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.btn_cancel = QtGui.QPushButton(New_Task_Form)
        self.btn_cancel.setMinimumSize(QtCore.QSize(120, 0))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(New_Task_Form)
        QtCore.QMetaObject.connectSlotsByName(New_Task_Form)

    def retranslateUi(self, New_Task_Form):
        New_Task_Form.setWindowTitle(QtGui.QApplication.translate("New_Task_Form", "Add New Task", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("New_Task_Form", "Source addres:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_group_2.setText(QtGui.QApplication.translate("New_Task_Form", "Target addres:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("New_Task_Form", "Proxy:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save.setText(QtGui.QApplication.translate("New_Task_Form", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("New_Task_Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
