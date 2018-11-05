import QuantLib as ql
import numpy as np
import matplotlib.pyplot as plt

AsOfDate = ql.Date(15,10,2018)
MaturityDate = ql.Date(15,10,2019)
DayCount = ql.Actual365Fixed()
ql.Settings.instance().evaluationdate = AsOfDate
calendar = ql.UnitedStates()
exercise = ql.EuropeanExercise(MaturityDate)

length = 1
timestep = MaturityDate-AsOfDate

constant_rate = 0.01
rate_curve = ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(constant_rate)),DayCount)
rate_curve_handle = ql.YieldTermStructureHandle(rate_curve)

constant_div = 0.005
div_curve = ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(constant_div)),DayCount)
div_curve_handle = ql.YieldTermStructureHandle(div_curve)

S0 = 100
S0_handle = ql.QuoteHandle(ql.SimpleQuote(S0))

v0 = 0.01
kappa = 0.5
theta = 0.01
sigma = 0.05
rho = -0.5

heston_process = ql.HestonProcess(rate_curve_handle,div_curve_handle,S0_handle,v0,kappa,theta,sigma,rho)
times = [n/timestep*length for n in range(timestep+1)]
rng = ql.GaussianRandomSequenceGenerator(ql.UniformRandomSequenceGenerator(2*(len(times)-1),ql.UniformRandomGenerator()))
TimeGrid = ql.TimeGrid(length,timestep)
seq = ql.GaussianMultiPathGenerator(heston_process,times,rng,False)
#heston_process.apply()

option_type = ql.Option.Call

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


def generate_paths_productHeston(num_paths, timestep, seq, multi=False, nb_assets=1):
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



#num_paths = 500
#time, paths = generate_paths(num_paths, timestep,seq,True)
#for i in range(num_paths):
#    plt.plot(time, paths[i, :], lw=1, alpha=1)
#plt.title("Heston Simulation")
#plt.show()