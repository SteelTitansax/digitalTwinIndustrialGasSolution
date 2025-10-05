import logging
import azure.functions as func
import json
from config import settings
import pyodbc 
def main(req: func.HttpRequest) -> func.HttpResponse:
    
    
    try:

        req_body = req.get_json()

    except Exception as e:

        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    finally:

        # TODO : DOUBLE CHECK MATHEMATICS
        # --------------------------------

        # Variable declarations
        # --------------------------------
        # 
        # Compressor 
        # --------------------------------
                
        m_1 = "To Be Fetched By Cosmos" # m3 / h
        T_1 =  "To Be Fetched By Cosmos" # K only one temperature in the compressor ( isothermal )
        P_1 =  "To Be Fetched By Cosmos" # Pa
        P_2 = "To Be Fetched By Cosmos" # Pa
        R = 287 # J / kg K
        Vm_1 = "To Be Fetched By Cosmos" # m3 / kmol at 1 atm and 298 K  ( standart conditions )
        m_2 = 0
        
        # Compressor mass balance
        # --------------------------------
        #

        logging.error("Compressor mass Balance ...")
        
        m_1 = m_2 

        # Absortion mass balance
        # --------------------------------
        #
        
        m_2_v = m_2
        m_2_l = "To be fetched by cosmos"
        X_v_0 = "To be fetched by cosmos"
        X_v_1 = "To be fetched by cosmos"

        m_absortion = m_2_v * (X_v_1 - X_v_0)
        m_3_V = m_2_v - m_absortion

        m3_L = m_2_l + m_absortion

        # Heat exchanger mass balance
        # --------------------------------

        m_4 = m_3_V

        # Expansion Valve mass balance
        # --------------------------------

        m_5 = m_4

        # Distillation column mass balance
        # --------------------------------
        X_5_N2 = "To Be Fetched By Cosmos"
        X_5_O2 = "To Be Fetched By Cosmos"
        X_5_Ar = "To Be Fetched By Cosmos"
        X_6_N2 = "To Be Fetched By Cosmos"
        X_6_O2 = "To Be Fetched By Cosmos"
        X_6_Ar = "To Be Fetched By Cosmos"
        
        m_5_N2 = m_5 * X_5_N2 
        m_5_O2 = m_5 * X_5_O2
        m_5_Ar = m_5 * X_5_Ar

        m_6_N = m_5 * X_6_N2
        m_6_O = m_5 * X_6_O2
        m_6_Ar = m_5 * X_6_Ar
        
         
        
    return func.HttpResponse("Request processed successfully.", status_code=200)
    
        
