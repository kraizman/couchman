import multiprocessing
from time import sleep,time
from datetime import datetime 

import logging
from config import DATETIME_FMT
from couchdbcurl import Server
import sys

class ServerWorker(multiprocessing.Process):
    
    def __init__(self,pipe,server):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.server = server
        self.flag = True
        self.address = server['url']
        self.db_server = Server(self.address)
        try:
            self.update_period = float(server.get('autoupdate'))
        except:
            self.update_period = None
        
        self.last_update = time()
    
    def update(self):
        #logging.debug("worker: update command for %s" % self.address)
        try:
            tasks = self.db_server.tasks()
            ver = "ver. %s" % self.db_server.version
            server_enabled = True;
        except:
            tasks = None
            ver = "-"
            server_enabled = False;
            
        self.last_update = time()
   
        
        self.pipe.send({"command": "update_server", 
                        "url": self.server['url'],
                        "data":{"enabled": server_enabled,
                                "updated": datetime.now(),
                                "version": ver,
                                "tasks": tasks}})
        
    def run(self):
        while self.flag:
            while self.pipe.poll():
                data = self.pipe.recv()

                if "command" in data:
                    command = data['command']
                    if command == "update_server":

                        
                        self.update()
                    elif command == "update_data":
                        self.server = data['data']
                        self.address = self.server['url']
                        self.db_server = Server(self.address)
                        try:
                            self.update_period = float(self.server.get('autoupdate'))
                        except:
                            self.update_period = None
                        
                    elif command == "shutdown":
                        logging.debug("worker: shutdown command for %s" % self.address)
                        self.flag = False
                        
                        return
                
            sleep(0.05)
            
            if self.update_period and time() > self.last_update + self.update_period:
                self.update()
                
                

class ReplicationWorker(multiprocessing.Process):
    
    def __init__(self,pipe,data):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.source = data.get('source')
        self.target = data.get('target')
        self.filter = data.get('filter',"")

        self.query = data.get('query', "")
        self.continuous = data.get('continuous')
        self.proxy = data.get('proxy', "")
        self.flag = True
        server = data.get('server')
        self.server_address = server.get('url')
        self.db_server = Server(self.server_address)
        self.flag = True
        
        
    def run(self):

        logging.debug("replication worker: run replication worker for %s" % self.server_address)
        while self.flag:
            while self.pipe.poll():
                data = self.pipe.recv()
                if "command" in data:
                    command = data['command']
                    if command == "start_replication":
                        error = None
                        args = {}
                        if self.proxy:
                            args['proxy'] = self.proxy
                        if self.filter:
                            args['filter'] = self.filter
                            if self.query:
                                args['query_params'] = self.query
                        if self.continuous:
                            print "replicate url: source: %s, target: %s, continuous: true, args: %s" % (self.source, self.target, args,)
                            try:
                                self.db_server.replicate(self.source, self.target, continuous=True, **args)
                            except:
                                logging.debug("worker: replication creation error for %s" % self.server_address)
                                error = sys.exc_info()[1]
                        else:
                            print "replicate url: source: %s, target: %s, continuous: false, args: %s" % (self.source, self.target, args,)
                            try:
                                self.db_server.replicate(self.source, self.target, **args)
                            except:
                                logging.debug("worker: replication creation error for %s" % self.server_address)
                                error = sys.exc_info()[1]
                            
                        if error:
                            self.pipe.send({
                                "command":'error',
                                "url": self.server_address,
                                "error": error,
                                "source": self.source,
                                "target": self.target,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        else:
                            self.pipe.send({
                                "command": "done",
                                "message": "Replication start successfully. Details:",
                                "url": self.server_address,
                                "source": self.source,
                                "target": self.target,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        self.flag = False
                    elif command == "stop_replication":
                        error = None
                        try:
                            self.db_server.replicate(self.source, self.target,continuous=True, cancel = True)
                            self.continuous = True
                        except:
                            try:
                                self.db_server.replicate(self.source, self.target, cancel = True)
                                self.continuous = False
                            except:
                                error = sys.exc_info()[1]
                        if error:
                            self.pipe.send({
                                "command": 'error',
                                "url": self.server_address,
                                "error": error,
                                "source": self.source,
                                "target": self.source,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        else:
                            self.pipe.send({
                                "command": "done",
                                "message": "Replication stop successfully. Details:",
                                "url": self.server_address,
                                "source": self.source,
                                "target": self.target,
                                "filter": self.filter,
                                "query": self.query,
                                "proxy": self.proxy,
                                "continuous": self.continuous,
                            })
                        self.flag = False       
                               
                    if command == "shutdown":
                        logging.debug("worker: shutdown command for %s" % self.server_address)
                        self.flag = False
                        
                        return      
            sleep(0.5)
            
class ViewWorker(multiprocessing.Process):
    
    def __init__(self,pipe,url,command,db_name,params):
        multiprocessing.Process.__init__(self)
        self.pipe = pipe
        self.params = params
        self.command = command
        self.address = url
        self.db_server = Server(self.address)
        self.db = self.db_server[db_name]
        
    
    def send_error(self, error):
        self.pipe.send({"command":self.command,
                        "url": self.address,
                        "updated": datetime.now(),
                        "db_name": self.db.name,
                        "params": self.params,
                        "error": error,
                        })
    
    def send_result(self, result):
        self.pipe.send({"command":self.command,
                        "url": self.address,
                        "updated": datetime.now(),
                        "db_name": self.db.name,
                        "params": self.params,
                        "result": result,
                        })
    
    def run(self):
        if self.command == "get_info":
            try:
                result = self.db.design_info(self.params["row_id"])
                self.send_result(result)
            except:
                self.send_error(sys.exc_info()[1])
        elif self.command == "ping":
            try:
                doc_name = self.db['_design/' + self.params["view_name"]].views.keys()[0]
                self.db.view(self.params["view_name"] + '/' + doc_name, limit = 0).rows
                self.send_result("")
            except:
                self.send_error(sys.exc_info()[1])
            


            
        
            
        