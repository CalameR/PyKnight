import Option as Opt
import Factory as Fact

class OneAssetOption(Opt.Option):
    def __init__(self,payoff,exercise):
        Opt.Option.__init__(self,payoff,exercise)
        self._Delta, self._DeltaForward, self._Elasticity = 0
        self._Gamma, self._Theta, self._ThetaPerDay = 0
        self._Vega, self._Rho, self._DividendRho = 0
        self._StrikeSensi, self._ITMCashProba = 0
    
    def Delta(self):
        self._calculate()
        return self._Delta
    
    def DeltaForward(self):
        self._calculate()
        return self._DeltaForward
    
    def Elasticity(self):
        self._calculate()
        return self._Elasticity
    
    def Gamma(self):
        self._calculate()
        return self._Gamma
    
    def Theta(self):
        self._calculate()
        return self._Theta
    
    def ThetaPerDay(self):
        self._calculate()
        return self._ThetaPerDay
    
    def Vega(self):
        self._calculate()
        return self._Vega
    
    def Rho(self):
        self._calculate()
        return self._Rho
    
    def DividendRho(self):
        self._calculate()
        return self._DividendRho
    
    def StrikeSensi(self):
        self._calculate()
        return self._StrikeSensi
    
    def ITMCashProba(self):
        self._calculate()
        return self._ITMCashProba
    
  
        