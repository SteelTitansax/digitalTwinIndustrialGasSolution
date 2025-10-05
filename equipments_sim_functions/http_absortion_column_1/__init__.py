# Absortion column http function 
# -----------------------------------------------------------------------------------------------
# Author : Manuel Portero Leiva 
# -----------------------------------------------------------------------------------------------
# Purpose : The purpose of this code is execute the design calculations of an absortion column.
# ----------------------------------------------------------------------------------------------- 
# Input arguments : 
# -----------------------------------------------------------------------------------------------
# x : x axis of equilibrium data 
# y : y axis of equilibrium data 
# submit : boolean submit # boolean
# x_starting_point : x startng point of the iteration design
# y_starting_point : y starting point of the iteration design 
# -----------------------------------------------------------------------------------------------
# Output arguments : 
# -----------------------------------------------------------------------------------------------
# HETP (Height Equivalent to a Theoretical Plate (m))
# HE (Height Equivalent)
# Xn Product concentraction
# ns number of plates
# -----------------------------------------------------------------------------------------------

import logging
import azure.functions as func
import json
import pyodbc
from tabulate import tabulate
from http_absortion_column_1.absortion_column import AbsorptionColumn
from config import settings 

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    
    SQL NOT IMPLEMENTED YET 

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
        
        # Equilibrium data
        
        x = req_body.get('x') # Pa
        y = req_body.get('y') # Pa
        HETP = req_body.get('HETP') # m
        submit = req_body.get('submit') # boolean

        # Starting point

        x_starting_point = req_body.get('x_starting_point') # Pa
        y_starting_point = req_body.get('y_starting_point') # Pa

        # ORIENTATIVE INITIAL DATA PLEASE NOT REMOVE 
        # ---------------------------------------------------------------------------------------

        #x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16]
        #y = [0.001, 0.0028, 0.0067, 0.01, 0.0126, 0.0142, 0.0157, 0.0170, 0.0177, 0.0190, 0.0202]
        #x_starting_point = [0]
        #y_starting_point = [0.0048]
        
        logging.info("Equilibrium data")
        logging.info("----------------")

        results = list(zip(x, y))
        
        logging.info(tabulate(results, headers=["H2O mols/NaOH", "H2O mols/dry air mols"]))

        absorption_column = AbsorptionColumn(x, y, HETP, x_starting_point,y_starting_point)
        
        logging.info("Absortion column initialied ...")

        result = absorption_column.design()
        
        return_json = {
                        "HE" : str(result[0]), # m 
                        "HETP" : str(result[1]), # m
                        "Xn" : str(round(result[2],2)), # molar fraction liquid
                        "ns" : str(result[3]), # number of stages
                        "Yn" :str(round(result[4],2)) # molar fraction gas
                      }

        logging.info(return_json)

        # If mode submit we insert simulation in database
        
        """
        NOTE : TO BE IMPLEMENTED IN CLOUD

        if submit : 
            
            try:    
                insert_query ="INSERT INTO [dbo].[xxxx] ([HE],[HETP],[Xn],[ns]) VALUES (?,?,?,?)"
                cursor.execute(insert_query,str(result[0]),str(result[1]),str(result[2]),str(result[3]))       
            except:
                cnxn.rollback()
            finally:
                cnxn.commit()
                cnxn.close()
        """    
        logging.info("Request processed successfully.")

    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
