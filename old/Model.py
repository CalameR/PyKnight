from Securities import Securities as Secu
from NumericalMethod import NumericalMethod as NumMeth

class Model(object):
    
    def MsgParams(BoolParams=True):
        if not(BoolParams):
            print("Params are not correct")
        else:
            print("Params are correct")
        return
    
    def __init__(self,ModelName,ModelParams=()):
        self.Name = ModelName
        self.Params = ModelParams
    
    def __str__(self):
        return "{0} with params {1}".format(self.Name,self.Params)
    
    def GetParamPos(self,ParamName):
        print("GetParamPos not implemented for {0}".format(self.Name))
        return 0
    
    def SetParam(self,ParamName,ParamValue):
        self.Params[self.GetParamPos(ParamName)] = ParamValue
    
    def SetAllParams(self,ModelParams):
        self.Params = ModelParams
        
    def TestParams(self,ModelParams):
        return self.MsgParams()

    def SimulatePath(self,S0,T,nbstep=1):
        print("{0} simulate path function with is not implemented".format(self.Name))
        return 0

    def Price(self,S0,T,MySecurities,MyNumericalMethod):
        if not(isinstance(MySecurities,Secu)):
            print("Security parameter is not correct")
        
            