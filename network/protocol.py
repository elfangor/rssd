import pickle

from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Protocol(LineReceiver):
    def __init__(self,deamon):
        self.auth= False
        self.deamon = deamon

    def lineReceived(self, line):
        try:
            data=pickle.loads(line)
            if data["cmd"]=="login":
                self.login(data["param"])
                self.sendLine("Auth status:"+str(self.auth))
            else:
                func=getattr(self.deamon,data["cmd"]) 
                if "param" in data:
                   func(data["param"])
                else:
                    func() 
        except Exception, e:
            print e

    def login(self, param):
        if param["login"]== "test" and param["pass"]=="ok":
            print "user auth"
            self.auth= True
