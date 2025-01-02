# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PulseBoyUI_v2.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1229, 809)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.viewWidgetTab = QtWidgets.QTabWidget(self.centralwidget)
        self.viewWidgetTab.setObjectName("viewWidgetTab")
        self.pulseTab = QtWidgets.QWidget()
        self.pulseTab.setObjectName("pulseTab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.pulseTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.graphicsView = PlotWidget(self.pulseTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_5.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.viewWidgetTab.addTab(self.pulseTab, "")
        self.analogDataTab = QtWidgets.QWidget()
        self.analogDataTab.setObjectName("analogDataTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.analogDataTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.analogView = PlotWidget(self.analogDataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analogView.sizePolicy().hasHeightForWidth())
        self.analogView.setSizePolicy(sizePolicy)
        self.analogView.setObjectName("analogView")
        self.gridLayout_6.addWidget(self.analogView, 0, 0, 1, 1)
        self.viewWidgetTab.addTab(self.analogDataTab, "")
        self.gridLayout.addWidget(self.viewWidgetTab, 3, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.trialBankTable = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trialBankTable.sizePolicy().hasHeightForWidth())
        self.trialBankTable.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.trialBankTable.setFont(font)
        self.trialBankTable.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.trialBankTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.trialBankTable.setObjectName("trialBankTable")
        self.trialBankTable.horizontalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.trialBankTable, 3, 0, 1, 1)
        self.valveBankScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.valveBankScrollArea.setWidgetResizable(True)
        self.valveBankScrollArea.setObjectName("valveBankScrollArea")
        self.valveBankContents = QtWidgets.QWidget()
        self.valveBankContents.setGeometry(QtCore.QRect(0, 0, 18, 348))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valveBankContents.sizePolicy().hasHeightForWidth())
        self.valveBankContents.setSizePolicy(sizePolicy)
        self.valveBankContents.setObjectName("valveBankContents")
        self.valveBankLayout = QtWidgets.QVBoxLayout(self.valveBankContents)
        self.valveBankLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.valveBankLayout.setContentsMargins(0, 0, 0, 0)
        self.valveBankLayout.setObjectName("valveBankLayout")
        self.valveBankScrollArea.setWidget(self.valveBankContents)
        self.gridLayout.addWidget(self.valveBankScrollArea, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.setupTabs = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setupTabs.sizePolicy().hasHeightForWidth())
        self.setupTabs.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        font.setPointSize(10)
        self.setupTabs.setFont(font)
        self.setupTabs.setObjectName("setupTabs")
        self.hardwareTab = QtWidgets.QWidget()
        self.hardwareTab.setObjectName("hardwareTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.hardwareTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.digitalChannelsEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.digitalChannelsEdit.setObjectName("digitalChannelsEdit")
        self.gridLayout_2.addWidget(self.digitalChannelsEdit, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.hardwareTab)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 9, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.hardwareTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.hardwareTab)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)
        self.digitalOutDevEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.digitalOutDevEdit.setObjectName("digitalOutDevEdit")
        self.gridLayout_2.addWidget(self.digitalOutDevEdit, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.hardwareTab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.analogChannelsLabel = QtWidgets.QLabel(self.hardwareTab)
        self.analogChannelsLabel.setObjectName("analogChannelsLabel")
        self.gridLayout_2.addWidget(self.analogChannelsLabel, 2, 1, 1, 1)
        self.analogInDevEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.analogInDevEdit.setObjectName("analogInDevEdit")
        self.gridLayout_2.addWidget(self.analogInDevEdit, 3, 0, 1, 1)
        self.analogChannelsEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.analogChannelsEdit.setObjectName("analogChannelsEdit")
        self.gridLayout_2.addWidget(self.analogChannelsEdit, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.hardwareTab)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)
        self.sampRateEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.sampRateEdit.setObjectName("sampRateEdit")
        self.gridLayout_2.addWidget(self.sampRateEdit, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 8, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.hardwareTab)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.triggerInEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.triggerInEdit.setObjectName("triggerInEdit")
        self.gridLayout_2.addWidget(self.triggerInEdit, 10, 0, 1, 1)
        self.syncClockEdit = QtWidgets.QLineEdit(self.hardwareTab)
        self.syncClockEdit.setObjectName("syncClockEdit")
        self.gridLayout_2.addWidget(self.syncClockEdit, 5, 0, 1, 1)
        self.setupTabs.addTab(self.hardwareTab, "")
        self.globalParametersTab = QtWidgets.QWidget()
        self.globalParametersTab.setObjectName("globalParametersTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.globalParametersTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.globalParametersTab)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 1)
        self.globalOnsetEdit = QtWidgets.QLineEdit(self.globalParametersTab)
        self.globalOnsetEdit.setObjectName("globalOnsetEdit")
        self.gridLayout_3.addWidget(self.globalOnsetEdit, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.globalParametersTab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 1, 1, 1)
        self.globalOffsetEdit = QtWidgets.QLineEdit(self.globalParametersTab)
        self.globalOffsetEdit.setObjectName("globalOffsetEdit")
        self.gridLayout_3.addWidget(self.globalOffsetEdit, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        self.setupTabs.addTab(self.globalParametersTab, "")
        self.experimentSetupTab = QtWidgets.QWidget()
        self.experimentSetupTab.setObjectName("experimentSetupTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.experimentSetupTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem2, 4, 0, 1, 1)
        self.trialNameEdit = QtWidgets.QLineEdit(self.experimentSetupTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trialNameEdit.sizePolicy().hasHeightForWidth())
        self.trialNameEdit.setSizePolicy(sizePolicy)
        self.trialNameEdit.setObjectName("trialNameEdit")
        self.gridLayout_4.addWidget(self.trialNameEdit, 3, 0, 1, 1)
        self.valveTypeCombo = QtWidgets.QComboBox(self.experimentSetupTab)
        self.valveTypeCombo.setObjectName("valveTypeCombo")
        self.valveTypeCombo.addItem("")
        self.valveTypeCombo.addItem("")
        self.valveTypeCombo.addItem("")
        self.valveTypeCombo.addItem("")
        self.valveTypeCombo.addItem("")
        self.gridLayout_4.addWidget(self.valveTypeCombo, 0, 1, 1, 1)
        self.removeTrialButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.removeTrialButton.setObjectName("removeTrialButton")
        self.gridLayout_4.addWidget(self.removeTrialButton, 2, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 1, 0, 1, 1)
        self.runSelectedButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.runSelectedButton.setObjectName("runSelectedButton")
        self.gridLayout_4.addWidget(self.runSelectedButton, 7, 0, 1, 1)
        self.moveUpButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.moveUpButton.setObjectName("moveUpButton")
        self.gridLayout_4.addWidget(self.moveUpButton, 3, 1, 1, 1)
        self.startQueueButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.startQueueButton.setObjectName("startQueueButton")
        self.gridLayout_4.addWidget(self.startQueueButton, 6, 0, 1, 1)
        self.addTrialButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.addTrialButton.setObjectName("addTrialButton")
        self.gridLayout_4.addWidget(self.addTrialButton, 2, 0, 1, 1)
        self.updateTrialButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.updateTrialButton.setObjectName("updateTrialButton")
        self.gridLayout_4.addWidget(self.updateTrialButton, 2, 1, 1, 1)
        self.moveDownButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.moveDownButton.setObjectName("moveDownButton")
        self.gridLayout_4.addWidget(self.moveDownButton, 3, 2, 1, 1)
        self.addValveButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.addValveButton.setObjectName("addValveButton")
        self.gridLayout_4.addWidget(self.addValveButton, 0, 0, 1, 1)
        self.stopQueueButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.stopQueueButton.setObjectName("stopQueueButton")
        self.gridLayout_4.addWidget(self.stopQueueButton, 6, 2, 1, 1)
        self.triggerWaitCheckBox = QtWidgets.QCheckBox(self.experimentSetupTab)
        self.triggerWaitCheckBox.setObjectName("triggerWaitCheckBox")
        self.gridLayout_4.addWidget(self.triggerWaitCheckBox, 7, 2, 1, 1)
        self.pauseQueueButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.pauseQueueButton.setObjectName("pauseQueueButton")
        self.gridLayout_4.addWidget(self.pauseQueueButton, 6, 1, 1, 1)
        self.startQueueFromSelectedButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.startQueueFromSelectedButton.setObjectName("startQueueFromSelectedButton")
        self.gridLayout_4.addWidget(self.startQueueFromSelectedButton, 7, 1, 1, 1)
        self.randomiseTrialsButton = QtWidgets.QPushButton(self.experimentSetupTab)
        self.randomiseTrialsButton.setObjectName("randomiseTrialsButton")
        self.gridLayout_4.addWidget(self.randomiseTrialsButton, 5, 0, 1, 1)
        self.setupTabs.addTab(self.experimentSetupTab, "")
        self.dataExportTab = QtWidgets.QWidget()
        self.dataExportTab.setObjectName("dataExportTab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.dataExportTab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_13 = QtWidgets.QLabel(self.dataExportTab)
        self.label_13.setObjectName("label_13")
        self.gridLayout_7.addWidget(self.label_13, 1, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.dataExportTab)
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 0, 0, 1, 1)
        self.exportPathEdit = QtWidgets.QLineEdit(self.dataExportTab)
        self.exportPathEdit.setObjectName("exportPathEdit")
        self.gridLayout_7.addWidget(self.exportPathEdit, 0, 1, 1, 1)
        self.exportSuffixEdit = QtWidgets.QLineEdit(self.dataExportTab)
        self.exportSuffixEdit.setObjectName("exportSuffixEdit")
        self.gridLayout_7.addWidget(self.exportSuffixEdit, 1, 1, 1, 1)
        self.exportPathDirButton = QtWidgets.QPushButton(self.dataExportTab)
        self.exportPathDirButton.setObjectName("exportPathDirButton")
        self.gridLayout_7.addWidget(self.exportPathDirButton, 0, 2, 1, 1)
        self.setupTabs.addTab(self.dataExportTab, "")
        self.gridLayout.addWidget(self.setupTabs, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1229, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave_Configuration = QtWidgets.QAction(MainWindow)
        self.actionSave_Configuration.setObjectName("actionSave_Configuration")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave_Configuration)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.viewWidgetTab.setCurrentIndex(0)
        self.setupTabs.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.viewWidgetTab.setTabText(self.viewWidgetTab.indexOf(self.pulseTab), _translate("MainWindow", "Pulses"))
        self.viewWidgetTab.setTabText(self.viewWidgetTab.indexOf(self.analogDataTab), _translate("MainWindow", "Analog Data"))
        self.label_8.setText(_translate("MainWindow", "Trial Bank"))
        self.label.setText(_translate("MainWindow", "Valve Bank"))
        self.digitalChannelsEdit.setText(_translate("MainWindow", "4"))
        self.label_9.setText(_translate("MainWindow", "Trigger In Source"))
        self.label_2.setText(_translate("MainWindow", "Digital Out Device"))
        self.label_4.setText(_translate("MainWindow", "Digital Channels"))
        self.digitalOutDevEdit.setText(_translate("MainWindow", "dev2/port0/line0:3"))
        self.label_3.setText(_translate("MainWindow", "Analog Input Device"))
        self.analogChannelsLabel.setText(_translate("MainWindow", "Analog Channels"))
        self.analogInDevEdit.setText(_translate("MainWindow", "dev2/ai4"))
        self.analogChannelsEdit.setText(_translate("MainWindow", "1"))
        self.label_5.setText(_translate("MainWindow", "Sampling Rate"))
        self.sampRateEdit.setText(_translate("MainWindow", "20000"))
        self.label_11.setText(_translate("MainWindow", "Synchronisation Clock"))
        self.triggerInEdit.setText(_translate("MainWindow", "cDAQ1Mod2/ai3"))
        self.syncClockEdit.setText(_translate("MainWindow", "/dev2/ai/SampleClock"))
        self.setupTabs.setTabText(self.setupTabs.indexOf(self.hardwareTab), _translate("MainWindow", "Hardware"))
        self.label_6.setText(_translate("MainWindow", "Onset"))
        self.globalOnsetEdit.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "Offset"))
        self.globalOffsetEdit.setText(_translate("MainWindow", "0"))
        self.setupTabs.setTabText(self.setupTabs.indexOf(self.globalParametersTab), _translate("MainWindow", "Global Parameters"))
        self.trialNameEdit.setText(_translate("MainWindow", "Trial Name"))
        self.valveTypeCombo.setItemText(0, _translate("MainWindow", "Simple"))
        self.valveTypeCombo.setItemText(1, _translate("MainWindow", "Binary"))
        self.valveTypeCombo.setItemText(2, _translate("MainWindow", "Anti Plume"))
        self.valveTypeCombo.setItemText(3, _translate("MainWindow", "Noise"))
        self.valveTypeCombo.setItemText(4, _translate("MainWindow", "Plume"))
        self.removeTrialButton.setText(_translate("MainWindow", "Remove Trial"))
        self.runSelectedButton.setText(_translate("MainWindow", "Run Selected"))
        self.moveUpButton.setText(_translate("MainWindow", "Move Up"))
        self.startQueueButton.setText(_translate("MainWindow", "Start Queue"))
        self.addTrialButton.setText(_translate("MainWindow", "Add To Trials"))
        self.updateTrialButton.setText(_translate("MainWindow", "Update Trial"))
        self.moveDownButton.setText(_translate("MainWindow", "Move Down"))
        self.addValveButton.setText(_translate("MainWindow", "Add Valve"))
        self.stopQueueButton.setText(_translate("MainWindow", "Stop Queue"))
        self.triggerWaitCheckBox.setText(_translate("MainWindow", "Wait for trigger"))
        self.pauseQueueButton.setText(_translate("MainWindow", "Pause Queue"))
        self.startQueueFromSelectedButton.setText(_translate("MainWindow", "Start Queue from Selected"))
        self.randomiseTrialsButton.setText(_translate("MainWindow", "Randomise trials"))
        self.setupTabs.setTabText(self.setupTabs.indexOf(self.experimentSetupTab), _translate("MainWindow", "Experiment"))
        self.label_13.setText(_translate("MainWindow", "Export Suffix"))
        self.label_12.setText(_translate("MainWindow", "Export Path"))
        self.exportPathEdit.setText(_translate("MainWindow", "C:/Users/erskina/PycharmProjects/PulseBoy/Data/"))
        self.exportSuffixEdit.setText(_translate("MainWindow", "data"))
        self.exportPathDirButton.setText(_translate("MainWindow", "..."))
        self.setupTabs.setTabText(self.setupTabs.indexOf(self.dataExportTab), _translate("MainWindow", "Data"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionSave_Configuration.setText(_translate("MainWindow", "Save Configuration"))

from pyqtgraph import PlotWidget