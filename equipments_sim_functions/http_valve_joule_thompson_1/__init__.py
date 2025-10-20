# Thompson valve http function 
# -----------------------------------------------------------------------------------------------
# Author : Manuel Portero Leiva 
# -----------------------------------------------------------------------------------------------
# Purpose : The purpose of this code is execute the design calculations of a distillator.
# ----------------------------------------------------------------------------------------------- 
# Input arguments : 
# -----------------------------------------------------------------------------------------------
# gas Initial pressure (name)
# P_in Iniital Temperature (bar)
# P_out Final Temperature (bar)
# T_in Iniital Temperature (K)
# submit boolean value
# -----------------------------------------------------------------------------------------------
# Output arguments : 
# -----------------------------------------------------------------------------------------------
# P_in Iniital Temperature (bar)
# P_out Final Temperature (bar)
# T_in Iniital Temperature (K)
# T_out Final Temperature (K)
# -----------------------------------------------------------------------------------------------

import logging
import azure.functions as func
from http_valve_joule_thompson_1.valve_joule_thompson import Joule_Thompson_Valve
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
        # --------------------------------------------

        gas = req_body.get('gas')
        P_in = req_body.get('P_in') # Entry pressure in Pascals (200 bar)
        T_in = req_body.get('T_in') # Entry Temp in Kelvin
        P_out = req_body.get('P_out') # # 1 bar in Pascales
        submit = req_body.get('submit') # boolean


        logging.info("Joule-thompson valv initialied ...")

        JT_valve = Joule_Thompson_Valve(gas,P_in,T_in,P_out)

        result = JT_valve.design()

        # Mostrar resultados
        logging.info(f"In_Temperature : {T_in} K")
        logging.info(f"Out_Temperature: {result[3]:.2f} K")
        
        return_json = {
                        "P_in" : str(round(result[0],3)), # Pascales
                        "P_out" : str(round(result[1],3)), # Pascales
                        "T_in" : str(round(result[2],3)), # K
                        "T_out" : str(round(result[3],3)), # K
                      }

        logging.info(return_json)
        

    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
