from datetime import datetime
import Factory as Base
import QuantLib as ql

class RandomSequenceGenerator(Base.Factory):
    def __init__(self,name,dimension):
        Base.Factory.__init__(self,name)
        self._Dimension = dimension
        
    def GetDimension(self):
        return self._Dimension
    
    def SetDimension(self,dimension):
        self._Dimension = dimension
        self._QLBuild()
        self._Timestamp = str(datetime.now())

class UniformRandomSequenceGenerator(RandomSequenceGenerator):
    def __init__(self,dimension):
        RandomSequenceGenerator.__init__(self,"UniformRandomSequenceGenerator",dimension)
    
    def _QLBuild(self):
        self._QLFactory = ql.UniformRandomSequenceGenerator(self._Dimension,ql.UniformRandomGenerator())

class GaussianRandomSequenceGenerator(RandomSequenceGenerator):
    def __init__(self,dimension):
        RandomSequenceGenerator.__init__(self,"GaussianRandomSequenceGenerator",dimension)
        self._UniformRandomSequenceGenerator = UniformRandomSequenceGenerator(dimension)
    
    def _QLBuild(self):
        self._QLFactory = ql.GaussianRandomSequenceGenerator(self._UniformRandomSequenceGenerator())