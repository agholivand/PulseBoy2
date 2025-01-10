# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TrialWidget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(200, 76)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        Form.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.removeButton = QtWidgets.QToolButton(Form)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 1, 0, 1, 1)
        self.activeValvesEdit = QtWidgets.QLineEdit(Form)
        self.activeValvesEdit.setReadOnly(True)
        self.activeValvesEdit.setObjectName("activeValvesEdit")
        self.gridLayout.addWidget(self.activeValvesEdit, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 1, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.removeButton.setText(_translate("Form", "-"))
        self.label_2.setText(_translate("Form", "Active Valves"))

