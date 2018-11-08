import numpy as np

def GeneratePaths(NumPaths, GlobalData, PathGenerator):
    nb_assets = 1
    nb_factors = PathGenerator.GetNbFactors()
    timestep = int(PathGenerator.GetParams().get('dimension')/nb_factors)
    arr = np.zeros((NumPaths*nb_assets, timestep+1))
    
    seq = PathGenerator.Make(**GlobalData)
    
    for i in range(NumPaths):
        sample_path = seq.next()
        path = sample_path.value()
        path_ref = []
        if nb_factors == 1:
            path_ref = path
        else:
            path_ref = path[0]
        if i==0:
            time = [path_ref.time(j) for j in range(len(path))]
        for k in range(nb_assets):
            if k == 0:
                value = [path_ref[j] for j in range(len(path_ref))]
            else:
                value = [path[k][j] for j in range(len(path[k]))]
        arr[i*nb_assets+k, :] = np.array(value)
    return np.array(time), arr

def BacktestDeltaHedge1DWithRateDivConstant(GlobalData,PathGenerator,Instrument1D,PricingEngine,HedgingEngine,
                                          HedgingStepDays=1,Margin=0):
    
    #######################################################
    # ------ GLOBAL DATA (AsOfDate,Calendar,Day,Count): etc
    #######################################################
    
    ###############################################################
    # ------------- CONFIG SIMU PARAMS ----------------------------
    ###############################################################
    nb_assets = 1
    nb_factors = PathGenerator.GetNbFactors()
    timestep = int(PathGenerator.GetParams().get('dimension')/nb_factors)
    arr = np.zeros((2*nb_assets, timestep+1))
    
    ################################################################
    # ---- PATH SIMULATION & CONFIG ARRAYS
    ################################################################
    seq = PathGenerator.Make(**GlobalData)
    sample_path = seq.next()
    path = sample_path.value()
    path_ref = []
    if nb_factors == 1:
        path_ref = path
    else:
        path_ref = path[0]
    time = [path_ref.time(j) for j in range(len(path))]
    instrument_value = np.zeros(len(path_ref))
    portfolio_value = np.zeros(len(path_ref))
    
    #############################################################
    # ----- DATES AND HEDGING CONSTANT RATE/DIV CONFIG ---------
    #############################################################
    r = HedgingEngine.GetParams().get('r')
    q = HedgingEngine.GetParams().get('q')
    LocalDate = GlobalData.get('AsOfDate')
    DayCount =  GlobalData.get('DayCount')
    Delta = 0
    
    #######################################
    # ----- PRICING AND HEDGING ----------- 
    #######################################
    for m in range(len(path_ref)):
        #######################################################
        # -------- UPDATE DATA -------------------------------
        # --- TO BE CHANGED WHEN CALIBRATION METHODS READY ---
        #######################################################
        data = {}
        for k in range(nb_factors):
            if k == 0:
                data[PathGenerator.GetFactorName(k)] = path_ref[m]
            else:
                data[PathGenerator.GetFactorName(k)] = path[k][m]
        HedgingEngine.UpdateParams(**data)
        PricingEngine.UpdateParams(**data)
        
        #######################################################
        # ----- INSTRUMENT AT MARKET PRICE --------------------
        #######################################################
        Instrument1D.setPricingEngine(PricingEngine.Make(**GlobalData))
        instrument_value[m] = Instrument1D.NPV()
        
        #######################################################
        # --------- HEDGING COMPUTATION -----------------------
        #######################################################
        dt = DayCount.yearFraction(LocalDate,LocalDate-HedgingStepDays)
        if m==0:
            portfolio_value[m] = instrument_value[m]+Margin
        else:
            portfolio_value[m] = portfolio_value[m-1]+(np.exp((r-q)*dt)-1)*(portfolio_value[m-1]-Delta*path_ref[m-1])+Delta*(path_ref[m]-path_ref[m-1])
        Instrument1D.setPricingEngine(HedgingEngine.Make(**GlobalData))
        Delta = Instrument1D.delta()
        LocalDate = LocalDate + HedgingStepDays
        arr[0, :] = instrument_value
        arr[1, :] = portfolio_value
    return np.array(time), arr