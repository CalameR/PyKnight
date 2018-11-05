import QuantLib as ql

AsOfDate = ql.Date(15,10,2018)
DayCount = ql.Thirty360()
ql.Settings.instance().evaluationdate = AsOfDate

constant_rate = 0.01
rate_curve = ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(constant_rate),DayCount)
rate_curve_handle = ql.YieldTermStructureHandle(rate_curve)

constant_div = 0.005
div_curve = ql.FlatForward(AsOfDate,ql.QuoteHandle(ql.SimpleQuote(constant_rate),DayCount))
div_curve_handle = ql.YieldTermStructureHandle(div_curve)

S0 = 100
S0_handle = ql.QuoteHandle(ql.SimpleQuote(S0))

v0 = 0.01
kappa = 0.5
theta = 0.01
sigma = 0.05
rho = -0.5

heston_process = ql.HestonProcess(rate_curve_handle,disc_curve_handle,S0_handle,v0,kappa,theta,sigma,rho)
ql.MultiPath()
ql.GaussianPathGenerator()