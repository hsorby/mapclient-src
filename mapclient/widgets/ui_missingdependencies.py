# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/missingdependencies.ui'
#
# Created: Fri Jan  9 11:41:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MissingDependencies(object):
    def setupUi(self, MissingDependencies):
        MissingDependencies.setObjectName("MissingDependencies")
        MissingDependencies.resize(351, 319)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MissingDependencies.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(MissingDependencies)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(MissingDependencies)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtGui.QListWidget(MissingDependencies)
        self.listWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(MissingDependencies)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MissingDependencies)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), MissingDependencies.close)
        QtCore.QMetaObject.connectSlotsByName(MissingDependencies)

    def retranslateUi(self, MissingDependencies):
        MissingDependencies.setWindowTitle(QtGui.QApplication.translate("MissingDependencies", "Dependencies", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MissingDependencies", "The following plugins require additional plackages that are not installed at this time. For each plugin please examine its README.md file and obtain the listed dependencies.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MissingDependencies", "OK", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
