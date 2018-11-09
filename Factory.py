from datetime import datetime

class Factory(object):
    def __init__(self,name,params={}):
        self._name = name + "_" + str(datetime.now())
        self._params = params
    
    def GetName(self):
        return self._name
    
    def GetParams(self):
        return self._params
    
    def GetParamNames(self):
        return list(self._params.keys())
    
    def SetParams(self,**params):
        for (key,val) in self._params.items():
            self._params[key] = params.get(key,val)
    
    def UpdateParams(self,**data):
        pass
    
    def __call__(self,**data):
        pass

