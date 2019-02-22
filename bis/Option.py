import Instrument as Base
import Engine as Engine

class Option(Base.Instrument):
    def __init__(self,payoff,exercise):
        Base.Instrument.__init__(self)
        self._Payoff = payoff
        self._Exercise = exercise
        
    def Payoff(self):
        return self._Payoff
    
    def Exercise(self):
        return self._Exercise
    
    def setupArguments(self,arguments):
        if (arguments.Payoff is not None and arguments.Exercise is None):
            self._Payoff = arguments.Payoff 
            self._Exercise = arguments.Exercise
        else:
            raise Exception('Payoff or Exercise not setup')

class Arguments(Engine.Arguments):
    def __init__(self):
        self.Payoff = None
        self.Exercise = None
    
    def validate(self):
        if (self.Payoff is None or self.Exercise is None):
            return False
        else:
            return True
        
class Greeks(Engine.Results):
    def __init__(self):
        self.Delta, self.Gamma, self.Theta = None
        self.Vega, self.Rho, self.DivRho = None
    
    def reset(self):
        self.Delta, self.Gamma, self.Theta = None
        self.Vega, self.Rho, self.DivRho = None

class MoreGreeks(Engine.Results):
    def __init__(self):
        self._DeltaForward, self._Elasticity = None
        self._ThetaPerDay = None
        self._StrikeSensi, self._ITMCashProba = None
    
    def reset(self):
        self._DeltaForward, self._Elasticity = None
        self._ThetaPerDay = None
        self._StrikeSensi, self._ITMCashProba = None
        
    

        
    

