import Factory as Base

class EngineFactory(Base.Factory):
    def __init__(self,name,params):
        Base.Factory.__init__(self,name,params)
        self._Arguments = 0
        self._Results = 0
    
    def calculate(self):
        pass
    
    def getArguments(self):
        return self._Arguments
    
    def getResults(self):
        return self._Results
    
    def reset(self):
        self._Results.reset()
        
class Results(object):
    def __init__(self)