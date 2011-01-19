from UI.UI_MainWindow import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from couchdbcurl import Server
from models import ServerTreeModel, TaskTreeModel
from server_windows import ServerWindow
from replication_windows import ReplicationWindow
from db_manager import DBManager
from workers import ServerWorker, ReplicationWorker
from config import *
from db_json import MyJson
import multiprocessing
import logging
import sys
from time import sleep

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        logging.debug("MainWindow: init")
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        logging.debug('MainWindow: Create myJson class')
        self.myJson = MyJson()
        logging.debug('MainWindow: Getting data from json file')
        self.MAIN_DB = self.myJson.readFromDB()
        
       
        #set model for server treeview
        logging.debug("MainWindow: set model for server treeview list")
        self.server_model = ServerTreeModel(self)
        self.ui.tlw_servers.setModel(self.server_model)
        self.server_model.servers = self.MAIN_DB
        self.ui.tlw_servers.setColumnWidth(0,24)
        self.server_model.reset()
        self.ui.tlw_servers.setSortingEnabled(False)
        
        
        self.connect(self.ui.tlw_servers, QtCore.SIGNAL('list_currentChanged (const QModelIndex &)'), self.server_selection_changed)
        self.connect(self.ui.tlw_replications, QtCore.SIGNAL('list_currentChanged (const QModelIndex &)'), self.replication_selection_changed)

        #worker's main timer
        logging.debug("MainWindow: create timer for wokers main loop")
        self.timer = QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.mainTimer_update)
        
        #init lists and dicts for internal use
        self.server_workers = {}
        self.replication_workers = []
        self.model_list = {}
        self.server_view_list = {}
        
        self.server_windows = []
        self.replication_windows = []
        self.dbmanager_windows = []

        #start workers for each server and assign task model record
        for serv in self.MAIN_DB:
            self.start_worker('server', serv)
            tasks_model = TaskTreeModel(serv)
            self.model_list[serv['url']] = tasks_model
            
        logging.debug("MainWindow: connect buttons to Signals ")
        #buttons connectors
        self.connect(self.ui.btn_addserver, QtCore.SIGNAL("clicked()"), self.btn_add_server_react)
        self.connect(self.ui.btn_editserver, QtCore.SIGNAL("clicked()"), self.btn_edit_server_react)
        self.connect(self.ui.btn_rmserver, QtCore.SIGNAL("clicked()"), self.btn_rm_server_react)
        self.connect(self.ui.btn_addtask, QtCore.SIGNAL("clicked()"), self.btn_add_replication_react)
        self.connect(self.ui.btn_starttask, QtCore.SIGNAL("clicked()"), self.btn_start_replication_react)
        self.connect(self.ui.btn_start_con, QtCore.SIGNAL("clicked()"), self.btn_start_con_replication_react)
        self.connect(self.ui.btn_stoptask, QtCore.SIGNAL("clicked()"), self.btn_stop_replication_react)
        self.connect(self.ui.btn_rmtask, QtCore.SIGNAL("clicked()"), self.btn_remove_replication_react)
        self.connect(self.ui.btn_refresh_sel, QtCore.SIGNAL("clicked()"), self.btn_refresh_react)
        
        self.connect(self.ui.btn_dbmanager, QtCore.SIGNAL("clicked()"), self.btn_dbmanager_react)
        
        index = self.ui.tlw_servers.model().index(0,0)
        self.ui.tlw_servers.setCurrentIndex(index)
        
        logging.debug("MainWindow: add images for buttons")
        self.ui.btn_addserver.setIcon(QtGui.QIcon(ROOT_DIR+'/media/true_state.png'))
        self.ui.btn_rmserver.setIcon(QtGui.QIcon(ROOT_DIR+'/media/false_state.png'))
        self.ui.btn_editserver.setIcon(QtGui.QIcon(ROOT_DIR+'/media/options.png'))
        
        self.ui.btn_starttask.setIcon(QtGui.QIcon(ROOT_DIR+'/media/play.png'))
        self.ui.btn_start_con.setIcon(QtGui.QIcon(ROOT_DIR+'/media/play2.png'))
        self.ui.btn_stoptask.setIcon(QtGui.QIcon(ROOT_DIR+'/media/stop.png'))
        self.ui.btn_addtask.setIcon(QtGui.QIcon(ROOT_DIR+'/media/true_state.png'))
        self.ui.btn_rmtask.setIcon(QtGui.QIcon(ROOT_DIR+'/media/false_state.png'))
        
        self.ui.btn_refresh_sel.setIcon(QtGui.QIcon(ROOT_DIR+'/media/refresh.png'))
        self.ui.btn_dbmanager.setIcon(QtGui.QIcon(ROOT_DIR+'/media/workflow.png'))
        
        self.timer.start(300)
        
    
    def start_worker(self,type,data):
        """Start multiprocessing worker of given type.
        """
        if type == 'server':
            logging.debug("MainWindow: start server worker for %s" % data["url"])
            self_pipe, remote_pipe = multiprocessing.Pipe(duplex = True)
            connector = ServerWorker(remote_pipe,data)
            self.server_workers[data['url']] = {'pipe':self_pipe,'thread':connector}
            connector.start()
            self_pipe.send({'command':'update_server'})
        elif type == 'replication':
            logging.debug("MainWindow: start replication worker for %s" % data["server"])
            self_pipe, remote_pipe = multiprocessing.Pipe(duplex = True)
            connector = ReplicationWorker(remote_pipe,data)
            self.replication_workers.append({"pipe":self_pipe,"thread":remote_pipe})
            connector.start()
            return self_pipe
      
    def server_selection_changed(self,cur_index):
        """Signal slot for servers tree view list current index change
        """
        cur_record = self.server_model.data(cur_index, SERVER_INFO_ROLE)
        self.ui.lbl_srv_addres.setText('<a href="%(url)s%(pref)s">%(url)s</a>' % {'url': cur_record['url'], 'pref':"/_utils"})
        self.ui.lbl_srv_group.setText(cur_record['group'])
        self.ui.lbl_srv_name.setText(cur_record['name'])
        self.ui.lbl_period.setText(str(cur_record['autoupdate']))
        if cur_record.get('last_update'):
            self.ui.lbl_lastupdate.setText(cur_record.get('last_update').strftime(DATETIME_FMT))
        else:
            self.ui.lbl_lastupdate.setText("infinity")
        self.ui.btn_refresh_sel.setEnabled(True)
        #self.replicationListEnabled(False)
        
        if cur_record.get('enabled') == '2':
            self.ui.lbl_status.setText('Enabled')
            self.tasks_model = self.model_list[cur_record['url']]
            self.ui.tlw_replications.setModel(self.tasks_model)
            self.tasks_model.update_data()
            
            self.ui.btn_addserver.setEnabled(True)
            self.empty_rep_list_status()
            
  
            if len(self.tasks_model.tasks_rendered) == 0:
                self.ui.tlw_replications.setEnabled(False)
            else:
                self.ui.tlw_replications.setEnabled(True)
                
            for i in range(self.tasks_model.columnCount()):
                self.ui.tlw_replications.resizeColumnToContents(i) 
               
            
        else:
            self.ui.lbl_status.setText('Disabled')
            self.tasks_model = self.model_list[cur_record['url']]
            self.ui.tlw_replications.setModel(self.tasks_model)
            self.tasks_model.update_data()
            self.replicationListEnabled(False)
            self.empty_rep_list_status()
            
    
    def replication_selection_changed(self, cur_index):
        """Signal slot for replications tree view list current index change
        """
        cur_record = self.tasks_model.data(cur_index, TASK_INFO_ROLE)
        if cur_record is not None:
            persisted = cur_record.get('record_type')
            if persisted == 0:
                self.ui.btn_addtask.setEnabled(True)
                self.ui.btn_stoptask.setEnabled(True)
                self.ui.btn_rmtask.setEnabled(False)
                self.ui.btn_starttask.setEnabled(False)
                self.ui.btn_start_con.setEnabled(False)
                self.ui.btn_stoptask.setEnabled(True)
            elif persisted == 1:
                self.ui.btn_addtask.setEnabled(True)
                self.ui.btn_stoptask.setEnabled(True)
                self.ui.btn_rmtask.setEnabled(True)
                self.ui.btn_starttask.setEnabled(False)
                self.ui.btn_start_con.setEnabled(False)
                self.ui.btn_stoptask.setEnabled(True)
            elif persisted == 2:
                self.ui.btn_addtask.setEnabled(True)
                self.ui.btn_stoptask.setEnabled(False)
                self.ui.btn_rmtask.setEnabled(True)
                self.ui.btn_starttask.setEnabled(True)
                self.ui.btn_start_con.setEnabled(True)
                self.ui.btn_stoptask.setEnabled(False)
            else:
                self.empty_rep_list_status()
        else:
            self.empty_rep_list_status()
    
    def empty_rep_list_status(self):
        """Disable buttons control buttons except "Add task"
        """
        self.ui.btn_addtask.setEnabled(True)
        self.ui.btn_stoptask.setEnabled(False)
        self.ui.btn_rmtask.setEnabled(False)
        self.ui.btn_starttask.setEnabled(False)
        self.ui.btn_start_con.setEnabled(False)
        self.ui.btn_stoptask.setEnabled(False)   
      
    def replicationListEnabled(self,state):
        """Disable or enable control buttons
        """
        self.ui.tlw_replications.setEnabled(state)
        self.ui.btn_starttask.setEnabled(state)
        self.ui.btn_stoptask.setEnabled(state)
        self.ui.btn_start_con.setEnabled(state)
        self.ui.btn_rmtask.setEnabled(state)
        self.ui.btn_addtask.setEnabled(state)
        
      

    def btn_add_server_react(self):
        """Slot for Signal"clicked()" of "Add server" button
        """
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        newserver_win = ServerWindow(self, "new", selectedServer)
        newserver_win.show()
        self.server_windows.append(newserver_win)
        
    def btn_edit_server_react(self):
        """Slot for Signal"clicked()" of "Edit server" button
        """
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        editserver_win = ServerWindow(self, "edit", selectedServer)
        editserver_win.show()
        self.server_windows.append(editserver_win)
    
    def btn_add_replication_react(self):
        """Slot for Signal"clicked()" of "Add replication" button
        """
        selectedServer = self.server_model.data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        if len(self.tasks_model.tasks_rendered) > 0:
            selected_task = self.tasks_model.data(self.ui.tlw_replications.currentIndex(), TASK_INFO_ROLE)
        else:
            selected_task = None
        add_replication_win = ReplicationWindow(self, selectedServer, selected_task)
        add_replication_win.show()
        self.replication_windows.append(add_replication_win)

    
    def btn_remove_replication_react(self):
        """Slot for Signal"clicked()" of "Remove server" button
        """
        self.remove_replication()
        
        
    def btn_start_replication_react(self):
        """Slot for Signal"clicked()" of "Start replication" button
        """
        self.start_replication(False)
        
    def btn_start_con_replication_react(self):
        """Slot for Signal"clicked()" of "Start continuous replication" button
        """
        self.start_replication(True)
        
    
    def btn_stop_replication_react(self):
        """Slot for Signal"clicked()" of "Stop replication" button
        """
        self.stop_replication()
        
    def btn_refresh_react(self):
        """Slot for Signal"clicked()" of "Refresh" button
        """
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        #send signal to worker for update data    
        cur_worker = self.server_workers.get(selectedServer.get('url')).get('pipe')
        cur_worker.send({'command': 'update_server'})
    
    def btn_dbmanager_react(self):
        """Slot for Signal"clicked()" of "DB manager" button
        """
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        dbmanager_win = DBManager(self.server_view_list,self, self.MAIN_DB,selectedServer)
        dbmanager_win.show()
        self.dbmanager_windows.append(dbmanager_win) 
    
    def remove_replication(self):
        """Remove selected replication of selected server
        """
        selected_task = self.tasks_model.data(self.ui.tlw_replications.currentIndex(), TASK_INFO_ROLE)
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)

        txt_lst = selected_task.get('task').split(' ')
        if selected_task.get('record_type') != 2:
            task_source = txt_lst[1]
            task_target = txt_lst[3]
        else:
            task_source = txt_lst[0]
            task_target = txt_lst[2]
            
        msg = "%s - > %s" % (task_source, task_target)
        if QMessageBox(QMessageBox.Warning, 'Warning', 'Remove replication record {%s} from "%s"?' % (msg, selectedServer.get('url')), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_() == QtGui.QMessageBox.Yes:            
            rep_list = selectedServer.get('replications')
            for rep in rep_list:
                if rep['source'] == task_source and rep['target'] == task_target:
                    rep_list.remove(rep)       
                    self.myJson.save()
            if len(self.tasks_model.tasks_rendered) < 2:
                self.empty_rep_list_status()
            pipe = self.server_workers.get(selectedServer.get('url')).get('pipe')
            pipe.send({"command": "update_server"})
                
       
    def start_replication(self,type):
        """Start selected replication on selected server if it not running yet 
        """
        selected_task = self.tasks_model.data(self.ui.tlw_replications.currentIndex(), TASK_INFO_ROLE)
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        print selected_task
        txt_lst = selected_task.get('task').split(' ')
        if selected_task.get('record_type') != 2:
            task_source = txt_lst[1]
            task_target = txt_lst[3]
        else:
            task_source = txt_lst[0]
            task_target = txt_lst[2]  

        
        if QMessageBox(QMessageBox.Question, 'Warning', 
'''Start replication
    {source: "%s"
    target: "%s"
    continuous: %s
    proxy: %s
    filter: %s
    query: %s} ? 
    ''' % (task_source, task_target, type, selected_task.get('proxy',""), selected_task.get('filter',""), selected_task.get('query',"")), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_() == QtGui.QMessageBox.Yes:
            logging.debug("MainWindow: start replication, continuous %s" % type)
            pipe = self.start_worker('replication',{
                                            'source': task_source,
                                            'target': task_target,
                                            'continuous': type,
                                            'filter': selected_task.get('filter', ""),
                                            'query': selected_task.get('query', ""),
                                            'proxy': selected_task.get('proxy', ""),
                                            'server': selectedServer,
                                            })
            pipe.send({'command': 'start_replication'})
      
    def stop_replication(self):
        """Stop selected replication on selected server of it running
        """
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        selected_task = self.tasks_model.data(self.ui.tlw_replications.currentIndex(), TASK_INFO_ROLE)
        txt_lst = selected_task.get('task').split(' ')
        if selected_task.get('record_type') != 2:
            task_source = txt_lst[1]
            task_target = txt_lst[3]
        else:
            task_source = txt_lst[0]
            task_target = txt_lst[2]  
        if QMessageBox(QMessageBox.Question, 'Warning', 
'''Stop replication
    {source: "%s"
    target: "%s"
    proxy: %s
    filter: %s
    query: %s} ? 
    ''' % (task_source, task_target, selected_task.get('proxy',""), selected_task.get('filter',""), selected_task.get('query',"")), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_() == QtGui.QMessageBox.Yes:
            logging.debug("MainWindow: stop replication")
            pipe =self.start_worker('replication', {
                                            'source': task_source,
                                            'target': task_target,
                                            'filter': selected_task.get('filter', ""),
                                            'query': selected_task.get('query', ""),
                                            'proxy': selected_task.get('proxy', ""),
                                            'server': selectedServer,
                                            })
            pipe.send({'command': 'stop_replication'})

            
    
    def dump_replication_record(self,server,record):
        """Dump replication record to persisted list
        """
        logging.debug("MainWindow: replication record adding")
        rep_list = server.get('replications')
        rep_list.append(record)
        if self.myJson.save():
            pipe = self.server_workers.get(server.get('url')).get('pipe')
            pipe.send({"command": 'update_server'})
        else:
            #print "error saving"
            logging.debug('MainWindow:error saving')
    
    def dump_server_record(self,record):
        """Dump server record to persisted list
        """
        logging.debug("MainWindow: server record adding")
        self.MAIN_DB.append(record)
        if self.myJson.save():
            tasks_model = TaskTreeModel(record)
            self.model_list[record['url']] = tasks_model 
            self.server_model.update_data()
        else:
            #print "error saving"
            logging.debug('MainWindow:error saving')
    
    def btn_rm_server_react(self):
        """Slot for Signal"clicked()" of "Remove server" button
        """
        selectedServer = self.server_model.data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        if QMessageBox(QMessageBox.Warning, 'Warning', 'Remove records for "%s"?' % (selectedServer.get('url')), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_() == QtGui.QMessageBox.Yes:
            
            pos = self.ui.tlw_servers.currentIndex().row()
            item = self.server_workers[selectedServer['url']]
            item['thread'].terminate()
            
            del self.server_workers[selectedServer['url']]
            del self.model_list[selectedServer['url']]
            
            self.server_model.removeServRecord(selectedServer)
            self.myJson.save()
            
            if pos == self.server_model.rowCount() and pos > 0:
                index = self.ui.tlw_servers.model().index(pos-1, 0)
                self.ui.tlw_servers.setCurrentIndex(index)
            
            if self.server_model.rowCount() == 0:
                self.ui.btn_rmserver.setEnabled(False)
                self.ui.tlw_servers.setEnabled(False)
                self.ui.tlw_replications.setEnabled(False)
                
                self.ui.formLayout_3.setEnabled(False)
                
                self.ui.btn_starttask.setEnabled(False)
                self.ui.btn_stoptask.setEnabled(False)
                self.ui.btn_addtask.setEnabled(False)
                self.ui.btn_rmtask.setEnabled(False)
                self.ui.btn_editserver.setEnabled(False)
                
                self.ui.lbl_srv_group.setText("")
                self.ui.lbl_srv_addres.setText("")
                self.ui.lbl_srv_name.setText("")
                self.ui.lbl_status.setText("")
                self.ui.lbl_lastupdate.setText("")
                self.ui.lbl_period.setText("")
                self.ui.btn_refresh_sel.setEnabled(False)
        
        
    
    def mainTimer_update(self):
        """Main worker loop. Take care for data that was received from workers of each type
        """
        
        for item_key in self.server_workers:
            obj = self.server_workers[item_key]
            worker = obj.get('pipe')
            while worker.poll():
                data = worker.recv()
                if "command" in data:
                    if data["command"] == "update_server":
                        #print "timer: update server status for %s" % data["url"]
                        #print "new task list: %s" % data.get('tasks')
                        
                        self.update_server_data(data.get("url"), data.get("data"))
        
        for rep in self.replication_workers:
            worker = rep.get('pipe')
            while worker and worker.poll():
                data = worker.recv()
                if "command" in data:
                    if data.get("command") == "error":
                        QMessageBox(QMessageBox.Critical, 'Error',  
''''
Error in replicating process.
Error details:
     Replication source: "%s"
     Replication target: "%s"
     continuous: %s
     proxy: %s
     filter: %s
     query: %s
     error: %s ''' % (data.get('source'), data.get('target'), data.get('continuous'),
                      data.get("proxy", ""), data.get("filter", ""), 
                      data.get("query", ""), data.get('error')), QtGui.QMessageBox.Ok).exec_()
                    else:
                        QMessageBox(QMessageBox.Information, 'Information', 
'''
%s
    source: "%s"
    target: "%s"
    continuous: %s
    proxy: %s
    filter: %s
    query: %s
     ''' % (data.get('message'), data.get('source'), data.get('target'), data.get('continuous'),
            data.get("proxy", ""), data.get("filter", ""), 
            data.get("query", "")), QtGui.QMessageBox.Ok).exec_()
                        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(),SERVER_INFO_ROLE)
                        if selectedServer.get('url') == data.get('url'):
                            pipe = self.server_workers.get(data.get('url')).get('pipe')
                            pipe.send({"command": "update_server"})
                        
                        
                    self.replication_workers.remove(rep)
                    
                        
    def update_server_data(self,address,data):
        """Update server data record that was received by worker
        """
        selectedServer = self.ui.tlw_servers.model().data(self.ui.tlw_servers.currentIndex(), SERVER_INFO_ROLE)
        serv_record = self.server_model.getServByAddress(address)
        
        if data['enabled']:
            serv_record['enabled'] = '2'
        else:
            serv_record['enabled'] = '0'
        updeted = data.get('updated')
        serv_record['last_update'] = updeted
        self.model_list[address].update_runetime(data.get('tasks'))
        serv_record["version"] = data["version"]
        if  selectedServer == serv_record:
            
            self.ui.lbl_lastupdate.setText(updeted.strftime(DATETIME_FMT))
            if serv_record['enabled'] == '2':
                self.ui.lbl_status.setText('Enabled')
            else:
                self.ui.lbl_status.setText('Disabled')  
            
            if len(self.tasks_model.tasks_rendered) == 0:
                self.empty_rep_list_status()
            else:
                self.ui.tlw_replications.setEnabled(True)
           
        self.server_model.update_data();  
        
  
    def closeEvent(self,event):
        """Close all workers and opened windows before closing self
        """
        self.timer.stop()
        
        for win in self.server_windows:
            win.close()
            
        for win in self.replication_windows:
            win.close()
            
        for win in self.dbmanager_windows:
            win.close()
        
        
        #print "MainWindow: terminate server workers"
        logging.debug('MainWindow:terminate server workers')
        for key in self.server_workers:
            worker = self.server_workers[key]
            worker.get('thread').terminate()
   
        for rep in self.replication_workers:
            rep.get('thread').terminate()
            
        event.accept()
        