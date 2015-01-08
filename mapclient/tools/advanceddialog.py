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
import pkgutil, os, sys, imp, importlib, collections
from PySide.QtGui import QDialog, QMessageBox

from mapclient.tools.ui_advanceddialog import Ui_AdvancedDialog
from mapclient.tools.pluginupdater import PluginUpdater

class AdvancedDialog(QDialog):
    '''
    Dialog containing advanced plugin tools, settings and information.
    '''
    
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_AdvancedDialog()
        self._ui.setupUi(self)
        self._makeConnections()
        self._pluginUpdater = PluginUpdater()
        self.fillList(self._pluginUpdater._pluginUpdateDict)
        
    def _makeConnections(self):
        self._ui.updateButton.clicked.connect(self.updatePlugins)
        self._ui.dependenciesButton.clicked.connect(self.showAdditionalPluginModules)
        self._ui.analyseButton.clicked.connect(self.analysePlugins)
        
    def fillList(self, plugin_updates_dict):
        self._ui.listWidget.clear()
        location_string = 'Location Update'
        resource_string = 'Resource Update'
        syntax_string = 'Syntax Update'
        modules_string = 'Additional Modules Required'
        indentation_string = 'Inconsistent Indentation'
        stringList = [location_string, resource_string, syntax_string, indentation_string]
        
        for plugin in plugin_updates_dict:
            display_string = plugin + ' - '
            for index in range(1, 5):
                update = plugin_updates_dict[plugin][index]
                if update:
                    display_string += stringList[index-1] + ' | '
            if self._pluginUpdater._additionalPluginModules:
                display_string += modules_string + ' | '
            if len(display_string) > (len(plugin)+3):
                self._ui.listWidget.addItem(display_string[:-3])
                
        if self._ui.listWidget.count() == 0:
            self._ui.updateButton.setEnabled(False)
            self._ui.dependenciesButton.setEnabled(False)
            self._ui.updateLabel.setText('None of your plugins currently require updating. \nClick \'Analyse Plugins\' to check for more updates.')
        else:
            self._ui.updateButton.setEnabled(True)
            if self._pluginUpdater._additionalRequiredModules:
                self._ui.dependenciesButton.setEnabled(True)
            else:
                self._ui.dependenciesButton.setEnabled(False)
            self._ui.updateLabel.setText('Please update the above plugins:')
            
    def analysePlugins(self):
        self._pluginUpdater._pluginUpdateDict = {}
        self._pluginUpdater._additionalRequiredModules = []
        try:
            package = imp.reload(sys.modules['mapclientplugins'])
        except Exception:
            package = importlib.reload(sys.modules['mapclientplugins'])
        for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg and modname != 'imagesourcestep' and modname != 'pointcloudserializerstep':
                self._pluginUpdater._directory = _.path
                plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(_.path, modname))
                plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(_.path, modname, '__init__.py'))            
                plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(_.path)
                if plugin_tabbed_indentation:
                    self._pluginUpdater.fixTabbedIndentation(modname, tabbed_modules, True)
                plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(_.path)
                self._pluginUpdater.deleteTempFiles(tabbed_modules)
                requires_additional_modules = self._pluginUpdater.checkAdditionalModules(modname)
                if requires_additional_modules:
                    self._pluginUpdater.additionalRequiredModules(modname)
                self._pluginUpdater.pluginUpdateDict(modname, plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(_.path, modname, '__init__.py'), resourcesDir, tabbed_modules)
        self.fillList(self._pluginUpdater._pluginUpdateDict)
            
    def updatePlugins(self):
        unsuccessful_updates = []
        self._pluginUpdater._additionalPluginModules = []
        for plugin in self._pluginUpdater._pluginUpdateDict.keys():
            if self._pluginUpdater._pluginUpdateDict[plugin][4] and sys.version_info > (2, 7):
                self._pluginUpdater.fixTabbedIndentation(plugin, self._pluginUpdater._pluginUpdateDict[plugin][7], False)            
            if self._pluginUpdater._pluginUpdateDict[plugin][3]:
                self._pluginUpdater.updateSyntax(plugin, self._pluginUpdater._pluginUpdateDict[plugin][0])
            if self._pluginUpdater._pluginUpdateDict[plugin][1]:
                self._pluginUpdater.updateInitContents(plugin, self._pluginUpdater._pluginUpdateDict[plugin][5])
            if self._pluginUpdater._pluginUpdateDict[plugin][2]:
                self._pluginUpdater.updateResourcesFile(plugin, self._pluginUpdater._pluginUpdateDict[plugin][6])
            
            plugins_to_delete = []
            compare = lambda required_updates, update_report: collections.Counter(required_updates) == collections.Counter(update_report)
            if compare(self._pluginUpdater._pluginUpdateDict[plugin][1:5], [item for item in self._pluginUpdater._successful_plugin_update.values()]):
                plugins_to_delete += [plugin]
                self._pluginUpdater._successful_plugin_update = {'indentation_update_sucess':False, 'init_update_success':False, 'resources_update_success':False, 'syntax_update_success':False}
            else:
                unsuccessful_updates += [plugin]
            
        for plugin in plugins_to_delete:
            del self._pluginUpdater._pluginUpdateDict[plugin]
        self.fillList(self._pluginUpdater._pluginUpdateDict)
        
        if unsuccessful_updates:
            warning_string = '\n  The following plugins failed to update successfully:\n'
            for plugin in unsuccessful_updates:
                warning_string += '\n\t\t\t' + plugin
            ret = QMessageBox.warning(self, 'Warning', warning_string + '\n\nPlease inspect the program logs for more information.  \t', QMessageBox.Ok)

    def showAdditionalPluginModules(self):
        from mapclient.tools.additionalpluginmodules import AdditionalPluginModules
        dlg = AdditionalPluginModules(self._pluginUpdater._additionalPluginModules)
        dlg.setModal(True)
        dlg.fillList()
        dlg.exec_()
