import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt

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

def MakeHestonProcess_GetParameterNames():
    return 'AsOfDate', 'r', 'q', 's0', 'v0', 'kappa', 'theta', 'sigma', 'rho'

def MakeHestonProcess(AsOfDate,**kwargs):
    rate_curve_handle = [0]
    div_curve_handle = [0]
    spot_handle = [0]
    v0 = [0]
    kappa = [0]
    theta = [0]
    sigma = [0]
    rho = [0]
    DayCount = [ql.Actual365Fixed()]
    ql.Settings.instance().evaluationdate = AsOfDate
    if 'DayCount' in kwargs.keys():
        DayCount = [kwargs.get('DayCount',None)]
    for (key,val) in kwargs.items():
        if key=='r':
            rate_curve_handle = [ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(val)),*DayCount))]
        elif key=='q':
            div_curve_handle = [ql.YieldTermStructureHandle(ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(val)),*DayCount))]
        elif key=='s0':
            spot_handle = [ql.QuoteHandle(ql.SimpleQuote(val))]
        elif key=='v0':
            v0=[val]
        elif key=='kappa':
            kappa=[val]
        elif key=='theta':
            theta=[val]
        elif key=='sigma':
            sigma=[val]
        elif key=='rho':
            rho=[val]
    return ql.HestonProcess(*rate_curve_handle,*div_curve_handle,*spot_handle,*v0,*kappa,*theta,*sigma,*rho)

def MakeHestonModel_GetParameterNames():
    return MakeHestonProcess_GetParameterNames()

def MakeHestonModel(AsOfDate,**kwargs):
    return ql.HestonModel(MakeHestonProcess(AsOfDate,**kwargs))

def MakeAnalyticHestonEngine(AsOfDate,**kwargs):
    heston_model = MakeHestonModel(AsOfDate,**kwargs)
    relTolerance = [0]
    maxEvaluations = [0]
    if 'relTolerance' in kwargs.keys():
        relTolerance = [kwargs.get('relTolerance',None)]
    if 'maxEvaluations' in kwargs.keys():
        maxEvaluations = [kwargs.get('maxEvaluations',None)]
    return ql.AnalyticHestonEngine(heston_model,*relTolerance,*maxEvaluations)

def MakeAnalyticHestonEngine_GetParameterNames():
    return MakeHestonModel_GetParameterNames(), 'relTolerance', 'maxEvaluations'

def MakeUniformRandomSequenceGenerator_GetParameterNames():
    return 'dimension'

def MakeUniformRandomSequenceGenerator(**kwargs):
    return ql.UniformRandomSequenceGenerator(kwargs.get('dimension'),ql.UniformRandomGenerator())

def MakeGaussianRandomSequenceGenerator_GetParameterNames():
    return MakeUniformRandomSequenceGenerator_GetParameterNames()

def MakeGaussianRandomSequenceGenerator(**kwargs):
    return ql.GaussianRandomSequenceGenerator(MakeUniformRandomSequenceGenerator(**kwargs))

def MakeHestonPathGenerator_GetParameterNames():
    return MakeHestonProcess_GetParameterNames, 'times', MakeGaussianRandomSequenceGenerator_GetParameterNames(), 'brownianBridge'

def MakeHestonPathGenerator(AsOfDate,**kwargs):
    brownianBridge = [False]
    if 'brownianBridge' in kwargs.keys():
        brownianBridge = [kwargs.get('brownianBridge')]
    kwargs_GaussianSeq = kwargs
    kwargs_GaussianSeq['dimension'] = 2*(len(kwargs.get('times'))-1)
    return ql.GaussianMultiPathGenerator(MakeHestonProcess(AsOfDate,**kwargs),
                                         kwargs.get('times'),
                                         MakeGaussianRandomSequenceGenerator(**kwargs_GaussianSeq),
                                         *brownianBridge)

def UpdateInitialValuesHestonProcess(params_process,*heston_path):
    params_process['s0']=heston_path[0]
    params_process['v0']=heston_path[1]

if __name__=="__main__":
    AsOfDate = ql.Date(15,10,2018)
    MaturityDate = ql.Date(15,10,2019)

    length = 1
    timestep = MaturityDate-AsOfDate
    params_process={'r':0.01,'q':0.005,'s0':100,'v0':0.01,'kappa':0.5,'theta':0.01,'sigma':0.05,'rho':-0.5}
    
    params_generator = params_process
    params_generator['times']=[n/timestep*length for n in range(timestep+1)]
    params_generator['brownianBridge']=False
    seq = MakeHestonPathGenerator(AsOfDate,**params_generator)
    
    params_engine = params_process
    params_engine['relTolerance']=0.01
    params_engine['maxEvaluations']=1000
    
    #heston_process = MakeHestonProcess(AsOfDate,r=0.01,q=0.005,s0=100,v0=0.01,kappa=0.5,theta=0.01,sigma=0.05,rho=-0.5)
    #times = [n/timestep*length for n in range(timestep+1)]
    #rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(2*(len(times)-1),ql.UniformRandomGenerator()))
    #seq = ql.GaussianMultiPathGenerator(heston_process,times,rng,False)
    
    strike = 100
    option_type = ql.Option.Call
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    exercise = ql.EuropeanExercise(MaturityDate)
    european_option = ql.VanillaOption(payoff, exercise)
    
    engine = MakeAnalyticHestonEngine(AsOfDate,**params_engine)
    
    
    
    european_option.setPricingEngine(engine)
    print(european_option.NPV())
    
    
    num_paths=10
    nb_assets=1
    arr = np.zeros((num_paths*nb_assets, timestep+1))
    for i in range(num_paths):
            sample_path = seq.next()
            path = sample_path.value()
            if i==0:
                time = [path[0].time(j) for j in range(len(path[0]))]
            for k in range(nb_assets):
                pricing_values = np.zeros(len(path[k]))
                for m in range(len(path[k])):
                    UpdateInitialValuesHestonProcess(params_process, path[0][m], path[1][m])
                    #print(path[0][m])
                    #print(path[1][m])
                    #print(params_process)
                    #print(params_engine)
                    engine = MakeAnalyticHestonEngine(AsOfDate,**params_engine)
                    european_option.setPricingEngine(engine)
                    #european_option.setPricingEngine(engine)
                    pricing_values[m] = european_option.NPV()
                    ######################
                    #TO MODIFY#
                    AsOfDate = AsOfDate + 1
                    ql.Settings.instance().evaluationDate = AsOfDate
                    #TO MODIFY#
                    ##################
                #value = [path[k][j] for j in range(len(path[k]))]
                arr[i*nb_assets+k, :] = np.array(pricing_values)
    time, paths = np.array(time), arr
    
    #time, paths = generate_paths(num_paths,timestep,seq,True)
    for i in range(num_paths):
        plt.plot(time, paths[i, :], lw=1, alpha=1)
    plt.title("Heston Price Simulation")
    plt.show()
    