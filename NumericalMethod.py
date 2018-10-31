class NumericalMethod(object):
    def __init__(self,MethodName,MethodParams=()):
        self.Name = MethodName
        self.Params = MethodParams
        
    def __str__(self):
        return "{0} with params {1}".format(self.Name,self.Params)

    def GetParamPos(self,ParamName):
        print("GetParamPos not implemented for {0}".format(self.Name))
        return 0

class PDE(NumericalMethod):
    def __init__(self,MethodName,MethodParams=(50,100)):
        NumericalMethod.__init__("{0}_{1}".format("PDE",MethodName),MethodParams)
    
    def GetParamPos(self,ParamName):
        if (ParamName == "t" or "T" or "time"):
            return 0
        elif (ParamName == "x" or "X" or "x1" or "X1"):
            return 1
        elif (ParamName == "y" or "Y" or "x2" or "X2"):
            return 2
        elif (ParamName == "z" or "z" or "x3" or "X3"):
            return 3

class MC(NumericalMethod):
    def __init__(self,MethodName,MethodParams=(10000,0.1)):
        NumericalMethod.__init__("{0}_{1}".format("MC",MethodName),MethodParams)
    
    def GetParamPos(self,ParamName):
        if (ParamName == "n" or "N" or "NBRAND" or "nbrand"):
            return 0
        elif (ParamName == "var" or "VAR"):
            return 1
    
    def ComputeMean(self,FuncSimulate,ParamsSimu,FuncEval,ParamsEval):
        Sum = 0
        n = self.GetParamPos("n")
        for i in range(0,n):
            S = FuncSimulate(ParamsSimu)
            Sum = Sum + FuncEval(S,ParamsEval)
        return Sum/n
    
            