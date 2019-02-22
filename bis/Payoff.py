import Factory as Base
import QuantLib as ql
#import numpy as np
from datetime import datetime

# FOR ANY FINAL CHILD PAYOFF CLASS IMPLEMENTED IN QL, 
# THE __init__ CALL MUST CONTAIN self._QLBuild() AT THE END !

class Payoff(Base.Factory):
    def __init__(self,name):
        Base.Factory.__init__(self,name)
    
    def __call__(self,data=None):
        if data is not None:
            return self._QLFactory(data)
        else:
            return self._QLFactory

class TypePayoff(Payoff):
    def __init__(self,name,option_type):
        Payoff.__init__(self,name)
        self._OptionType = option_type
    
    def SetOptionType(self,option_type):
        self._OptionType = option_type
        self._QLBuild()
        
    def GetOptionType(self):
        return self._OptionType
    
class FloatingTypePayoff(TypePayoff):
    def __init__(self,name,option_type):
        TypePayoff.__init__(self,name,option_type)

class StrikedTypePayoff(TypePayoff):
    def __init__(self,name,strike,option_type):
        TypePayoff.__init__(self,name,option_type)
        self._Strike = strike
        
    def SetStrike(self,strike):
        self._Strike = strike
        self._QLBuild()
    
    def GetStrike(self):
        return self._Strike
        
class CashPayoff(Payoff):
    def __init__(self,name,cash):
        Payoff.__init__(self,name)
        self._Cash = cash
    
    def SetCash(self,cash):
        self._Cash = cash
        self._QLBuild()
    
    def GetCash(self):
        return self._Cash

class PlainVanillaPayoff(StrikedTypePayoff):
    def __init__(self,strike,option_type):
        StrikedTypePayoff.__init__(self,'PlainVanillaPayoff',strike,option_type)
        self._QLBuild()
    
    def _QLBuild(self):
        self._QLPayoff = ql.PlainVanillaPayoff(self._OptionType, self._Strike)
        self._Timestamp = str(datetime.now())
    
class DigitalPayoff(StrikedTypePayoff,CashPayoff):
    def __init__(self,strike,option_type,cash):
        StrikedTypePayoff.__init__(self,'DigitalPayoff',strike,option_type)
        CashPayoff.__init__(self,'DigitalPayoff',cash)
        self._QLBuild()
    
    def _QLBuild(self):
        self._QLPayoff = ql.CashOrNothingPayoff(self._OptionType,self._Strike,self._Cash)
        self._Timestamp = str(datetime.now())
    
    
    
    
    
    
    
    
    
    
    
    
    