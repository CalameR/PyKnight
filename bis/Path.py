import Factory as Base
import QuantLib as ql
import RandomSequenceGenerator as Rand
from datetime import datetime

class PathGenerator(Base.Factory):
    def __init__(self,name,pathProcess,randomSequenceGenerator):
        Base.Factory.__init__(self,name)
        self._PathProcess = pathProcess
        self._RandomSequenceGenerator = randomSequenceGenerator
        
    def GetNbAssets(self):
        return self._PathProcess.GetNbAssets()
    
    def GetNbFactors(self):
        return self._PathProcess.GetNbFactors()
    
    def GetFactorName(self,pos):
        return self._PathProcess.GetFactorName(pos)
    
class GaussianPathGenerator(PathGenerator):
    def __init__(self,name,pathProcess,length,timestep,brownianBridge=False):
        gaussianRandomSequenceGenerator = Rand.GaussianRandomSequenceGenerator(timestep)
        PathGenerator.__init__(self,name,pathProcess,gaussianRandomSequenceGenerator)
        self._Length = length
        self._Timestep = timestep
        self._BrownianBridge = brownianBridge
        self._QLBuild()
    
    def SetBrownianBridge(self,Yes=True):
        self._BrownianBridge = Yes
        self._QLBuild()
    
    def _QLBuild(self):
        self._QLFactory = ql.GaussianPathGenerator(self._PathProcess(),
                                        self._Length,
                                        self._Timestep,
                                        self._RandomSequenceGenerator(),
                                        self._BrownianBridge)
        self._Timestamp = str(datetime.now())

class GaussianMultiPathGenerator(Base.Factory):
    def __init__(self,name,pathProcess,timeGrid,brownianBridge=False):
        dimension = pathProcess.GetNbFactors()*(len(timeGrid)-1)
        gaussianRandomSequenceGenerator = Rand.GaussianRandomSequenceGenerator(dimension)
        PathGenerator.__init__(self,name,pathProcess,gaussianRandomSequenceGenerator)
        self._TimeGrid = timeGrid
        self._BrownianBridge = brownianBridge
        self._QLBuild()
    
    def SetBrownianBridge(self,Yes=True):
        self._BrownianBridge = Yes
        self._QLBuild()
    
    def _QLBuild(self):
        self._QLFactory = ql.GaussianMultiPathGenerator(self._PathProcess(),
                                             self._TimeGrid,
                                             self._RandomSequenceGenerator(),
                                             self._BrownianBridge)
        self._Timestamp = str(datetime.now())