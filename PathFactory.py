import Factory as Base
import QuantLib as ql
import RandomSequenceGeneratorFactory as RandSeqGen

#TO BE MERGED INTO ONE CLASS

class GaussianPathGeneratorFactory(Base.Factory):
    def __init__(self,name,pathProcess,length,timestep,brownianBridge=False):
        params = {'length':length,'timestep':timestep,'brownianBridge':brownianBridge}
        Base.Factory.__init__(self,name,params)
        self._PathProcess = pathProcess
        self._GaussianRandomSequenceGenerator = RandSeqGen.GaussianRandomSequenceGeneratorFactory(timestep)
    
    def GetNbAssets(self):
        return 1
    
    def GetNbFactors(self):
        return 1
    
    def GetFactorName(self,pos):
        return self._PathProcess.GetFactorName(pos)
    
    def GetParams(self):
        params = dict(list(self._PathProcess.GetParams().items()) +
                      list(self._GaussianRandomSequenceGenerator.GetParams().items()) + 
                      list(Base.Factory.GetParams(self).items()))
        return params
    
    def GetParamNames(self):
        names = self._PathProcess.GetParamNames()
        names.extend(self._GaussianRandomSequenceGenerator.GetParamNames())
        names.extend(Base.Factory.GetParamNames(self))
        return names
    
    def _QLBuild(self):
        self._QLFactory = ql.GaussianPathGenerator(self._PathProcess(),
                                        self._params.get('length'),
                                        self._params.get('timestep'),
                                        self._GaussianRandomSequenceGenerator(),
                                        self._params.get('brownianBridge'))    
    
    def Update(self,**data):
        self._PathProcess.Update(**data)
        dimension = data.get('timestep',self._params.get('timestep'))
        data['dimension']=dimension
        self._GaussianRandomSequenceGenerator.Update(**data)
        Base.Factory.Update(self,**data)
    
    def _UpdateParams(self,**data):
        Base.Factory._SetParams(self,**data)
    
    def _UpdateData(self,**data):
        return 0

class GaussianMultiPathGeneratorFactory(Base.Factory):
    def __init__(self,name,pathProcess,timeGrid,brownianBridge=False):
        params = {'timeGrid':timeGrid,'brownianBridge':brownianBridge}
        Base.Factory.__init__(self,name,params)
        self._PathProcess = pathProcess
        dimension = pathProcess.GetNbFactors()*(len(timeGrid)-1)
        self._GaussianRandomSequenceGenerator = RandSeqGen.GaussianRandomSequenceGeneratorFactory(dimension)
    
    def GetNbFactors(self):
        return self._PathProcess.GetNbFactors()
    
    def GetNbAssets(self):
        return self._PathProcess.GetNbAssets()
    
    def GetFactorName(self,pos):
        return self._PathProcess.GetFactorName(pos)
    
    def GetParams(self):
        params = dict(list(self._PathProcess.GetParams().items()) +
                      list(self._GaussianRandomSequenceGenerator.GetParams().items()) + 
                      list(Base.Factory.GetParams(self).items()))
        return params
    
    def GetParamNames(self):
        names = self._PathProcess.GetParamNames()
        names.extend(self._GaussianRandomSequenceGenerator.GetParamNames())
        names.extend(Base.Factory.GetParamNames(self))
        return names
    
    def _QLBuild(self):
        self._QLFactory = ql.GaussianMultiPathGenerator(self._PathProcess(),
                                             self._params.get('timeGrid'),
                                             self._GaussianRandomSequenceGenerator(),
                                             self._params.get('brownianBridge'))    
    
    def Update(self,**data):
        self._PathProcess.Update(**data)
        dimension = self._PathProcess.GetNbFactors()*(len(data.get('timeGrid',self._params.get('timeGrid')))-1)
        data['dimension']=dimension
        self._GaussianRandomSequenceGenerator.Update(**data)
        Base.Factory.Update(self,**data)
        
    def _UpdateParams(self,**data):
        Base.Factory._SetParams(self,**data)
    
    def _UpdateData(self,**data):
        return 0