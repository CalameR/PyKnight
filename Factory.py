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
        return self._params.keys()
    
    def SetParams(self,**params):
        for (key,val) in self._params.items():
            self._params[key] = params.get(key,val)
    
    def Make(self,**data):
        pass
    
    def UpdateParams(self,**data):
        pass

