from UI.UI_New_Task import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from config import *
from couchdbcurl import Server 
import logging
import urlparse
import json

class ReplicationWindow(QWidget):
    def __init__(self,mainWindow,server_obj, replication_record):
        super(ReplicationWindow, self).__init__()
        self.ui = Ui_New_Task_Form()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow
        self.server_obj = server_obj
        self.connect(self.ui.btn_cancel, QtCore.SIGNAL("clicked()"), self.cancel_react)
        if replication_record:
            cur_type = replication_record.get('record_type')
        else:
            cur_type = -1

        self.ui.btn_save.setText("Add")
        self.connect(self.ui.btn_save, QtCore.SIGNAL("clicked()"), self.add_react)
        
        self.connect(self.ui.txt_remotesource, QtCore.SIGNAL("returnPressed()"), self.add_react)
        self.connect(self.ui.txt_remotetarget, QtCore.SIGNAL("returnPressed()"), self.add_react)
        self.connect(self.ui.txt_proxy, QtCore.SIGNAL("returnPressed()"), self.add_react)
        
        self.connect(self, QtCore.SIGNAL("keyPressEvent( QKeyEvent *)"), self.key_pressed)
        
        self.connect(self.ui.btn_getfilters, QtCore.SIGNAL("clicked()"), self.fill_filters)
        
        self.connect(self.ui.rdb_localsource, QtCore.SIGNAL("toggled(bool)"), self.localsource_toggeled)
        self.connect(self.ui.rdb_localtarget, QtCore.SIGNAL("toggled(bool)"), self.localtarget_toggeled)
        
        self.connect(self.ui.cmb_localsource, QtCore.SIGNAL("currentIndexChanged (int)"), self.clear_filters)
        
        db_names = []       
        for db in Server(self.server_obj['url']):
            db_names.append(db)
        db_names.sort()
        
        task_source = ""
        task_target = ""
        
        if cur_type == 0:
            txt_lst = replication_record.get('task').split(' ')
           
            task_source = txt_lst[1]
            task_target = txt_lst[3]
            
#            self.ui.txt_source.setText(task_source)
#            self.ui.txt_target.setText(task_target)
        
        
        for i, value in enumerate(db_names):
            self.ui.cmb_localsource.addItem(QString(value), userData=value)
            if value == task_source:
                self.ui.cmb_localsource.setCurrentIndex(i)

            self.ui.cmb_localtarget.addItem(QString(value), userData=value)
            if value == task_target:
                self.ui.cmb_localtarget.setCurrentIndex(i)
                
                
        if task_source.startswith("http://"):
            self.ui.txt_remotesource.setText(task_source)
            self.ui.rdb_remotesource.setChecked(True)
        
        if task_target.startswith("http://"):
            self.ui.txt_remotetarget.setText(task_target)
            self.ui.rdb_remotetarget.setChecked(True)
        
    def clear_filters(self, index):
        self.ui.cmb_filters.clear()
        
    def filter_functions(self, db):
        functions = []
        for row in db.view('_all_docs', startkey = '_design/', endkey = '_designZ', include_docs = True).rows:
            if 'filters' in row.doc:
                doc_id = row.id.split('/')[1]
                for name in row.doc.filters:
                    functions.append("%s/%s" % (doc_id, name))

        return functions

    
    def fill_filters(self):
        server = self.server_obj['url']
        db = str(self.ui.cmb_localsource.currentText())
        if not self.ui.rdb_localsource.isChecked():
            url = str(self.ui.txt_remotesource.text())
            url_parsed = urlparse.urlparse(url)
            
            server = "http://%s/" % url_parsed.hostname
            port = url_parsed.port;
            
            if port:
                server = "http://%s:%s/" % (url_parsed.hostname, port,)

            db = url_parsed.path
            db_list = db.split('/')
            if len(db_list) == 3:
                db =  db_list[1]

        filter_list = []

        try:
            remote_serv = Server(server)
            remote_db = remote_serv[db]
            filter_list = self.filter_functions(remote_db)
            self.ui.cmb_filters.clear()
            self.ui.cmb_filters.addItems(QStringList(filter_list))

        except:
            QMessageBox(QMessageBox.Critical, 'Error', 'Error while fetching filter functions', QtGui.QMessageBox.Ok).exec_()
             
    
    def localsource_toggeled(self, state):
        if state:
            self.ui.txt_remotesource.setEnabled(False)
            self.ui.cmb_localsource.setEnabled(True)
        else:
            self.ui.txt_remotesource.setEnabled(True)
            self.ui.cmb_localsource.setEnabled(False)
    
    
    def localtarget_toggeled(self, state):
        if state:
            self.ui.txt_remotetarget.setEnabled(False)
            self.ui.cmb_localtarget.setEnabled(True)
        else:
            self.ui.txt_remotetarget.setEnabled(True)
            self.ui.cmb_localtarget.setEnabled(False)
    def key_pressed(self,event):    
        print "key pressed ",event.key  
            
    def add_react(self):
        """Slot for signal "clicked()" of "Add" button 
        """
        if self.validate():

            source = str(self.ui.txt_remotesource.text())
            if self.ui.rdb_localsource.isChecked():
                source = str(self.ui.cmb_localsource.currentText())
            
            target = str(self.ui.txt_remotetarget.text())
            if self.ui.rdb_localtarget.isChecked():
                target = str(self.ui.cmb_localtarget.currentText())
            
            proxy = str(self.ui.txt_proxy.text())
            
            filter = str(self.ui.cmb_filters.currentText())
            
            query = str(self.ui.txt_query.text())
            if query:
                try:
                    query = json.loads(query)
                    
                except:
                    QMessageBox(QMessageBox.Critical, 'Error', 'Error parsing query field', QtGui.QMessageBox.Ok).exec_()
                    return
            
            
           
            
            if source.startswith("http"):
                if not source.endswith("/"):
                    source += "/"
            if target.startswith("http"):
                if not target.endswith("/"):
                    target += "/"
            
            new_relication = {'source': source, 'target': target, 'proxy': proxy, 'filter': filter, 'query': query}

            if new_relication in self.server_obj.get('replications'):
                QMessageBox(QMessageBox.Warning, 'Warning', 'Record for this replication already exist!!!', QtGui.QMessageBox.Ok).exec_()
            else:
                self.mainWindow.dump_replication_record(self.server_obj, new_relication)
                self.close()
                
        
                   
    def cancel_react(self):
        self.close()
    
    
    def validate(self):
        if not self.ui.rdb_localsource.isChecked() and not str(self.ui.txt_remotesource.text()):
            QMessageBox(QMessageBox.Critical, 'Error', 'Source field are required', QtGui.QMessageBox.Ok).exec_()
            return False
        
        if not self.ui.rdb_localtarget.isChecked() and not str(self.ui.txt_remotetarget.text()):
            QMessageBox(QMessageBox.Critical, 'Error', 'Target field are required', QtGui.QMessageBox.Ok).exec_()
            return False
    
        return True
        
    def closeEvent(self,event):
        try:
            self.mainWindow.replication_windows.remove(self)
        except:
            #print "error removing from replication windows list"
            logging.debug('ReplicationWindow: error removing from replication windows list')
        