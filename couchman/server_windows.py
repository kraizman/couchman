from UI.UI_New_Server import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime
import sys
from config import *
from couchdbcurl import Server
import logging
import urlparse

class ServerWindow(QWidget):

    def __init__(self, mainWindow,role,serv_data):
        super(ServerWindow, self).__init__()
        self.ui = Ui_AddServerForm()
        self.ui.setupUi(self)
        self.mainWindow = mainWindow
        self.serv_data = serv_data
        self.connect(self.ui.btn_cancel,QtCore.SIGNAL("clicked()"), self.btn_cancel_react)
        self.connect(self.ui.chb_showpass,QtCore.SIGNAL("toggled(bool)"), self.show_pass_react)
        
        self.connect(self.ui.txt_host,QtCore.SIGNAL("textChanged ( const QString &)"), self.field_changed)
        self.connect(self.ui.spin_port,QtCore.SIGNAL("valueChanged ( const QString &)"), self.field_changed)
        self.connect(self.ui.txt_login,QtCore.SIGNAL("textChanged ( const QString &)"), self.field_changed)
        self.connect(self.ui.txt_password,QtCore.SIGNAL("textChanged ( const QString &)"), self.field_changed)
        self.connect(self.ui.cmb_protocol,QtCore.SIGNAL("activated ( const QString &)"), self.field_changed)
        self.connect(self.ui.grp_login,QtCore.SIGNAL("toggled(bool)"), self.field_changed)
        

        self.connect(self.ui.btn_parse,QtCore.SIGNAL("clicked()"), self.parse_url)
        self.connect(self.ui.btn_test,QtCore.SIGNAL("clicked()"), self.test_url)
        
        if role == 'new':
            self.ui.btn_add.setText("Add")
            self.connect(self.ui.btn_add,QtCore.SIGNAL("clicked()"), self.btn_add_react)
            
            self.ui.txt_url.setText('%s://' % str(self.ui.cmb_protocol.currentText()))
            
        else:
            self.ui.btn_add.setText("Save")
            self.connect(self.ui.btn_add,QtCore.SIGNAL("clicked()"), self.btn_edit_react)
            
            if serv_data['enabled'] == '2':
                self.ui.chb_enabled.setChecked(True)
            else:
                self.ui.chb_enabled.setChecked(False)
            
            self.ui.txt_name.setText(serv_data.get('name'))
            self.ui.txt_proxy.setText(serv_data.get('proxy'))
            
            self.ui.txt_url.setText(self.serv_data.get('url'))
            
            self.parse_url()
            
            if self.serv_data['autoupdate'] == 'None':
                self.ui.group_autoupdate.setChecked(False)
        i=0
        for item in mainWindow.MAIN_DB:
            if self.ui.cmb_group.findText(QString(item['group'])) == -1:
                self.ui.cmb_group.addItems([QString(item['group'])])
                if serv_data and serv_data['url'] == item['url']:
                    self.ui.cmb_group.setCurrentIndex(i)
            i += 1
        
        
        
        
            
    def btn_add_react(self):
        #validating
        
        if self.validate():
        
        
            conflict_server = self.mainWindow.server_model.getServByAddress(str(self.ui.txt_url.text()))
            if conflict_server:
            
                QMessageBox(QMessageBox.Warning, 'Warning', 'Record for address %s already exist!!!' % str(self.ui.txt_url.text()), QtGui.QMessageBox.Ok).exec_()
            
            else: 
                servObj = {}
                servObj["name"] = str(self.ui.txt_name.text())
                servObj["url"] = str(self.ui.txt_url.text())
                servObj["group"] = str(self.ui.cmb_group.currentText())
                servObj["enabled"] = str(self.ui.chb_enabled.checkState())
                servObj["date"] = datetime.now().strftime(DATE_FORMAT)
                servObj["proxy"] = str(self.ui.txt_proxy.text())
                servObj["replications"] = []
                if self.ui.group_autoupdate.isChecked():
                    servObj["autoupdate"] = self.ui.spin_time.value()
                else:
                    servObj["autoupdate"] = 'None'
                self.mainWindow.dump_server_record(servObj)
                self.mainWindow.start_worker('server', servObj)
            
                self.close()
            
    def btn_edit_react(self):
        
        if self.validate():
        
        
            url = self.serv_data["url"]
            
            self.serv_data["name"] = str(self.ui.txt_name.text())
            self.serv_data["url"] = str(self.ui.txt_url.text())
            self.serv_data["group"] = str(self.ui.cmb_group.currentText())
            self.serv_data["enabled"] = str(self.ui.chb_enabled.checkState())
            self.serv_data["date"] = datetime.now().strftime(DATE_FORMAT)
            self.serv_data["proxy"] = str(self.ui.txt_proxy.text())
            if self.ui.group_autoupdate.isChecked():
                self.serv_data["autoupdate"] = self.ui.spin_time.value()
            else:
                self.serv_data["autoupdate"] = 'None'
            
            if self.mainWindow.myJson.save():
                self.mainWindow.server_workers[self.serv_data["url"]] = self.mainWindow.server_workers[url]
                obj = self.mainWindow.server_workers[self.serv_data["url"]]
                pipe = obj['pipe']
                pipe.send({"command":'update_data', "data":self.serv_data})
                self.mainWindow.server_model.update_data()
                self.close()
            else:
                logging.debug('save server changes fail')
            
    def btn_cancel_react(self):
        self.close()
        
    def show_pass_react(self,state):
        if state:
            self.ui.txt_password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.txt_password.setEchoMode(QLineEdit.Password)
    
    def field_changed(self,text):
        scheme = str(self.ui.cmb_protocol.currentText())
        
        login = str(self.ui.txt_login.text())
        password = str(self.ui.txt_password.text())
        
        host = str(self.ui.txt_host.text())
        port = str(self.ui.spin_port.text())
        
        url = '%s://' % scheme
        if self.ui.grp_login.isChecked():
            url += '%s:%s@' % (login, password)
        url += host
        if len(port) > 0 and len(host) > 0:
            url += ':%s' % port
        
        self.ui.txt_url.setText(url)
        
    def parse_url(self):
        
        url = str(self.ui.txt_url.text())
        url_parsed = urlparse.urlparse(url)
        
        self.ui.txt_host.setText(url_parsed.hostname or "")
        self.ui.spin_port.setValue(url_parsed.port or 5984)
        if url_parsed.username and len(url_parsed.username) > 0:
            self.ui.grp_login.setChecked(True)
            self.ui.txt_login.setText(url_parsed.username or "")
            self.ui.txt_password.setText(url_parsed.password or "")
        else:
            self.ui.grp_login.setChecked(False)
            self.ui.txt_login.setText('')
            self.ui.txt_password.setText('')       
        if url_parsed.scheme == 'http':
            self.ui.cmb_protocol.setCurrentIndex(0)
        else:
            self.ui.cmb_protocol.setCurrentIndex(1) 
    
    def test_url(self):
        logging.debug("ServerWindow: test url %s" % str(self.ui.txt_url.text()))
        db_server = Server(str(self.ui.txt_url.text()))
        try:
            version = db_server.version
            server_enabled = True;
        except:
            server_enabled = False;
        
        if server_enabled:
            QMessageBox(QMessageBox.Information, 'Test Result', 'Server with couchDB does exist in %s.\nDB version: %s' % (str(self.ui.txt_url.text()), version), QtGui.QMessageBox.Ok).exec_()
        else:
            QMessageBox(QMessageBox.Warning, 'Test Result', 'Server with couchDB does not exist in %s' % str(self.ui.txt_url.text()), QtGui.QMessageBox.Ok).exec_()
    
    
    def validate(self):
        if str(self.ui.txt_name.text()) == "":
            QMessageBox(QMessageBox.Critical, 'Error', 'Name field are required', QtGui.QMessageBox.Ok).exec_()
            return False
        
        if str(self.ui.txt_host.text()) == "":
            QMessageBox(QMessageBox.Critical, 'Error', 'Host field are required', QtGui.QMessageBox.Ok).exec_()
            return False
        
        if str(self.ui.txt_url.text()) == "":
            QMessageBox(QMessageBox.Critical, 'Error', 'Url field are required', QtGui.QMessageBox.Ok).exec_()
            return False
        
        if self.ui.group_proxy.isChecked() and str(self.ui.txt_proxy.text()) == "":
            QMessageBox(QMessageBox.Critical, 'Error', 'Since proxy are enabled the Proxy field are required', QtGui.QMessageBox.Ok).exec_()
            return False
        
        if self.ui.grp_login.isChecked() and (str(self.ui.txt_login.text()) == "" or str(self.ui.txt_password.text()) == ""):
            QMessageBox(QMessageBox.Critical, 'Error', 'Since authentication are enabled the Login and password fields are required', QtGui.QMessageBox.Ok).exec_()
            return False        
        
        return True                            
    
    def closeEvent(self,event):
        try:
            self.mainWindow.server_windows.remove(self)
        except:
            #print "error removing from server windows list"
             logging.debug('ReplicationWindow: error removing from server windows list')
        
