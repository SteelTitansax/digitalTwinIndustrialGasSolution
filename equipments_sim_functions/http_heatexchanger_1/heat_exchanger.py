import math
import logging

class HeatExchanger:
    def __init__(self, m_air, T_air_in, T_air_out, T_cooling_flow_in, T_cooling_flow_out, m_nitrogen, D, n, L, C_p_air, C_p_nitrogen_liquid):
        # Variables set up 
        self.m_air = m_air
        self.T_air_in = T_air_in
        self.T_air_out = T_air_out
        self.T_cooling_flow_in = T_cooling_flow_in
        self.T_cooling_flow_out = T_cooling_flow_out
        self.m_nitrogen = m_nitrogen
        self.D = D
        self.n = n
        self.L = L
        self.C_p_air = C_p_air
        self.C_p_nitrogen_liquid = C_p_nitrogen_liquid

        logging.info("Heat exchanger initial variables")
        logging.info("--------------------------------")
        logging.info(f"m_air: {m_air}")
        logging.info(f"T_air_in: {T_air_in}")
        logging.info(f"T_air_out: {T_air_out}")
        logging.info(f"T_cooling_flow_in: {T_cooling_flow_in}")
        logging.info(f"T_cooling_flow_out: {T_cooling_flow_out}")
        logging.info(f"m_nitrogen: {m_nitrogen}")
        logging.info(f"D: {D}")
        logging.info(f"n: {n}")
        logging.info(f"L: {L}")
        logging.info(f"C_p_air: {C_p_air}")
        logging.info(f"C_p_nitrogen_liquid: {C_p_nitrogen_liquid}")

    def kern_dimensioning(self, rho_air, mu_air, rho_nitrogen, mu_nitrogen):
        # Air thermic load (Q)
        Q_air = self.m_air * self.C_p_air * (self.T_air_in - self.T_air_out)
        logging.info(f"Q_air: {Q_air} J/s")
        
        # Liquide nytrogen thermic load (Q)
        Q_nitrogen = self.m_nitrogen * self.C_p_nitrogen_liquid * (self.T_cooling_flow_out - self.T_cooling_flow_in)
        logging.info(f"Q_nitrogen: {Q_nitrogen} J/s")
        logging.info("------------------------")

        # LMTD calculation
        delta_T1 = self.T_air_in - self.T_cooling_flow_out  # Bigger temperature difference
        delta_T2 = self.T_air_out - self.T_cooling_flow_in  # Smaller temperature difference

        if delta_T1 > 0 and delta_T2 > 0:
            delta_T_ml = (delta_T2 - delta_T1) / math.log(delta_T2 / delta_T1)
            logging.info(f"T Delta (LMTD): {delta_T_ml} K")
        else:
            delta_T_ml = None
            logging.info("Error: Not valid temperatures for LMTD calculation")
        
        # Cooling refrigerant mass calculation 
        
        m_cooling = Q_air / (self.C_p_nitrogen_liquid * (self.T_cooling_flow_out - self.T_cooling_flow_in))
        logging.info(f"required m_cooling: {m_cooling} kg/s")
        logging.info("------------------------")

        # Dimension parameters calculation and details 

        A_tubes = self.n * 3.1416 * (self.D**2 / 4)
        logging.info(f"Tubes area: {A_tubes} m²")
        v_air = self.m_air / (rho_air * A_tubes)
        logging.info(f"air velocity: {v_air} m/s")
        reynolds_air = (rho_air * v_air * self.D) / mu_air
        logging.info(f"Reynolds air: {reynolds_air}")
        f_air = 0.079 * (reynolds_air**-0.25)
        logging.info(f"frictión factor air: {f_air}")
        delta_P_air = (f_air * self.L * rho_air * (v_air**2)) / self.D
        logging.info(f"air pressure fall: {delta_P_air} Pa")
        logging.info(f"air pressure fall: {delta_P_air / 101300} atm")

        # Liquide nitrogen calculation 

        v_nitrogen = self.m_nitrogen / (rho_nitrogen * A_tubes)
        reynolds_nitrogen = (rho_nitrogen * v_nitrogen * self.D) / mu_nitrogen
        f_nitrogen = 0.079 * (reynolds_nitrogen ** -0.25)
        delta_nitrogen = (f_nitrogen * self.L * rho_nitrogen * (v_nitrogen**2)) / self.D
        logging.info(f"liquid nytrogen pressure fall: {delta_nitrogen} Pa")
        logging.info(f"liquid nytrogen pressure fall: {delta_nitrogen / 101300} atm")

        return [Q_air,Q_nitrogen,delta_T_ml,m_cooling,A_tubes,v_air,reynolds_air,f_air,delta_P_air,delta_nitrogen,v_nitrogen,reynolds_nitrogen,f_nitrogen,delta_nitrogen]