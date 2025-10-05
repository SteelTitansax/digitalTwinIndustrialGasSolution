# Compressor http function 
# -----------------------------------------------------------------------------------------------
# Author : Manuel Portero Leiva 
# -----------------------------------------------------------------------------------------------
# Purpose : The purpose of this code is execute the design calculations of a compressor.
# ----------------------------------------------------------------------------------------------- 
# Input arguments : 
# -----------------------------------------------------------------------------------------------
# P1 Initial pressure (Pa)
# P2 Final pressure (Pa)
# Vm Molecular volume (m3 /kmol at 1 atm 273 K)
# R Gases constant (J / Kg ·mol)
# Q Flow (m3/s)
# rho (percentage)
# submit boolean value
# -----------------------------------------------------------------------------------------------
# Output arguments : 
# -----------------------------------------------------------------------------------------------
# m massic flow (kg/s)
# W_total total work enetgy (Kw)
# P_real Real Power (Kw)
# -----------------------------------------------------------------------------------------------

import logging
import azure.functions as func
from http_compressor_1.compressor import Compressor
import json
import pyodbc
from config import settings

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    """
    # Note : Code commented, not necessary in this point of the development 
    # ----------------------------------------------------------------------

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
        
        P1 = req_body.get('P1') # Pa
        P2 = req_body.get('P2') # Pa
        Vm = req_body.get('Vm') # m3 /kmol at 1 atm 273 K
        R = req_body.get('R') # J / Kg ·mol
        T = req_body.get('T') # K
        Q = req_body.get('Q')  # m3/s
        rho = req_body.get('rho') # percentage
        submit = req_body.get('submit') # boolean

        compressor = Compressor(P1,P2,Vm,R,T,Q,rho)

        logging.info("Compressor initialied ...")

        result = compressor.design()

        return_json = {
                        "m" : str(round(result[0],2)), # m (kg/s)
                        "W_total" : str(round(result[1],2)), # W total(KW)
                        "P_real" : str(round(result[2],2)), # P real (Kw)
                      }

        logging.info(return_json)

        """
        # Note : Code not necessary for this development stage 
        # ------------------------------------------------------

        # If mode submit we insert simulation in database

        if submit : 
            
            try:    
                insert_query ="INSERT INTO [dbo].[xxxx] ([m],[W_total],[P_real]) VALUES (?,?,?)"
                cursor.execute(insert_query,str(result[0]),str(result[1]),str(result[2]),str(result[3]))       
            except:
                cnxn.rollback()
            finally:
                cnxn.commit()
                cnxn.close()
        """            

    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
