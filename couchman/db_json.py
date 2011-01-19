import json
import sys
import os.path
from config import *
import logging
from copy import deepcopy
from pprint import pprint
class MyJson():
    def __init__(self):
        logging.debug('MyJson: init')
        self.MAIN_DB = None;
    
    def getManDB(self):
        return self.MAIN_DB
    
    def readFromDB(self):
        if os.path.isfile(DB_FILE_PATH):
            logging.debug('MyJson: file exist... start reading')
            with open(DB_FILE_PATH, 'r') as f:
                self.MAIN_DB = json.load(f)
                

        else:
            logging.debug('MyJson: file not found... create new one')
            body = []
            
            with open(DB_FILE_PATH, 'w') as f:
                json.dump(body, f)     
            
            self.MAIN_DB = body
        return self.getManDB()

    def save(self):
        try:
            
            dump = deepcopy(self.MAIN_DB)
            for item in dump:
                item['last_update'] = None
                
            with open(DB_FILE_PATH, 'w') as f:
                    json.dump(dump, f, separators=(', ', ': '))
            logging.debug('MyJson: save json complete')
            return True
        except:
            logging.debug('MyJson: Save json failed: %s' % sys.exc_info()[1])
            return False