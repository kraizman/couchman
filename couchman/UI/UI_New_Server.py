# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created: Thu Oct 28 10:05:09 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AddServerForm(object):
    def setupUi(self, AddServerForm):
        AddServerForm.setObjectName(_fromUtf8("AddServerForm"))
        AddServerForm.setWindowModality(QtCore.Qt.NonModal)
        AddServerForm.resize(364, 540)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddServerForm.sizePolicy().hasHeightForWidth())
        AddServerForm.setSizePolicy(sizePolicy)
        AddServerForm.setMinimumSize(QtCore.QSize(0, 0))
        AddServerForm.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(AddServerForm)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.chb_enabled = QtGui.QCheckBox(AddServerForm)
        self.chb_enabled.setChecked(True)
        self.chb_enabled.setObjectName(_fromUtf8("chb_enabled"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.chb_enabled)
        self.label = QtGui.QLabel(AddServerForm)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.txt_name = QtGui.QLineEdit(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_name.sizePolicy().hasHeightForWidth())
        self.txt_name.setSizePolicy(sizePolicy)
        self.txt_name.setObjectName(_fromUtf8("txt_name"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.txt_name)
        self.lbl_group = QtGui.QLabel(AddServerForm)
        self.lbl_group.setObjectName(_fromUtf8("lbl_group"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_group)
        self.cmb_group = QtGui.QComboBox(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmb_group.sizePolicy().hasHeightForWidth())
        self.cmb_group.setSizePolicy(sizePolicy)
        self.cmb_group.setMinimumSize(QtCore.QSize(150, 0))
        self.cmb_group.setEditable(True)
        self.cmb_group.setObjectName(_fromUtf8("cmb_group"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmb_group)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lbl_url = QtGui.QLabel(AddServerForm)
        self.lbl_url.setOpenExternalLinks(True)
        self.lbl_url.setObjectName(_fromUtf8("lbl_url"))
        self.horizontalLayout_3.addWidget(self.lbl_url)
        self.txt_url = QtGui.QLineEdit(AddServerForm)
        self.txt_url.setObjectName(_fromUtf8("txt_url"))
        self.horizontalLayout_3.addWidget(self.txt_url)
        self.btn_parse = QtGui.QToolButton(AddServerForm)
        self.btn_parse.setObjectName(_fromUtf8("btn_parse"))
        self.horizontalLayout_3.addWidget(self.btn_parse)
        self.btn_test = QtGui.QToolButton(AddServerForm)
        self.btn_test.setObjectName(_fromUtf8("btn_test"))
        self.horizontalLayout_3.addWidget(self.btn_test)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.grp_login = QtGui.QGroupBox(AddServerForm)
        self.grp_login.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grp_login.sizePolicy().hasHeightForWidth())
        self.grp_login.setSizePolicy(sizePolicy)
        self.grp_login.setFlat(False)
        self.grp_login.setCheckable(True)
        self.grp_login.setChecked(False)
        self.grp_login.setObjectName(_fromUtf8("grp_login"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grp_login)
        self.verticalLayout_2.setMargin(5)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_4 = QtGui.QLabel(self.grp_login)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.txt_login = QtGui.QLineEdit(self.grp_login)
        self.txt_login.setObjectName(_fromUtf8("txt_login"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.txt_login)
        self.label_5 = QtGui.QLabel(self.grp_login)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.txt_password = QtGui.QLineEdit(self.grp_login)
        self.txt_password.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.txt_password.setInputMask(_fromUtf8(""))
        self.txt_password.setMaxLength(32767)
        self.txt_password.setEchoMode(QtGui.QLineEdit.Password)
        self.txt_password.setObjectName(_fromUtf8("txt_password"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.txt_password)
        self.chb_showpass = QtGui.QCheckBox(self.grp_login)
        self.chb_showpass.setObjectName(_fromUtf8("chb_showpass"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.chb_showpass)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout.addWidget(self.grp_login)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.cmb_protocol = QtGui.QComboBox(AddServerForm)
        self.cmb_protocol.setObjectName(_fromUtf8("cmb_protocol"))
        self.cmb_protocol.addItem(_fromUtf8(""))
        self.cmb_protocol.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_protocol)
        self.label_2 = QtGui.QLabel(AddServerForm)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.txt_host = QtGui.QLineEdit(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_host.sizePolicy().hasHeightForWidth())
        self.txt_host.setSizePolicy(sizePolicy)
        self.txt_host.setMinimumSize(QtCore.QSize(200, 0))
        self.txt_host.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.txt_host.setObjectName(_fromUtf8("txt_host"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.txt_host)
        self.label_3 = QtGui.QLabel(AddServerForm)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.spin_port = QtGui.QSpinBox(AddServerForm)
        self.spin_port.setMinimumSize(QtCore.QSize(80, 0))
        self.spin_port.setFrame(True)
        self.spin_port.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_port.setAccelerated(False)
        self.spin_port.setMinimum(1)
        self.spin_port.setMaximum(65535)
        self.spin_port.setProperty(_fromUtf8("value"), 5984)
        self.spin_port.setObjectName(_fromUtf8("spin_port"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.spin_port)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.group_autoupdate = QtGui.QGroupBox(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_autoupdate.sizePolicy().hasHeightForWidth())
        self.group_autoupdate.setSizePolicy(sizePolicy)
        self.group_autoupdate.setMinimumSize(QtCore.QSize(0, 45))
        self.group_autoupdate.setFlat(True)
        self.group_autoupdate.setCheckable(True)
        self.group_autoupdate.setObjectName(_fromUtf8("group_autoupdate"))
        self.spin_time = QtGui.QDoubleSpinBox(self.group_autoupdate)
        self.spin_time.setGeometry(QtCore.QRect(0, 20, 150, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spin_time.sizePolicy().hasHeightForWidth())
        self.spin_time.setSizePolicy(sizePolicy)
        self.spin_time.setMinimumSize(QtCore.QSize(120, 20))
        self.spin_time.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_time.setDecimals(1)
        self.spin_time.setMaximum(10000000.0)
        self.spin_time.setProperty(_fromUtf8("value"), 5.0)
        self.spin_time.setObjectName(_fromUtf8("spin_time"))
        self.verticalLayout.addWidget(self.group_autoupdate)
        self.group_proxy = QtGui.QGroupBox(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_proxy.sizePolicy().hasHeightForWidth())
        self.group_proxy.setSizePolicy(sizePolicy)
        self.group_proxy.setMinimumSize(QtCore.QSize(0, 60))
        self.group_proxy.setFlat(False)
        self.group_proxy.setCheckable(True)
        self.group_proxy.setChecked(False)
        self.group_proxy.setObjectName(_fromUtf8("group_proxy"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.group_proxy)
        self.horizontalLayout_2.setMargin(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_6 = QtGui.QLabel(self.group_proxy)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6)
        self.txt_proxy = QtGui.QLineEdit(self.group_proxy)
        self.txt_proxy.setObjectName(_fromUtf8("txt_proxy"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.txt_proxy)
        self.horizontalLayout_2.addLayout(self.formLayout_4)
        self.verticalLayout.addWidget(self.group_proxy)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_add = QtGui.QPushButton(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMinimumSize(QtCore.QSize(120, 0))
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_cancel = QtGui.QPushButton(AddServerForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_cancel.sizePolicy().hasHeightForWidth())
        self.btn_cancel.setSizePolicy(sizePolicy)
        self.btn_cancel.setMinimumSize(QtCore.QSize(120, 0))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AddServerForm)
        QtCore.QMetaObject.connectSlotsByName(AddServerForm)

    def retranslateUi(self, AddServerForm):
        AddServerForm.setWindowTitle(QtGui.QApplication.translate("AddServerForm", "Add Server", None, QtGui.QApplication.UnicodeUTF8))
        self.chb_enabled.setText(QtGui.QApplication.translate("AddServerForm", "Enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AddServerForm", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_group.setText(QtGui.QApplication.translate("AddServerForm", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_url.setText(QtGui.QApplication.translate("AddServerForm", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_parse.setText(QtGui.QApplication.translate("AddServerForm", "Parse", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_test.setText(QtGui.QApplication.translate("AddServerForm", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.grp_login.setTitle(QtGui.QApplication.translate("AddServerForm", "Enable authentication", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("AddServerForm", "Login:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("AddServerForm", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.chb_showpass.setText(QtGui.QApplication.translate("AddServerForm", "Show password", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_protocol.setItemText(0, QtGui.QApplication.translate("AddServerForm", "http", None, QtGui.QApplication.UnicodeUTF8))
        self.cmb_protocol.setItemText(1, QtGui.QApplication.translate("AddServerForm", "https", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("AddServerForm", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("AddServerForm", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.group_autoupdate.setTitle(QtGui.QApplication.translate("AddServerForm", "Autoupdate", None, QtGui.QApplication.UnicodeUTF8))
        self.spin_time.setSuffix(QtGui.QApplication.translate("AddServerForm", " sec.", None, QtGui.QApplication.UnicodeUTF8))
        self.group_proxy.setTitle(QtGui.QApplication.translate("AddServerForm", "Use proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("AddServerForm", "Proxy:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add.setText(QtGui.QApplication.translate("AddServerForm", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("AddServerForm", "Close", None, QtGui.QApplication.UnicodeUTF8))

