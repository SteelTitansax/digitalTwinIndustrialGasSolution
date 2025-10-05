import logging
import azure.functions as func
from http_heatexchanger_1.heat_exchanger import HeatExchanger
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

        """
        # Heat exchanger parameters
        
        m_air = 4.93  # kg/s
        T_air_in = 298  # K
        T_air_out = 100  # K
        T_cooling_flow_in = 77  # K (phase change liquide nytrogen)
        T_cooling_flow_out = 100  # K
        m_nitrogen = 2.78  # kg/s
        D = 0.02  # m (tubes diameter )
        n = 50  # number of tubes
        L = 5  # m (exchange length)

        # Heat calorific capacity parameters
        
        C_p_air = 1005  # J/kg·K (air heat capacity)
        C_p_nitrogen_liquid = 2.9 * 1000  # J/kg·K (nytrogen liquide heat capacity J/kg·K)

        # Reynolds parameters
        
        rho_air = 1.18  # kg/m³
        mu_air = 0.0000217  # Pa·s
        rho_nitrogen = 800  # kg/m³ (nytrogen líquide density)
        mu_nitrogen = 0.00019  # Pa·s (liquide nytrógen viscosity)
        """

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
                        "Q_air" : str(result[0]), # J/s
                        "Q_nitrogen" : str(result[1]), # J/s
                        "delta_T_ml" : str(result[2]), # K
                        "m_cooling" : str(result[3]), # kg/s
                        "A_tubes" : str(result[4]), # m2
                        "v_air" : str(result[5]), # m/s
                        "reynolds_air" : str(result[6]), # -
                        "f_air" : str(result[7]), #
                        "delta_P_air" : str(result[8]), # Pa
                        "delta_P_nitrogen" : str(result[9]), # Pa
                        "v_nitrogen" : str(result[10]), # m/s
                        "reynolds_nitrogen" : str(result[11]), # -
                        "f_nitrogen" : str(result[12]), #
                        "delta_nitrogen" : str(result[13]), # -
                      }

        logging.info(return_json)
        """

        # If mode submit we insert simulation in database

        if submit : 
            
            try:    
                insert_query ="INSERT INTO [dbo].[xxxx] ([Q_air],[Q_nitrogen],[delta_T_ml],[m_cooling],[A_tubes],[v_air],[reynolds_air],[f_air],[delta_P_air],[delta_P_nitrogen],[v_nitrogen],[reynolds_nitrogen],[f_nitrogen],[delta_nitrogen]) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                cursor.execute(insert_query,str(result[0]),str(result[1]),str(result[2]),str(result[3]),result[4],str(result[5]),str(result[6]),str(result[7]),result[8],str(result[9]),str(result[10]),str(result[11]),str(result[12]),str(result[13]))       
            except:
                cnxn.rollback()
            finally:
                cnxn.commit()
                cnxn.close()
        
        """


    return func.HttpResponse(json.dumps(return_json), status_code=200)
    

        
