from datetime import datetime

class Factory(object):
    def __init__(self,name,params={}):
        self._name = name
        self._timestamp = str(datetime.now())
        self._params = params
        self._Data = 0
        self._QLFactory = 0
        self._UpToDate = False
   
    # Called by _UpdateParams method when there is no need to do computation
    # on the dict data given in input
    def _SetParams(self,**params):
        for (key,val) in self._params.items():
            self._params[key] = params.get(key,val)
            
    def GetName(self):
        return self._name
    
    # TO BE DELETED
    def GetParams(self):
        return self._params
    
    def GetParamNames(self):
        return list(self._params.keys())
    
    def Update(self,**data):
        self._UpdateData(**data)
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
            
    def _UpdateData(self,**data):
        pass
    
    def _UpdateParams(self,**data):
        pass 

    def _QLBuild(self):
        pass
