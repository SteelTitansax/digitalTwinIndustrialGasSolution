import CoolProp.CoolProp as CP

class Joule_Thompson_Valve:
    def __init__(self, gas, P_in, T_in,P_out):        
        self.gas = gas
        self.P_in = P_in
        self.T_in = T_in
        self.P_out = P_out

    def design(self):
        
        # Entry entrophy calculation
        # --------------------------------
        
        h_in = CP.PropsSI("H", "P", self.P_in, "T", self.T_in, self.gas)

        # Out temperature with constant entrophy (isentrópica expansion)
        # --------------------------------------------------------------

        T_out = CP.PropsSI("T", "P", self.P_out, "H", h_in, self.gas)

        return [self.P_in,self.P_out,self.T_in,T_out]



        