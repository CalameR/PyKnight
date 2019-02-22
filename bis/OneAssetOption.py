import Option as Opt
import Engine as Eng

class OneAssetOption(Opt.Option):
    def __init__(self,payoff,exercise):
        Opt.Option.__init__(self,payoff,exercise)
        self._Delta, self._DeltaForward, self._Elasticity = None
        self._Gamma, self._Theta, self._ThetaPerDay = None
        self._Vega, self._Rho, self._DividendRho = None
        self._StrikeSensi, self._ITMCashProba = None
    
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
    
    def _setupExpired(self):
        Opt.Option._setupExpired()
        self._Delta, self._DeltaForward, self._Elasticity = None
        self._Gamma, self._Theta, self._ThetaPerDay = None
        self._Vega, self._Rho, self._DividendRho = None
        self._StrikeSensi, self._ITMCashProba = None
    
    def fetchResults(self,results):
        Opt.Option.fetchResults(results)
        self._Delta = results.Delta
        self._DeltaForward = results.DeltaForward
        self._Elasticity = results.Elasticity
        self._Gamma = results.Gamma
        self._Theta = results.Theta
        self._ThetaPerDay = results.ThetaPerDay
        self._Vega = results.Vega
        self._Rho = results.Rho
        self._DividendRho = results.DividendRho
        self._StrikeSensi = results.StrikeSensi
        self._ITMCashProba = results.ITMCashProba

class Results(Opt.Base.Results,Opt.Greeks,Opt.MoreGreeks):
    def reset(self):
        Opt.Base.Results.reset()
        Opt.Greeks.reset()
        Opt.MoreGreeks.reset()
    
  
        