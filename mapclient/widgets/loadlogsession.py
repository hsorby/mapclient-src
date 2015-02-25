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
import os
from PySide.QtGui import QDialog, QFileDialog, QMessageBox

from mapclient.widgets.ui_loadlogsession import Ui_LoadWindow
from mapclient.settings.general import getLogDirectory

class LoadLogSession(QDialog):
    '''
    Load a log record from a previous session.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''        
        QDialog.__init__(self, parent)
        self._ui = Ui_LoadWindow()
        self._ui.setupUi(self)
        self._makeConnections()
        
    def _makeConnections(self):
        self._ui.searchButton.clicked.connect(self.findLogSession)
        self._ui.loadButton.clicked.connect(self.validateSelection)
        
    def findLogSession(self):
        previousSession = QFileDialog.getOpenFileName(self, dir=getLogDirectory(), \
            filter='Log Files (logging_record.log.* logging_record.log)', caption='Select Previous Session',  options=QFileDialog.DontResolveSymlinks | QFileDialog.ReadOnly)
        if len(previousSession) > 0 and len(self._ui.lineEdit.text()) == 0:
            self._ui.lineEdit.insert(previousSession[0])
        else:
            self._ui.lineEdit.clear()
            self._ui.lineEdit.insert(previousSession[0])
            
    def validateSelection(self):
        from mapclient.widgets.ui_loadlogsession import Ui_LoadWindow
        if len(self._ui.lineEdit.text()) == 0:
            ret = QMessageBox.warning(self, 'Error', '\n  No file selected!\t', QMessageBox.Ok)
        else:
            self.accept()
        
    def loadSession(self):
        filename = self._ui.lineEdit.text()
        try:
            log_file = open(filename, 'r')
            log_data = log_file.read()
            log_file.close()        
            logs = log_data.split('\n')
            logs = logs[:-1]
            return logs, filename
        except IOError or FileNotFoundError:
            ret = QMessageBox.critical(self, 'Error', '\n  Failed to load file!\t', QMessageBox.Ok)
