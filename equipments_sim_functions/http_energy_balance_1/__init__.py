import logging
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    try:

        req_body = req.get_json()

    except Exception as e:

        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

    finally:

        # Variable declarations
        
        T1 = "To be fetched by Cosmos" # K

        # Energy balance in the compressor
        T2 = T1 # K 


        # Energy balance in the abosrtion column
        
        m2_L = "to be fetched by Cosmos" # kg/s
        m2_V = "to be fetched by Cosmos" # kg/s
        m3_L = "to be fetched by Cosmos" # kg/s
        m3_V = "to be fetched by Cosmos" # kg/s
        Cp2_L = "to be fetched by Cosmos" # J/kgK
        Cp2_V = "to be fetched by Cosmos" # J/kgK
        Cp3_L = "to be fetched by Cosmos" # J/kgK
        Cp3_V = "to be fetched by Cosmos" # J/kgK

        T3 = (m2_L*Cp2_L*T2 + m2_V*Cp2_V*T2)/(m3_L*Cp3_L + m3_V*Cp3_V) # K


        # Energy balance in the heat exchanger
        T4 = "To be fetched by Cosmos" # K
        m4_L = "To be fetched by Cosmos" # kg/s
        Cp4_L = "To be fetched by Cosmos" # J/kgK

        Q4 = m4_L*Cp4_L*(T4 - T3) # J/s

        # Energy balance in joule tompson valve

        T5 = "To be calculated by function valve"

        # Energy balance in the distillator column

        m5_N = "To be fetched by Cosmos" # kg/s
        m5_O2 = "To be fetched by Cosmos" # kg/s
        m5_Ar = "To be fetched by Cosmos" # kg/s
        m5_waste = "To be fetched by Cosmos" # kg/s
        Cp5_N = "To be fetched by Cosmos" # J/kgK
        Cp5_O2 = "To be fetched by Cosmos" # J/kgK
        Cp5_Ar = "To be fetched by Cosmos" # J/kgK
        Cp5_waste = "To be fetched by Cosmos" # J/kgK
        m6_N = "To be fetched by Cosmos" # kg/s
        m6_O2 = "To be fetched by Cosmos" # kg/s
        m6_Ar = "To be fetched by Cosmos" # kg/s
        m6_waste = "To be fetched by Cosmos" # kg/s
        Cp6_N = "To be fetched by Cosmos" # J/kgK
        Cp6_O2 = "To be fetched by Cosmos" # J/kgK
        Cp6_Ar = "To be fetched by Cosmos" # J/kgK
        Cp6_waste = "To be fetched by Cosmos" # J/kgK

        # Numerator of the energy balance equation
        numerator = (m5_N * Cp5_N * T5 + 
                    m5_O2 * Cp5_O2 * T5 + 
                    m5_Ar * Cp5_Ar * T5 + 
                    m5_waste * Cp5_waste * T5)
        
        # Denominator of the energy balance equation
        denominator = (m6_N * Cp6_N + 
                    m6_O2 * Cp6_O2 + 
                    m6_Ar * Cp6_Ar + 
                    m6_waste * Cp6_waste)
        
        # Compute T6
        T6 = numerator / denominator 
            
    return func.HttpResponse("Request processed successfully.", status_code=200)
    

        
