import HestonFactory as Heston
import BlackScholesFactory as BS
import matplotlib.pyplot as plt
import QuantLib as ql
import Utils

if __name__=="__main__":
    
    # GLOBAL CONFIG #
    AsOfDate = ql.Date(15,10,2018)
    DayCount = ql.Actual365Fixed()
    Calendar = ql.UnitedStates()
    GlobalData = {'AsOfDate':AsOfDate,'DayCount':DayCount,'Calendar':Calendar}
    
    # INSTRUMENT1D CONFIG #
    MaturityDate = ql.Date(15,10,2021)
    
    strike = 100
    option_type = ql.Option.Call
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    exercise = ql.EuropeanExercise(MaturityDate)
    EuropeanOption = ql.VanillaOption(payoff, exercise)

    r=0.01
    q=0.005
    s0=100
    v0=0.01
    kappa=0.5
    theta=0.01
    sigma=0.05
    rho=-0.5
    relTolerance=0.01
    maxEval=10000
    r_simple_quote = ql.SimpleQuote(r)
    rate_curve_handle = ql.YieldTermStructureHandle(
                ql.FlatForward(AsOfDate,ql.QuoteHandle(r_simple_quote),DayCount))
    div_curve_handle = ql.YieldTermStructureHandle(
                ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(q)),DayCount))
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(s0))
    HestonProcess = ql.HestonProcess(rate_curve_handle,div_curve_handle,spot_handle,
                                v0,kappa,theta,
                                sigma,rho)
    HestonModel = ql.HestonModel(HestonProcess)
    HestonModel2 = HestonModel
    HestonEngine = ql.AnalyticHestonEngine(HestonModel,relTolerance,maxEval)
    EuropeanOption.setPricingEngine(HestonEngine)
    print(EuropeanOption.NPV())
    
    print(HestonProcess.factors())
    
    print(payoff(102))
    
    r = 0.02
    r_simple_quote.setValue(r)
    
    print(EuropeanOption.NPV())
    
    v0 = 0.02
    params = (theta,kappa,sigma,rho,v0)
    HestonModel.setParams(params)
    
    print(EuropeanOption.NPV())
    
    
    # PRICING ENGINE CONFIG #
    #HestonEngine = Heston.HestonAnalyticEngineFactory(r=0.01,q=0.005,s0=100,v0=0.01,kappa=0.5,theta=0.01,sigma=0.05,rho=-0.5,relTolerance=0.01,maxEval=10000)
    
    # HEDGING ENGINE CONFIG #
    BlackScholesEngine = BS.BlackScholesAnalyticEngineFactory(r=0.01,q=0.005,s0=100,sigma=0.1)
    
    # PATH CONFIG # 
    timestep = int((MaturityDate-AsOfDate)/4)
    length = DayCount.yearFraction(AsOfDate,MaturityDate)
    timeGrid = [n/timestep*length for n in range(timestep+1)]
    brownianBridge = False
    HestonPathGenerator = Heston.HestonPathGenerator(r=0.1,q=0.005,s0=100,v0=0.01,kappa=0.5,theta=0.01,sigma=0.05,rho=-0.5,timeGrid=timeGrid,brownianBridge=brownianBridge)
    
    #time, paths = Utils.BacktestDeltaHedge1DWithRateDivConstant(GlobalData,HestonPathGenerator,EuropeanOption,
    #                                                      HestonEngine,BlackScholesEngine)
    
    #plt.plot(time, paths[0, :], label='Option Value', lw=1, alpha=1)
    #plt.plot(time, paths[1, :], label='Portfolio Value', lw=1, alpha=1)
    #plt.title("Backtest of European Option - Black Scholes Hedge in Heston World")
    #plt.legend()
    #plt.show()
    
    #NumPaths = 10
    #time, paths = Utils.GeneratePaths(NumPaths,GlobalData,HestonPathGenerator)
    #for i in range(NumPaths):
    #    plt.plot(time, paths[i, :], lw=1, alpha=1)
    #plt.title("Heston Simulation")
    #plt.show()
    
    
    
    