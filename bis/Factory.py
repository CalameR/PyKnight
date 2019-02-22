from datetime import datetime

class Factory(object):
    def __init__(self,name):
        self._Name = name
        self._Timestamp = str(datetime.now())
        self._QLFactory = None
            
    def GetName(self):
        return self._Name + "_" + self._Timestamp
    
    def __call__(self):
        return self._QLFactory
    
    def _QLBuild(self):
        pass
    
class CalibFactory(Factory):
    def __init__(self,name):
        Factory.__init__(self,name)
        self._UpToDate = False
        
    def Update(self,data):
        self._UpdateParams(data)
        self._Timestamp = str(datetime.now())
        self._QLBuild()
        self._UpToDate = True
        
    def __call__(self):
        if self._UpToDate:
            self._UpToDate = False
            return self._QLFactory
        else:
            print(self._name + ' Update method must be called before')
            return None
    
    def _UpdateParams(self,data):
        pass
    
    def SetContext(self,context):
        self._Context = context
        

        
