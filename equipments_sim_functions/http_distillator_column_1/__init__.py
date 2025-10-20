# Distillator http function 
# -----------------------------------------------------------------------------------------------
# Author : Manuel Portero Leiva 
# -----------------------------------------------------------------------------------------------
# Purpose : The purpose of this code is execute the design calculations of a distillator.
# ----------------------------------------------------------------------------------------------- 
# Input arguments : 
# -----------------------------------------------------------------------------------------------
# P_in Initial pressure (Pa)
# T_in Iniital Temperature (K)
# flow_rate (K???)
# energy_consumed (K)
# efficiency (percentage)
# submit boolean value
# -----------------------------------------------------------------------------------------------
# Output arguments : 
# -----------------------------------------------------------------------------------------------
# N2_out percentage of N2_out
# O2_out percentage of O2_out
# Ar_out percentage of Ar_out
# -----------------------------------------------------------------------------------------------

import logging
import azure.functions as func
import json
import joblib
import numpy as np
import pandas as pd
import pyodbc
import os 

def load_model(model_path):
    return joblib.load(model_path)

def predict(model, input_data):
    return model.predict(input_data)

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    try:

        req_body = req.get_json()

    except Exception as e:

        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    finally:

        # Variable declarations
        
        P_in = req_body.get('P_in') # Pa
        T_in = req_body.get('T_in') # K
        flow_rate = req_body.get('flow_rate') # K
        energy_consumed = req_body.get('energy_consumed') # K
        Efficiency = req_body.get('efficiency') # 
        submit = req_body.get('submit') # boolean

        
        # load model
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "logistic_regression.pkl")
        model = load_model(model_path)
    
        # Entry data
    
        data = pd.DataFrame({
            "P_in": [P_in],
            "T_in": [T_in],
            "flow_rate": [flow_rate],
            "energy_consumed": [energy_consumed],
            "Efficiency": [Efficiency]
        })


    
        # Predict
        result = predict(model, data)
        
        # Results
        
        logging.info("Output composition:")
        logging.info(f"Results: {result}")
        logging.info(f"H2_out (%): {result[0][0]:.4f}")
        logging.info(f"N2_out (%): {result[0][1]:.4f}")
        logging.info(f"O2_out (%): {result[0][2]:.4f}")
   

        return_json = { "P_in": str(P_in),
                        "T_in": str(T_in),
                        "N2_out" : str(round(result[0][1]*100,2)),  
                        "O2_out" : str(round(result[0][2]*100,2)), 
                        "H2_out" : str(round(result[0][0]*100,2)),  
                        "Efficiency": str(round(Efficiency*100,2))
                      }

        logging.info(return_json)

            
    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
