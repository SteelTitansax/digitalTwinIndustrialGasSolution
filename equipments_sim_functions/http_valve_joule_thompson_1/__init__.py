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
from config import settings 
import pyodbc

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    """

    server = settings.azure_sql.azure_sql_server
    database = settings.azure_sql.database
    username = settings.azure_sql.username
    password = settings.azure_sql.password
    drivers = [item for item in pyodbc.drivers()]
    driver = drivers[-1]
    logging.info("driver:{}".format(driver))
    

    #Create a connection string

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    """

    try:

        req_body = req.get_json()

    except Exception as e:

        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    finally:

        # Variable declarations
        # Entry conditions 
        # --------------------------------------------
        # Example: 200 bar a 100 K (Nitrogen)

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
                        "P_in" : str(result[0]), # Pascales
                        "P_out" : str(result[1]), # Pascales
                        "T_in" : str(result[2]), # K
                        "T_out" : str(result[3]), # K
                      }

        logging.info(return_json)
        
        """
        # If mode submit we insert simulation in database

        if submit : 
            
            try:    
                insert_query ="INSERT INTO [dbo].[xxxx] ([P_in],[P_out],[T_in],[T_out]) VALUES (?,?,?,?)"
                cursor.execute(insert_query,str(result[0]),str(result[1]),str(result[2]),str(result[3]))       
            except:
                cnxn.rollback()
            finally:
                cnxn.commit()
                cnxn.close()
        """

    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
