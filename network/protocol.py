import json

from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Protocol(LineReceiver):
    def __init__(self,deamon):
        self.auth= False
        self.deamon = deamon

    def lineReceived(self, line):
        try:
            data=json.loads(line)
            if data["cmd"]=="login":
                self.login(data["param"])
                self.sendLine("Auth status:"+str(self.auth))
            else:
                func=getattr(self.deamon,data["cmd"]) 
                if "param" in data:
                   ret = func(data["param"])
                else:
                   ret = func() 
                try:
                    for i in ret:
                        self.sendLine(json.dumps(i))
                except TypeError, te:
                    if ret:
                        self.sendLine(json.dumps(ret))
        except Exception, e:
            print e

    def login(self, param):
        if param["login"]== "test" and param["pass"]=="ok":
            print "user auth"
            self.auth= True
