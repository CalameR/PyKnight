import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt

def error_msg_kwargs(key,fName):
    return "{0} parameter: issue with {1} function".format(key,fName)

def generate_paths(num_paths, timestep, seq, multi=False, nb_assets=1):
    arr = np.zeros((num_paths*nb_assets, timestep+1))
    if not(multi):
        for i in range(num_paths):
            sample_path = seq.next()
            path = sample_path.value()
            if i==0:
                time = [path.time(j) for j in range(len(path))]
            value = [path[j] for j in range(len(path))]
            arr[i, :] = np.array(value)
    else:
        for i in range(num_paths):
            sample_path = seq.next()
            path = sample_path.value()
            if i==0:
                time = [path[0].time(j) for j in range(len(path[0]))]
            for k in range(nb_assets):
                value = [path[k][j] for j in range(len(path[k]))]
                arr[i*nb_assets+k, :] = np.array(value)
    return np.array(time), arr

def MakeHestonProcess(AsOfDate,**kwargs):
    rate_curve_handle = [(0)]
    div_curve_handle = [(0)]
    spot_handle = [(0)]
    v0 = [(0)]
    kappa = [(0)]
    theta = [(0)]
    sigma = [(0)]
    rho = [(0)]
    ql.Settings.instance().evaluationdate = AsOfDate
    DayCount = [(ql.Actual365Fixed())]
    if 'DayCount' in kwargs.keys():
        DayCount = [(kwargs.get('DayCount',None))]
    for (key,val) in kwargs.items():
        if key=='r' or key=='rate' or key=='R':
            rate_curve_handle = [(ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(val)),*DayCount)))]
        elif key=='q' or key=='div' or key=='Div':
            div_curve_handle = [(ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(val)),*DayCount)))]
        elif key=='s0' or key=='Spot' or key=='spot':
            spot_handle = [(ql.QuoteHandle(ql.SimpleQuote(val)))]
        elif key=='v0':
            v0=[(val)]
        elif key=='kappa':
            kappa=[(val)]
        elif key=='theta':
            theta=[(val)]
        elif key=='sigma' or key=='xi':
            sigma=[(val)]
        elif key=='rho' or key=='Correlation' or key=='correlation' or key=='Correl' or key=='correl':
            rho=[(val)]
    return ql.HestonProcess(*rate_curve_handle,*div_curve_handle,*spot_handle,*v0,*kappa,*theta,*sigma,*rho)

def MakeHestonModel(AsOfDate,**kwargs):
    return ql.HestonModel(MakeHestonProcess(AsOfDate,**kwargs))

def MakeAnalyticHestonEngine(AsOfDate,**kwargs):
    heston_model = MakeHestonModel(AsOfDate,**kwargs)
    relTolerance = [(0)]
    maxEvaluations = [(0)]
    if 'relTolerance' in kwargs.keys():
        relTolerance = [(kwargs.get('relTolerance'))]
    if 'maxEvaluations' in kwargs.keys():
        maxEvaluations = [(kwargs.get('maxEvaluations'))]
    return ql.AnalyticHestonEngine(heston_model,relTolerance,maxEvaluations)

#TO BE FINISHED
def generate_product_paths(num_paths, timestep, seq, product, FuncMakeEngine, AsOfDate, **ParamsEngine, multi=False, nb_assets=1):
    arr = np.zeros((num_paths*nb_assets, timestep+1))
    if not(multi):
        for i in range(num_paths):
            sample_path = seq.next()
            path = sample_path.value()
            if i==0:
                time = [path.time(j) for j in range(len(path))]
            value = [path[j] for j in range(len(path))]
            arr[i, :] = np.array(value)
    else:
        for i in range(num_paths):
            sample_path = seq.next()
            path = sample_path.value()
            if i==0:
                time = [path[0].time(j) for j in range(len(path[0]))]
            for k in range(nb_assets):
                value = [path[k][j] for j in range(len(path[k]))]
                arr[i*nb_assets+k, :] = np.array(value)
    return np.array(time), arr

if __name__=="__main__":
    AsOfDate = ql.Date(15,10,2018)
    MaturityDate = ql.Date(15,10,2019)

    length = 1
    timestep = MaturityDate-AsOfDate
    heston_process = MakeHestonProcess(AsOfDate,r=0.01,q=0.005,s0=100,v0=0.01,kappa=0.5,theta=0.01,sigma=0.05,rho=-0.5)
    times = [n/timestep*length for n in range(timestep+1)]
    rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(2*(len(times)-1),ql.UniformRandomGenerator()))
    seq = ql.GaussianMultiPathGenerator(heston_process,times,rng,False)

    #num_paths = 10
    #time, paths = generate_paths(num_paths, timestep,seq,True)
    #for i in range(num_paths):
    #    plt.plot(time, paths[i, :], lw=1, alpha=1)
    #plt.title("Heston Simulation")
    #plt.show()
    
    strike = 100
    option_type = ql.Option.Call
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    exercise = ql.EuropeanExercise(MaturityDate)
    european_option = ql.VanillaOption(payoff, exercise)
    
    rel_Tolerance = 0.01
    maxEval = 1000
    params_engine=dict(relTolerance=0.01,maxEvaluations=1000,
                r=0.01,q=0.005,s0=100,v0=0.01,kappa=0.5,theta=0.01,sigma=0.05,rho=-0.5)
    
    
    #engine = ql.AnalyticHestonEngine(ql.HestonModel(heston_process),0.01,1000)

    
    