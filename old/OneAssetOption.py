import Option

class OneAssetOption(Option.Option):
    def __init__(self,payoff,exercise):
        Option.Option.__init__(payoff,exercise)
        self.delta, self.gamma, self.theta, self.vega, self.rho, self.divRho = 0
        self.itmCashProba, self.deltaForward, self.elasticity, self.thetaPerDay, self.strikeSensitivity = 0
    
    def isExpired(self):
        #TO BE IMPLEMENTED
        #C++ : return detail::simple_event(exercise_->lastDate()).hasOccured();
        return False
    
    def fDelta(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.delta
    
    def fGamma(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.gamma
    
    def fTheta(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.theta
    
    def fVega(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.vega
    
    def fRho(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.rho
    
    def fDivRho(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.rho
    
    def fITMCashProba(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.itmCashProba
    
    def fDeltaForward(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.deltaForward
    
    def fElasticity(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.elasticity
    
    def fThetaPerDay(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.thetaPerDay
    
    def fStrikeSensitivity(self):
        self.calculate()
        #CHECK NOT DONE
        #if (xxx != Null<Real>):
        return self.fStrikeSensitivity
    
    def setupExpired(self):
        Option.Option.setupExpired()
        self.delta, self.gamma, self.theta, self.vega, self.rho, self.divRho = 0
        self.itmCashProba, self.deltaForward, self.elasticity, self.thetaPerDay, self.strikeSensitivity = 0
    
    def fetchResults(self,results):
        Option.Option.fetchResults(results)
        #NO CHECK IF RESULTS IS OK
        self.delta, self.gamma = results.delta, results.gamma
        self.theta, self.vega = results.theta, results.vega
        self.rho, self.divRho = results.rho, results.divRho
        self.itmCashProba, self.deltaForward = results.itmCashProba, results.deltaForward
        self.elasticity, self.thetaPerDay = results.elasticity, results.thetaPerDay
        self.strikeSensitivity = results.strikeSensitivity

class Results(Option.Instrument.Results,Option.Greeks,Option.MoreGreeks):
    def __init__(self):
        Option.Instrument.Results.__init__(self)
        Option.Greeks.__init__(self)
        Option.MoreGreeks.__init__(self)
        
    def reset(self):
        Option.Instrument.Results.reset(self)
        Option.Greeks.reset(self)
        Option.MoreGreeks.reset(self)

class Engine(Option.Instrument.PricingEngine):
    def __init__(self,arguments,results):
        Option.Instrument.PricingEngine.PricingEngine.__init__(self,arguments,results)
        
    