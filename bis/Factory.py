from datetime import datetime

class Factory(object):
    def __init__(self,name):
        self._Name = name
        self._Timestamp = str(datetime.now())
        self._GlobalData = 0
        self._QLFactory = 0
        self._UpToDate = False
            
    def GetName(self):
        return self._name
    
    def Update
    
    def Update(self,**data):
        self._UpdateGlobalData(**data)
        self._UpdateParams(**data)
        self._timestamp = str(datetime.now())
        self._QLBuild()
        self._UpToDate = True
    
    def __call__(self):
        if self._UpToDate:
            self._UpToDate = False
            return self._QLFactory
        else:
            print(self._name + ' Update method must be called before')
            return 0
            
    def _UpdateGlobalData(self,**data):
        pass
    
    def _UpdateParams(self,**data):
        pass 

    def _QLBuild(self):
        pass
