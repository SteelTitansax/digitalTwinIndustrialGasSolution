import logging
import azure.functions as func
from http_heatexchanger_1.heat_exchanger import HeatExchanger
import json
import pyodbc

def main(req: func.HttpRequest) -> func.HttpResponse:
        
    try:

        req_body = req.get_json()

    except Exception as e:

        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    finally:

        # Variable declarations
        
        m_air = req_body.get('m_air') # kg/s
        T_air_in = req_body.get('T_air_in') # K
        T_air_out = req_body.get('T_air_out') # K
        T_cooling_flow_in = req_body.get('T_cooling_flow_in') # K
        T_cooling_flow_out = req_body.get('T_cooling_flow_out')  # K
        m_nitrogen = req_body.get('m_nitrogen') # percentage
        D = req_body.get('D') # m
        n = req_body.get('n') # number of tubes
        L = req_body.get('L') # m (exchange length)
        C_p_air = req_body.get('C_p_air') # J/kg·K (air heat capacity)
        C_p_nitrogen_liquid = req_body.get('C_p_nitrogen_liquid') # J/kg·K (nytrogen liquide heat capacity J/kg·K)
        rho_air = req_body.get('rho_air') # kg/m³
        mu_air = req_body.get('mu_air') # Pa·s
        rho_nitrogen = req_body.get('rho_nitrogen') # kg/m³ (nytrogen líquide density)
        mu_nitrogen = req_body.get('mu_nitrogen') # Pa·s (liquide nytrógen viscosity)
        submit = req_body.get('submit') # boolean


        # Heat exchanger initialization
        logging.info("Heat exchanger initialization ...")

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
        logging.info(f"rho_air: {rho_air}")
        logging.info(f"mu_air: {mu_air}")
        logging.info(f"rho_nitrogen: {rho_nitrogen}")
        logging.info(f"mu_nitrogen: {mu_nitrogen}")
        logging.info(f"submit: {submit}")

        heatExchanger = HeatExchanger(m_air, T_air_in, T_air_out, T_cooling_flow_in, T_cooling_flow_out, m_nitrogen, D, n, L, C_p_air, C_p_nitrogen_liquid)
        result = heatExchanger.kern_dimensioning(rho_air, mu_air, rho_nitrogen, mu_nitrogen)
    
        return_json = {
                        "Q_air" : str(round(result[0],3)), # J/s
                        "Q_nitrogen" : str(round(result[1],3)), # J/s
                        "delta_T_ml" : str(round(result[2],3)), # K
                        "m_cooling" : str(round(result[3],3)), # kg/s
                        "A_tubes" : str(round(result[4],3)), # m2
                        "v_air" : str(round(result[5],3)), # m/s
                        "reynolds_air" : str(round(result[6],3)), # -
                        "f_air" : str(round(result[7],3)), #
                        "delta_P_air" : str(round(result[8],3)), # Pa
                        "delta_P_nitrogen" : str(round(result[9],3)), # Pa
                        "v_nitrogen" : str(round(result[10],3)), # m/s
                        "reynolds_nitrogen" : str(round(result[11],3)), # -
                        "f_nitrogen" : str(round(result[12],3)), #
                        "delta_nitrogen" : str(round(result[13],3)) # -
                      }

        logging.info(return_json)

    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
