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
import os, sys

from PySide import QtCore

from mapclient.settings import info

# Credentials follows:
#
# Key    OP8AKmDIlH7OkHaPWNbnb-zf
# Secret    QQcKMnyCjjb7JNDHA-Lwdu7p
#
# The scope that should be used
#
# from urllib import quote_plus
# DEFAULT_SCOPE = quote_plus(
#     'http://localhost:8280/pmr/scope/collection,'
#     'http://localhost:8280/pmr/scope/search,'
#     'http://localhost:8280/pmr/scope/workspace_tempauth,'
#     'http://localhost:8280/pmr/scope/workspace_full'
# )


class PMRInfo(object):

    DEFAULT_PMR_IPADDRESS = 'http://teaching.physiomeproject.org'
    DEFAULT_CONSUMER_PUBLIC_TOKEN = 'OP8AKmDIlH7OkHaPWNbnb-zf'
    DEFAULT_CONSUMER_SECRET_TOKEN = 'QQcKMnyCjjb7JNDHA-Lwdu7p'
    

    def __init__(self):
        self.readSettings()

    def readSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('PMR')
        # pmr_host?  this is a domain name...
        self.ipaddress = settings.value('pmr-website', self.DEFAULT_PMR_IPADDRESS)
        self.host = self.ipaddress
        self.consumer_public_token = settings.value('consumer-public-token', self.DEFAULT_CONSUMER_PUBLIC_TOKEN)
        self.consumer_secret_token = settings.value('consumer-secret-token', self.DEFAULT_CONSUMER_SECRET_TOKEN)
        self.user_public_token = settings.value('user-public-token', None)
        self.user_secret_token = settings.value('user-secret-token', None)
        settings.endGroup()

    def writeSettings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('PMR')

        temp_public = self.user_public_token or ''
        temp_secret = self.user_secret_token or ''

        settings.setValue('user-public-token', temp_public)
        settings.setValue('user-secret-token', temp_secret)
        settings.endGroup()

    def update_token(self, oauth_token, oauth_token_secret):
        self.user_public_token = oauth_token
        self.user_secret_token = oauth_token_secret
        self.writeSettings()

    def has_access(self):
        return bool(self.user_public_token and self.user_secret_token)

    def get_session_kwargs(self):
        return {
            'client_key': self.consumer_public_token,
            'client_secret': self.consumer_secret_token,
            'resource_owner_key': self.user_public_token,
            'resource_owner_secret': self.user_secret_token,
        }

def getLogDirectory():
    
    settings = QtCore.QSettings()
    fn = settings.fileName()
    app_dir, _ = os.path.splitext(fn)
    log_directory = os.path.join(app_dir, 'logs')
    
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    return log_directory
    
    
def getLogLocation():
    '''
    Set up location where log files will be stored (platform dependent).
    '''
    log_filename = 'logging_record.log'
    log_directory = getLogDirectory()
    
    logging_file_location = os.path.join(log_directory, log_filename)
    
    return logging_file_location
    
