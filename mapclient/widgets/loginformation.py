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
from PySide.QtGui import QDialog, QTableWidgetItem
from mapclient.widgets.ui_loginformation import Ui_LogInformation
from mapclient.settings.general import getLogLocation


class LogInformation(QDialog):
    '''
    Log record dialog to present the user with the log information recorded by the program.
    '''

    current_log_file = getLogLocation()
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_LogInformation()
        self._ui.setupUi(self)
        self._makeConnections()
        
    def fillTable(self, parent=None):
        log_file = open(getLogLocation(), 'r')
        log_data = log_file.read()
        log_file.close()        
        logs = log_data.split('\n')
        logs = logs[:-1]
        self._ui.information_table.setRowCount(len(logs))
      
        row_number = 0
        for log in logs:
            log_components = log.split(' - ')
            basic_info = []
            basic_info += [log_components[1]] + log_components[3:5]
            for column_number in range(3):
                self._ui.information_table.setItem(row_number,column_number, \
                    QTableWidgetItem(basic_info[column_number]))
            row_number += 1
        
    def _makeConnections(self):
        self._ui.detailsButton.clicked.connect(self.showLogDetails)
        self._ui.loadButton.clicked.connect(self.loadLogSession)
        
    def showLogDetails(self):
        from mapclient.widgets.logdetails import LogDetails
        dlg = LogDetails(self)
        dlg.setModal(True)
        index = self._ui.information_table.indexFromItem(self._ui.information_table.currentItem())
        row_number = index.row()
        selectedItemInformation = self._ui.information_table.item(row_number, 2)
        selectedItemTime = self._ui.information_table.item(row_number, 0)
        informationText = selectedItemInformation.text()
        timeText = selectedItemTime.text()
        dlg.fillTable(informationText, timeText, self.current_log_file)
        dlg.exec_()
        
    def loadLogSession(self):
        from mapclient.widgets.loadlogsession import LoadLogSession
        dlg = LoadLogSession(self)
        dlg.setModal(True)
        if dlg.exec_():
            action = dlg.loadSession()
            if action != None:
                self.updateTable(action[0])
                self.current_log_file = action[1]
        
    def updateTable(self, logs):
        self._ui.information_table.clearContents()
        self._ui.information_table.setRowCount(len(logs))
 
        row_number = 0
        for log in logs:
            log_components = log.split(' - ')
            basic_info = []
            basic_info += [log_components[1]] + log_components[3:5]
            for column_number in range(3):
                self._ui.information_table.setItem(row_number,column_number, \
                    QTableWidgetItem(basic_info[column_number]))
            row_number += 1
