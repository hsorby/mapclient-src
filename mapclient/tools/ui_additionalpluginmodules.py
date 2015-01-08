# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/additionalpluginmodules.ui'
#
# Created: Thu Jan  8 10:46:54 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AdditionalPluginModules(object):
    def setupUi(self, AdditionalPluginModules):
        AdditionalPluginModules.setObjectName("AdditionalPluginModules")
        AdditionalPluginModules.resize(351, 319)
        self.verticalLayout = QtGui.QVBoxLayout(AdditionalPluginModules)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(AdditionalPluginModules)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtGui.QListWidget(AdditionalPluginModules)
        self.listWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(AdditionalPluginModules)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AdditionalPluginModules)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), AdditionalPluginModules.close)
        QtCore.QMetaObject.connectSlotsByName(AdditionalPluginModules)

    def retranslateUi(self, AdditionalPluginModules):
        AdditionalPluginModules.setWindowTitle(QtGui.QApplication.translate("AdditionalPluginModules", "Dependencies", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("AdditionalPluginModules", "The following plugins may require additional modules that cannot be downloaded at this time. Please examine each README.md file and obtain the listed dependencies.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("AdditionalPluginModules", "OK", None, QtGui.QApplication.UnicodeUTF8))

