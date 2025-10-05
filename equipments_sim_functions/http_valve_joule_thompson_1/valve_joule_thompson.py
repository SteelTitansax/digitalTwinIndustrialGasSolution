import numpy as np 
import logging
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
        
        s_in = CP.PropsSI("S", "P", self.P_in, "T", self.T_in, self.gas)

        # Out temperature with constant entrophy (isentrópica expansion)
        # --------------------------------------------------------------

        T_out = CP.PropsSI("T", "P", self.P_out, "S", s_in, self.gas)

        return [self.P_in,self.P_out,self.T_in,s_in,T_out]



