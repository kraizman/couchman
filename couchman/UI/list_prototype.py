from PyQt4 import QtGui, QtCore

class ServersList(QtGui.QTreeView):
    
    def currentChanged(self,cur_index,prev_index):
        self.emit(QtCore.SIGNAL("list_currentChanged(const QModelIndex & )"),cur_index)
        
        
class DBList(QtGui.QListView):
    
    def currentChanged(self,cur_index,prev_index):
        self.emit(QtCore.SIGNAL("list_currentChanged(const QModelIndex & )"),cur_index)
        
    