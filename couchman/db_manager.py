from UI.UI_DocManager import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from models import DBListModel, DBViewModel
from config import *
from workers import ViewWorker
from couchdbcurl import Server 
from datetime import datetime 
import multiprocessing
import logging
import sys

class DBManager(QWidget):

    def __init__(self, server_view_list, mainWindow, server_list, selected_now):
        super(DBManager, self).__init__()
        self.ui = Ui_DocManager()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow
        self.server_list = server_list
        self.server_view_list = server_view_list
        self.view_workers_list = []

        i = 0
        curr = None
        for serv in self.server_list:
            self.ui.cmb_servers.addItem(QString("[%s] %s" % (serv['group'], serv['name'], )), userData=serv)
            self.ui.cmb_servers.setItemIcon(i, QtGui.QIcon(ROOT_DIR+'/media/workgroup.png'))
            if selected_now and selected_now['url'] == serv['url']:
                self.ui.cmb_servers.setCurrentIndex(i)
                cur = i
            i += 1

        self.connect(self.ui.cmb_servers, QtCore.SIGNAL("currentIndexChanged (int)"), self.on_server_changed)
        self.connect(self.ui.tlw_db_list, QtCore.SIGNAL('list_currentChanged (const QModelIndex &)'), self.db_selection_changed)
        self.connect(self.ui.tlw_view_list, QtCore.SIGNAL('list_currentChanged (const QModelIndex &)'), self.view_selection_changed)
        
        self.connect(self.ui.btn_refresh_all, QtCore.SIGNAL("clicked()"), self.btn_refresh_all_react)
        self.connect(self.ui.btn_ping, QtCore.SIGNAL("clicked()"), self.btn_ping_react)
        
        self.connect(self.ui.btn_clean_views, QtCore.SIGNAL("clicked()"), self.btn_cleanviews_react)
        self.connect(self.ui.btn_compact_db, QtCore.SIGNAL("clicked()"), self.btn_compact_db_react)
        self.connect(self.ui.btn_compact_views, QtCore.SIGNAL("clicked()"), self.btn_compact_views_react)
        self.connect(self.ui.btn_compact, QtCore.SIGNAL("clicked()"), self.btn_compact_react)
        

        self.ui.btn_refresh_all.setIcon(QtGui.QIcon(ROOT_DIR+'/media/refresh.png'))
        
        self.ui.btn_clean_views.setIcon(QtGui.QIcon(ROOT_DIR+'/media/clean.png'))
        self.ui.btn_compact_views.setIcon(QtGui.QIcon(ROOT_DIR+'/media/compact.png'))
        self.ui.btn_compact_db.setIcon(QtGui.QIcon(ROOT_DIR+'/media/compact.png'))
        
        self.ui.btn_compact.setIcon(QtGui.QIcon(ROOT_DIR+'/media/compact.png'))
        self.ui.btn_ping.setIcon(QtGui.QIcon(ROOT_DIR+'/media/ping.png'))
        
        if selected_now:    
            self.on_server_changed(cur)
            
            
        #worker's main timer
        self.timer = QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.workerTimer_update) 
        self.timer.start(300)
            
    def on_server_changed(self, index):
        """Slot for signal "currentIndexChanged" of servers combobox
        
            Clear old data and create and populate database list of selected server
        """
        self.server = self.server_list[index]
        if self.server_view_list.get(self.server['url']) is None:
            self.server_view_list[self.server['url']] = {}
            
        self.cur_server_dbs = self.server_view_list[self.server['url']]
        try:
            self.selected_server = Server(self.server['url'])
        except:
            self.selected_server = None
        
        self.disabling_refresh()
        if self.selected_server:
            db_names = []       
            for db in self.selected_server:
                if self.cur_server_dbs.get(db) is None:
                    info = self.selected_server[db].info()
                    self.cur_server_dbs[db] = {"last_refresh":"Unknown", "name":db, "size":info['disk_size'], "docs":info['doc_count']}
                    
                db_names.append(db)
            db_names.sort()
            
      
            self.db_model = DBListModel(self.cur_server_dbs, db_names)
            self.ui.tlw_db_list.setModel(self.db_model)
            
            if len(db_names):
                self.ui.btn_clean_views.setEnabled(False)
                self.ui.btn_compact.setEnabled(False)
                self.ui.btn_compact_db.setEnabled(False)
                self.ui.btn_compact_views.setEnabled(False)
                self.ui.btn_ping.setEnabled(False)
        else:
            self.db_model = DBListModel([])
            self.ui.tlw_db_list.setModel(self.db_model)          
            
        self.view_model = DBViewModel([])
        self.ui.tlw_view_list.setModel(self.view_model)
        
        self.ui.btn_clean_views.setEnabled(False)
        self.ui.btn_compact.setEnabled(False)
        self.ui.btn_compact_db.setEnabled(False)
        self.ui.btn_compact_views.setEnabled(False)
        self.ui.btn_ping.setEnabled(False)
        
        for i in range(self.db_model.columnCount()):
            self.ui.tlw_db_list.resizeColumnToContents(i) 
        
        
    def db_selection_changed(self, index):
        """Slot for signal "list_currentChanged" of database tree view list
            Clear old view list and populate it with new data from selected database
        
        """
        self.selected_db = self.selected_server[self.db_model.db_list[index.row()]]
        row_list = self.selected_db.view('_all_docs', startkey = "_design/", endkey = "_design0").rows
               
        view_list = []
        for row in row_list:
            name = row.key[8:]
           
            if self.cur_server_dbs[self.selected_db.name].get(row.id) is None:
                self.cur_server_dbs[self.selected_db.name][row.id] = {"name":name, "revision":row.value['rev'], "id": row.id}

            view_list.append(self.cur_server_dbs[self.selected_db.name][row.id])
        
        
        if len(view_list) > 0:
            self.ui.btn_refresh_all.setEnabled(True)
            if self.cur_server_dbs[self.selected_db.name]["last_refresh"] == "Unknown":
                self.ui.lbl_last_update.setText("Unknown")
            else:
                self.ui.lbl_last_update.setText(self.cur_server_dbs[self.selected_db.name]["last_refresh"].strftime(DATETIME_FMT))
                
        
        self.view_model = DBViewModel(view_list)
        self.ui.tlw_view_list.setModel(self.view_model)
        
        self.ui.btn_clean_views.setEnabled(True)
        self.ui.btn_compact_db.setEnabled(True)
        self.ui.btn_compact_views.setEnabled(True)
        
        for i in range(self.view_model.columnCount()):
            self.ui.tlw_view_list.resizeColumnToContents(i)        
            
    def view_selection_changed(self):
        """Slot for signal "list_currentChanged" of view tree view list
   
            Enable control buttons to operate with view
        """
        self.ui.btn_ping.setEnabled(True)
        self.ui.btn_compact.setEnabled(True)
        
        
    
    def btn_refresh_all_react(self):
        """Slot for signal "clicked()" of "Refresh all" button
        
            Create worker for each view of selected database and send signal for update information about it
        """
        cur_timestamp = datetime.now()
        self.cur_server_dbs[self.selected_db.name]['last_refresh'] = cur_timestamp
        
        info = self.selected_server[self.selected_db.name].info()
        self.cur_server_dbs[self.selected_db.name]["size"] = info['disk_size']
        self.cur_server_dbs[self.selected_db.name]["docs"] = info['doc_count']
        
        self.ui.lbl_last_update.setText(cur_timestamp.strftime(DATETIME_FMT))
        for row in self.view_model.view_list:
            self.start_view_worker("get_info", {"row_id": row['id']})
            row["refreshing"] = "now"
        self.view_model.update_data()
        self.db_model.update_data()
        
    def btn_ping_react(self):
        """Slot for signal "clicked()" of "Ping" button
        
            Create worker for selected view of selected database and send signal to rebuild it
        """
        name = self.view_model.data(self.ui.tlw_view_list.currentIndex(), VIEW_INFO_ROLE)['name']
        self.start_view_worker("ping", {"view_name":name})
    
    def btn_cleanviews_react(self):
        """Slot for signal "clicked()" of "Cleanup views" button
        
            Send signal to cleanup views on selected database
        """
        self.start_view_worker("cleanup_views")
        
    def btn_compact_db_react(self):
        """Slot for signal "clicked()" of "Compact db" button
        
            Send signal to compact selected database
        """
        self.start_view_worker("compact_db")
    
    def btn_compact_views_react(self):
        """Slot for signal "clicked()" of "Compact views" button
        
           Send signal to compact each views in selected database
        """
        self.start_view_worker("compact_views")
    
    def btn_compact_react(self):
        """Slot for signal "clicked()" of "Compact" button
        
            Send signal to compact selected views in selected database
        """
        name = self.view_model.data(self.ui.tlw_view_list.currentIndex(), VIEW_INFO_ROLE)['name']
        self.start_view_worker("compact_view", {"view_name":name})
    
    def start_view_worker(self,command,params=None):
        """Multifunctional structure (function) 
            
            Implement functionality of control buttons:
                Ping
                Compact
                Cleanup views
                Compact db
                Compact views
        """       
        if command == 'get_info' or command == "ping":
            self_pipe, remote_pipe = multiprocessing.Pipe(duplex = True)
            connector = ViewWorker(remote_pipe, self.server['url'], command, self.selected_db.name, params)
            self.view_workers_list.append({'pipe':self_pipe,'thread':connector})
            connector.start()
        elif command == "cleanup_views":
            try:
                result = self.selected_db.view_cleanup
                if result:
                    QMessageBox(QMessageBox.Information, 'Information', 
'''"Cleanup Views" was initiated successfully!!!
Server url: "%s"
Database name: "%s"
Date: %s''' % (self.server['url'], self.selected_db.name, datetime.now().strftime(DATETIME_FMT),), QtGui.QMessageBox.Ok).exec_() 
                else:
                    self.show_error(command, params, "Error status was returned by the wrapper")  
            except:
                self.show_error(command, params, sys.exc_info()[1])
        
        elif command == "compact_db" :
            try:
                self.selected_db.compact
                QMessageBox(QMessageBox.Information, 'Information', 
'''"Compact Database" was initiated successfully!!!
Server url: "%s"
Database name: "%s"
Date: %s''' % (self.server['url'], self.selected_db.name, datetime.now().strftime(DATETIME_FMT),), QtGui.QMessageBox.Ok).exec_()             
            except:
                self.show_error(command, params, sys.exc_info()[1]) 
        
        elif command == "compact_views":
            result_arr = []
            try:
                for view in self.view_model.view_list:
                    result = self.selected_db.compact_view(view["name"])
                    #print "%s: %s" % (view["name"], (lambda:"Yes", lambda:"No")[result](),)
                    result_arr.append("%s: %s" % (view["name"], {True: "Yes", False: "No"}[result],))
                report = "\n".join(["%s" % d for d in result_arr])
                QMessageBox(QMessageBox.Information, 'Information', 
'''"Compact Views" was initiated successfully!!!
Server url: "%s"
Database name: "%s"
Date: %s
Report: %s''' % (self.server['url'], self.selected_db.name, datetime.now().strftime(DATETIME_FMT), report,), QtGui.QMessageBox.Ok).exec_()                     
            except:
                self.show_error(command, params, sys.exc_info()[1])
        elif command == "compact_view":
            try:
                result = self.selected_db.compact_view(params["view_name"])
                report = "%s: %s" % (params["view_name"], {True: "Yes", False: "No"}[result],)
                QMessageBox(QMessageBox.Information, 'Information', 
'''"Compact View" was initiated successfully!!!
Server url: "%s"
Database name: "%s"
View name: %s
Date: %s
Report: %s''' % (self.server['url'], self.selected_db.name, params["view_name"], datetime.now().strftime(DATETIME_FMT), report,), QtGui.QMessageBox.Ok).exec_()                     
            except:
                self.show_error(command, params, sys.exc_info()[1])
                
    def show_error(self,command, params, error):
        """Show messageBox with information about error in db functionality 
        """
        QMessageBox(QMessageBox.Critical, 'Error', 
'''Error while work on command "%s"
Server url: "%s"
Database name: "%s"
Parameters: %s
Date: %s
Error: %s''' % (command, self.server['url'], self.selected_db.name, params,datetime.now().strftime(DATETIME_FMT), error), QtGui.QMessageBox.Ok).exec_()        
    
    def disabling_refresh(self):
        """Disable refresh button 
        """
        self.ui.btn_refresh_all.setEnabled(False)
        self.ui.lbl_last_update.setText("Unknown")
        
    def workerTimer_update(self):
        """Main worker loop 
        """
        remove_ready = []
        i = 0
        flag_was_changes = False
        for worker_obj in self.view_workers_list:
            worker = worker_obj['pipe']
            while worker.poll():
                data = worker.recv()
                if "error" in data:
                    QMessageBox(QMessageBox.Critical, 'Error', 
'''Error while work on command "%s"
Server url: "%s"
Database name: "%s"
Parameters: %s
Date: %s
Error: %s''' % (data["command"], data['url'], data['db_name'], data["params"], data["updated"], data["error"],), QtGui.QMessageBox.Ok).exec_()
                    remove_ready.append(worker_obj)
                    flag_was_changes = True   
                else:
                    if "command" in data:
                        if data["command"] == "get_info":
                            serv = self.server_view_list[data['url']]
                            db_heandler = serv[data['db_name']]
                            row_heandler = db_heandler[data['params']["row_id"]]
                            result_heandler = data['result']
                            row_heandler['view_index'] = result_heandler['view_index']
                            row_heandler["refreshing"] = "ready"
                            remove_ready.append(worker_obj)
                            flag_was_changes = True
                            

                            
                            
                        elif data["command"] == "ping":
                            QMessageBox(QMessageBox.Information, 'Information', 
'''Ping complete successfully!!!
Server url: "%s"
Database name: "%s"
View name: "%s"
Done on: %s''' % (data['url'], data['db_name'], data["params"]["view_name"], data["updated"],), QtGui.QMessageBox.Ok).exec_()
                            remove_ready.append(worker_obj)
                            flag_was_changes = True   
                i += 1
        
        
        for worker in remove_ready:
            self.view_workers_list.remove(worker)
        
        if flag_was_changes:
            self.view_model.update_data()
            for i in range(self.view_model.columnCount()):
                self.ui.tlw_view_list.resizeColumnToContents(i) 
            

        
    def closeEvent(self,event):
        try:
            self.mainWindow.dbmanager_windows.remove(self)
        except:
            #print "error removing from db manager windows list"
             logging.debug('ReplicationWindow: error removing from db manager windows list')
        