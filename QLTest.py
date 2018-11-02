import QuantLib as ql
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps, cumtrapz, romb
import math

# option data
maturity_date = ql.Date(15, 1, 2016)
spot_price = 100
strike_prices = range(70,131)

v0 = 0.1
theta = v0
kappa = 0.5
ksi = 0.3
rho = -0.75

dividend_rate =  0.0163
option_type = ql.Option.Call

risk_free_rate = 0.001
day_count = ql.Actual365Fixed()
calendar = ql.UnitedStates()

calculation_date = ql.Date(8, 5, 2015)
ql.Settings.instance().evaluationDate = calculation_date

# construct the European Option

exercise = ql.EuropeanExercise(maturity_date)

spot_handle = ql.QuoteHandle(
    ql.SimpleQuote(spot_price)
)
flat_ts = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, risk_free_rate, day_count)
)
dividend_yield = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, dividend_rate, day_count)
)
#flat_vol_ts = ql.BlackVolTermStructureHandle(
#    ql.BlackConstantVol(calculation_date, calendar, volatility, day_count)
#)

heston_process = ql.HestonProcess(flat_ts,
                                  dividend_yield,
                                  spot_handle,
                                  v0,
                                  kappa,
                                  theta,
                                  ksi,
                                  rho)

engine = ql.AnalyticHestonEngine(ql.HestonModel(heston_process),0.01,1000)

#bsm_process = ql.BlackScholesMertonProcess(spot_handle, 
#                                           dividend_yield, 
#                                           flat_ts, 
#                                           flat_vol_ts)

heston_prices = np.zeros(len(strike_prices))
i=0
for k in strike_prices:
    payoff = ql.PlainVanillaPayoff(option_type, k)
    european_option = ql.VanillaOption(payoff, exercise)
    european_option.setPricingEngine(engine)
    heston_prices[i] = european_option.NPV()
    i+=1

plt.plot(strike_prices,heston_prices)
