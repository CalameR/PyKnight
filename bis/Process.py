import Factory as Base

class Process(Base.CalibFactory):
    def __init__(self,name,nbFactors,nbAssets):
        Base.Factory.__init__(self,name)
        self._NbFactors = nbFactors
        self._NbAssets = nbAssets
        
    def GetNbFactors(self):
        return self._NbFactors
    
    def GetNbAssets(self):
        return self._NbAssets
