'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''

from PySide import QtGui

from mapclient.tools.pmr.dialogs.ui_pmrdialog import Ui_PMRDialog
from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.authoriseapplicationdialog import AuthoriseApplicationDialog

class PMRDialog(QtGui.QDialog):
    
    def __init__(self, parent=None):
        super(PMRDialog, self).__init__(parent)
        self._ui = Ui_PMRDialog()
        self._ui.setupUi(self)

        self._pmrTool = PMRTool()

        self._makeConnections()

        self._updateUi()

    def _updateUi(self):
        if self._pmrTool.hasAccess():
            self._ui.loginStackedWidget.setCurrentIndex(1)
        else:
            self._ui.loginStackedWidget.setCurrentIndex(0)

    def _makeConnections(self):
        self._ui.registerLabel.linkActivated.connect(self.register)
        self._ui.deregisterLabel.linkActivated.connect(self.deregister)

    def register(self, link):
        if link != 'mapclient.register':
            return

        dlg = AuthoriseApplicationDialog(self)
        dlg.setModal(True)
        dlg.exec_()

        self._updateUi()

    def deregister(self):
        self._pmrTool.deregister()
        self._updateUi()
