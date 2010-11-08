from PyQt4.QtCore import Qt
import os
from os.path import dirname, realpath
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DB_FILE_PATH = "db.json"
LOG_FILENAME = 'monitor.log'
DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
INFINITY = 360 * 24 * 60
ROOT_DIR = dirname(dirname(realpath(__file__)))
SERVER_INFO_ROLE = Qt.UserRole + 1
TASK_INFO_ROLE =  Qt.UserRole + 2
VIEW_INFO_ROLE =  Qt.UserRole + 3



