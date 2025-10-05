import numpy as np 
import logging
class Compressor:

    def __init__(self,P1,P2,Vm,R,T,Q,rho=1):
   
        self.P1 = P1   
        self.P2 = P2
        self.Vm = Vm
        self.R = R
        self.T = T
        self.Q = Q
        self.rho = rho

    def design(self):

        # Compressor ecuations 
        # -------------------------------------------------------

        density1 = self.P1/(self.R * self.T) # air density

        logging.info(f"density (kg/m3) {density1}")

        m = density1 * self.Q # molar mass flow

        logging.info(f"m (kg/s) {m}")

        W_total = m * self.R * self.T *  np.log(self.P2/self.P1) 

        logging.info(f"W total(KW) {W_total/1000}")

        P_real = (float(W_total) / self.rho) 
       
        logging.info(f"P real (Kw) {P_real/1000}")

        return [m,W_total/1000,P_real/1000]



