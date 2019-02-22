import Factory as Base

class Engine(Base.CalibFactory):
    def __init__(self,name):
        Base.Factory.__init__(self,name)
        self._Arguments = None
        self._Results = None
    
    def calculate(self):
        pass
    
    def getArguments(self):
        return self._Arguments
    
    def getResults(self):
        return self._Results
    
    def reset(self):
        self._Results.reset()
        
class Results(object):
    def reset(self):
        pass
    
class Arguments(object):
    def validate(self):
        pass
        