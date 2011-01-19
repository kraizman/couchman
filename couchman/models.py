import logging
from config import *
from datetime import datetime
from PyQt4 import QtGui, QtCore
from operator import itemgetter

class ServerTreeModel(QtCore.QAbstractTableModel):
    def __init__(self, mainWindow,parent = None):
        super(ServerTreeModel, self).__init__(parent)
        self.servers = []
        self.headers = (" ", "Name", "Group", "Info")
        self.mainWindow = mainWindow;
        self.enabled_brush = QtGui.QBrush()
        self.enabled_brush.setColor(QtGui.QColor(0,200,0))
        
        self.disabled_brush = QtGui.QBrush()
        self.disabled_brush.setColor(QtCore.Qt.gray)
        
        

    def columnCount(self, parent=None):
            return len(self.headers)
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.servers)
    
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 1:
                return self.servers[index.row()].get('name')
            elif index.column() == 2:
                return self.servers[index.row()].get('group')
            elif index.column() == 3:
                return self.servers[index.row()].get('version')
    
        elif role == QtCore.Qt.ForegroundRole:
            if index.column() == 1:
                if(self.servers[index.row()].get('enabled') == '2'):
                    return self.enabled_brush
                else:
                    return self.disabled_brush
        elif role == SERVER_INFO_ROLE:
            return self.servers[index.row()]
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                obj = self.servers[index.row()]
                last = obj.get('last_update')
                if last:
                    delta = datetime.now() - last
                    dif = delta.seconds
                else:
                    dif = INFINITY
                str_autoupdate = self.servers[index.row()].get('autoupdate')
                if str_autoupdate == "None":
                    period = -1.0
                else:
                    period = float(str_autoupdate)
                    
                if period < 0:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_blue.png')
                elif dif > 5 * period:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_red.png')
                elif dif > 2 * period:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_orange.png')
                else:
                    return QtGui.QIcon(ROOT_DIR+'/media/circle_green.png')
            
        return None
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass

        return None
    
    def getServByAddress(self,address):
        for serv in self.servers:
            if serv['url'] == address:
                return serv
        return None

    def removeServRecord(self,serv_obj):
        try:
            self.servers.remove(serv_obj)
            logging.debug("ServerModel: remove record complete")
            self.update_data()
        except:
            logging.debug("ServerModel: remove record error")
        
    def update_data(self):
        self.sort(1,QtCore.Qt.AscendingOrder)
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
        
        
    def sort(self, Ncol, order):
        self.servers.sort(cmp=self.cmp_func, reverse=order)
        #self.update_data()

    def cmp_func(self,a,b):

        if a['group'] == b['group']:
            return cmp(a['name'], b['name'])
        else:
            return cmp(a['group'], b['group'])


class TaskTreeModel(QtCore.QAbstractTableModel):
    def __init__(self, serv_obj,parent = None):
        super(TaskTreeModel, self).__init__(parent)
        self.tasks_rendered = []
        self.runetime = []
        self.need_rendering = True
        self.server_list = serv_obj['replications']

        self.server_obj = serv_obj
        self.headers = ("Type", "Task", "Status", "Pid", "Info")
        self.active_brush = QtGui.QBrush()
        self.active_brush.setColor(QtGui.QColor(0,200,0))
        
        self.nonactive_brush = QtGui.QBrush()
        self.nonactive_brush.setColor(QtCore.Qt.red)

    def columnCount(self, parent=None):
            return len(self.headers)
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.need_rendering:
            self.render()
        return len(self.tasks_rendered)
    
    
    def data(self, index, role):
        if not index.isValid() or index.row() < 0:
            return None
        if self.need_rendering:
            self.render()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.ToolTipRole:
            if index.column() == 0:
                if self.tasks_rendered[index.row()].get('record_type') != 2:
                    return self.tasks_rendered[index.row()].get('type')
                else:
                    return "Replication"
            if index.column() == 1:
                return self.tasks_rendered[index.row()].get('task')
            if index.column() == 2:
                if self.tasks_rendered[index.row()].get('record_type') != 2:
                    return self.tasks_rendered[index.row()].get('status')
                else:
                    return ""
            if index.column() == 3:
                if self.tasks_rendered[index.row()].get('record_type') != 2:
                    return self.tasks_rendered[index.row()].get('pid')
                else:
                    return ""
            if index.column() == 4:
                 if self.tasks_rendered[index.row()].get('record_type') == 2:
                     return "proxy: %s, filter: %s, query_params: %s" % (self.tasks_rendered[index.row()].get('proxy', ""),
                                                                         self.tasks_rendered[index.row()].get('filter', ""),
                                                                         self.tasks_rendered[index.row()].get('query', ""))
                 else:
                     return ""
            
        elif role == QtCore.Qt.ForegroundRole:
            if self.tasks_rendered[index.row()].get('record_type') == 1:
                return self.active_brush
            elif self.tasks_rendered[index.row()].get('record_type') == 2:
                return self.nonactive_brush
            else:
                return QtGui.QBrush()
        elif role == TASK_INFO_ROLE:
            try:
                return self.tasks_rendered[index.row()]
            except:
                return None

        return None
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass

        return QtCore.QVariant()
    
    def finde(self,source,target):
        for rec in self.tasks_rendered:
            if rec.get('type') == 'Replication':
                txt_lst = rec.get('task').split(' ')
                if rec.get('record_type') != 2:
                    task_source = txt_lst[1]
                    task_target = txt_lst[3]
                else:
                    task_source = txt_lst[0]
                    task_target = txt_lst[2]      
                                 
                if task_source == source and task_target == target:
                    return rec
        return None
         
    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
            
        #self.reset()
       
                   
        
    def update_runetime(self,runetime_list):
        if runetime_list is not None:
            self.runetime = runetime_list
        else:
            self.runetime = []
        self.need_rendering = True
        self.update_data()
    
    def render(self):
        self.tasks_rendered = []
        for task in self.runetime:
            task['record_type'] = 0
            self.tasks_rendered.append(task)
            
        nonactive = []
  
        for rec in self.server_list:
            isNonActive = True
            for task in self.tasks_rendered:
                if task.get('type') == 'Replication':
                    txt_lst = task.get('task').split(' ')
                    task_source = txt_lst[1]
                    task_target = txt_lst[3]
                    
                    if rec['source'] == task_source and rec['target'] == task_target:
                        task['record_type'] = 1
                        isNonActive = False
            if isNonActive:
                nonactive.append(rec)
        
        for rec in nonactive:
            msg = "%s -> %s" % (rec['source'], rec['target'])
            self.tasks_rendered.append({'task': msg,'record_type': 2, 'proxy': rec.get('proxy',""), 'filter': rec.get('filter', ""), 'query': rec.get('query',"")})
        
        self.need_rendering = False
        self.update_data()
    

        
class DBListModel(QtCore.QAbstractTableModel):
    def __init__(self, server_dbs, db_list,parent = None):
        super(DBListModel, self).__init__(parent)
        self.db_list = []#{'names':[], 'sizes':[], 'docs':[]} 
        self.server_dbs = {}
        self.headers = ("Database", "Size", "Documents",)
        if server_dbs:
            self.server_dbs = server_dbs
        if db_list:
            self.db_list = db_list       

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.db_list)
    
    def columnCount(self, parent=None):
            return len(self.headers)
    
    
    def headerData(self, column, orientation, role):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            try:
                return self.headers[column]
            except IndexError:
                pass

        return None
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return self.db_list[index.row()]
            elif index.column() == 1:
                name = self.db_list[index.row()]
                size_byte = self.server_dbs[name]["size"]
                return self.splitthousands(str(size_byte))
            elif index.column() == 2:
                name = self.db_list[index.row()]
                return self.splitthousands(str(self.server_dbs[name]["docs"]))

        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                return QtGui.QIcon(ROOT_DIR+'/media/database.png')
            
        elif role == QtCore.Qt.TextAlignmentRole:
            if index.column() !=0:
                return QtCore.Qt.AlignRight
        return None
    
    def splitthousands(self,s, sep=','):  
        if len(s) <= 3: return s  
        return self.splitthousands(s[:-3], sep) + sep + s[-3:]
    
    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))

class DBViewModel(QtCore.QAbstractTableModel):
    def __init__(self, view_list,parent = None):
        super(DBViewModel, self).__init__(parent)
        self.view_list = [] 
        self.headers = (" ", "Name", "Revision","Signature", "Size", "Language", "Clients", "Update", "P.S.", "C.R.", "W.C.", "U.R.", )
        self.colum_tips = ("Status", "View name", "Revision of View", "Signature of View", "Size on disk in MB", "Programming language of View",
                           "Waiting clients", "Update sequence", "Purge sequence", "Is compact running (+ equals True, - equals False)",
                           "Is waiting commit (+ equals True, - equals False)", "Is updater running (+ equals True, - equals False)",  )
        if view_list:
            self.view_list = view_list       

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.view_list)
    
    def columnCount(self, parent=None):
            return len(self.headers)
    
    
    def headerData(self, column, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                try:
                    return self.headers[column]
                except IndexError:
                    pass
            elif role == QtCore.Qt.ToolTipRole:
                try:
                    return self.colum_tips[column]
                except IndexError:
                    pass
                

        return None
    
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 1:
                return self.view_list[index.row()].get('name')
            elif index.column() == 2:
                return self.view_list[index.row()].get('revision')
            if self.view_list[index.row()].get('view_index'):
                if index.column() == 3:
                    return self.view_list[index.row()].get('view_index').get('signature')
                elif index.column() == 4:
                    size_byte = self.view_list[index.row()].get('view_index').get('disk_size')
                        
                    return self.splitthousands(str(size_byte))
                elif index.column() == 5:
                    return self.view_list[index.row()].get('view_index').get('language')
                elif index.column() == 6:
                    return self.view_list[index.row()].get('view_index').get('waiting_clients')
                elif index.column() == 7:
                    return self.view_list[index.row()].get('view_index').get('update_seq')
                elif index.column() == 8:
                    return self.view_list[index.row()].get('view_index').get('purge_seq')

        
        elif role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                if self.view_list[index.row()].get('refreshing') and self.view_list[index.row()]['refreshing'] == "now":
                    return QtGui.QIcon(ROOT_DIR+'/media/refresh.png')
                else:
                    return QtGui.QIcon(ROOT_DIR+'/media/true_symbol.png')
            if self.view_list[index.row()].get('view_index'):
                if index.column() == 9:
                    if self.view_list[index.row()].get('view_index').get('compact_running'):
                        return QtGui.QIcon(ROOT_DIR+'/media/true_state.png')
                    else:
                        return QtGui.QIcon(ROOT_DIR+'/media/false_state.png')
                elif index.column() == 10:
                    if self.view_list[index.row()].get('view_index').get('waiting_commit'):
                        return QtGui.QIcon(ROOT_DIR+'/media/true_state.png')
                    else:
                        return QtGui.QIcon(ROOT_DIR+'/media/false_state.png')
                elif index.column() == 11:
                    if self.view_list[index.row()].get('view_index').get('updater_running'):
                        return QtGui.QIcon(ROOT_DIR+'/media/true_state.png')
                    else:
                        return QtGui.QIcon(ROOT_DIR+'/media/false_state.png')          
               
        elif role == VIEW_INFO_ROLE:
            return self.view_list[index.row()]
        
        elif role == QtCore.Qt.TextAlignmentRole:
            if self.view_list[index.row()].get('view_index'):
                if index.column() == 4 or index.column() == 6 or index.column() == 7 or index.column() == 8:
                    return QtCore.Qt.AlignRight
                    
        return None
    
    def splitthousands(self,s, sep=','):  
        if len(s) <= 3: return s  
        return self.splitthousands(s[:-3], sep) + sep + s[-3:]

    def update_data(self):
        self.emit(QtCore.SIGNAL('layoutChanged()'))
        self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), self.index(0,0), self.index(self.rowCount(),self.columnCount()))
            
    