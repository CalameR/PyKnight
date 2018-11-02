import Instrument
from enum import Enum

class Option(Instrument.Instrument):
    def __init__(self,payoff,exercise):
        self.payoff = payoff
        self.exercise = exercise
    
    def setupArguments(self,arguments):
        self.arguments.payoff = self.payoff
        self.arguments.exercise = self.exercise

class Payoff(object):
    def __init__(self):
        pass
    
class Exercise(object):
    def __init__(self):
        pass

class Type(Enum):
    CALL = 1
    PUT = -1

class Greeks(Instrument.PricingEngine.Results):
    def __init__(self):
        self.delta, self.gamma, self.theta, self.vega, self.rho, self.divRho = 0
    
    def reset(self):
        self.delta, self.gamma, self.theta, self.vega, self.rho, self.divRho = 0
        
class MoreGreeks(Instrument.PricingEngine.Results):
    def __init__(self):
        self.itmCashProba, self.deltaForward, self.elasticity, self.thetaPerDay, self.strikeSensitivity = 0
    
    def reset(self):
        self.itmCashProba, self.deltaForward, self.elasticity, self.thetaPerDay, self.strikeSensitivity = 0

class Arguments(Instrument.PricingEngine.Arguments):
    def __init__(self):
        self.payoff = 0
        self.exercise = 0
    
    def validate(self):
        #MAYBE NOT GOOD CHECK
        if self.payoff == 0:
            print("no payoff given")
        if self.exercise == 0:
            print("no exercise given")

    
    
    
    
    

    
    
    
    
    

