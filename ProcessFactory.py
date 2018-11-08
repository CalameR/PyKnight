import Factory as Base

class ProcessFactory(Base.Factory):
    def __init__(self,name,params,nbFactors,nbAssets):
        Base.Factory.__init__(self,name,params)
        self._nbFactors = nbFactors
        self._nbAssets = nbAssets
        
    def GetNbFactors(self):
        return self._nbFactors
    
    def GetNbAssets(self):
        return self._nbAssets
    
    def GetFactorName(self,pos):
        pass
