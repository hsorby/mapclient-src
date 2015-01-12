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
from PySide.QtGui import QDialog

from mapclient.widgets.ui_pluginerrors import Ui_PluginErrors

class PluginErrors(QDialog):
    
    def __init__(self, plugins, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_PluginErrors()
        self._ui.setupUi(self)
        self._ui.label.setText('The following plugins could not be loaded correctly.\n\nHover over each plugin for suggested solutions.')
        self._pluginErrors = plugins
        
    def fillList(self):
        for error in self._pluginErrors:
            for plugin in self._pluginErrors[error]: 
                self._ui.listWidget.addItem(plugin + ' - ' + error)                    
        
        for row in range(self._ui.listWidget.count()):
            item = self._ui.listWidget.item(row)
            text = item.text().split(' - ')
            error = text[-1]
            if error == 'TypeError' or error == 'SyntaxError' or error == 'TabError':
                item.setToolTip('Please update this plugin using the built-in\nplugin updater under \'Advanced\' in the Plugin Manager\ndialog.')
            else:
                item.setToolTip('Please examine the plugin README.md file and\nobtain the listed dependencies.')