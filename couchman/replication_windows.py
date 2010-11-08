from UI.UI_New_Task import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from config import *
import logging

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
        
        if cur_type == 0:
            txt_lst = replication_record.get('task').split(' ')
           
            task_source = txt_lst[1]
            task_target = txt_lst[3]
            
            self.ui.txt_source.setText(task_source)
            self.ui.txt_target.setText(task_target)
            
            
    def add_react(self):
        """Slot for signal "clicked()" of "Add" button 
        """
        if self.validate():
        
            source = str(self.ui.txt_source.text())
            target = str(self.ui.txt_target.text())
            proxy = str(self.ui.txt_proxy.text())
            
            if source.startswith("http"):
                if not source.endswith("/"):
                    source += "/"
            if target.startswith("http"):
                if not target.endswith("/"):
                    target += "/"
            
            new_relication = {'source': source, 'target': target, 'proxy': proxy}
    
            if new_relication in self.server_obj.get('replications'):
                QMessageBox(QMessageBox.Warning, 'Warning', 'Record for this replication already exist!!!', QtGui.QMessageBox.Ok).exec_()
            else:
                self.mainWindow.dump_replication_record(self.server_obj, new_relication)
                self.close()
                
        
                   
    def cancel_react(self):
        self.close()
    
    
    def validate(self):
        if str(self.ui.txt_source.text()) == "":
            QMessageBox(QMessageBox.Critical, 'Error', 'Source field are required', QtGui.QMessageBox.Ok).exec_()
            return False
        
        if str(self.ui.txt_target.text()) == "":
            QMessageBox(QMessageBox.Critical, 'Error', 'Target field are required', QtGui.QMessageBox.Ok).exec_()
            return False
    
        return True
        
    def closeEvent(self,event):
        try:
            self.mainWindow.replication_windows.remove(self)
        except:
            print "error removing from replication windows list"
        
        