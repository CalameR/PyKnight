import OneAssetOption as Opt1D

class VanillaOption(Opt1D.OneAssetOption):
    def __init__(self,payoff,exercise):
        Opt1D.OneAssetOption.__init__(self,payoff,exercise)