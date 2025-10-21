# Views section DWSIM app  
# -----------------------------------------------------------------------------------------------
# Author : Manuel Portero Leiva 
# -----------------------------------------------------------------------------------------------
# Purpose : Controller part of the DWSIM application. Acts as a app backend.
# ----------------------------------------------------------------------------------------------- 


from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from config import settings
from equipments_sim.database import absortion_column_publish
import pyodbc
import requests
import json
import os
import ast

# Database details 
# ------------------------------------------
server = os.getenv("AZURE_SQL_SERVER", settings.azure_settings.SERVER)
database = os.getenv("AZURE_SQL_DATABASE", settings.azure_settings.DATABASE)
username = os.getenv("AZURE_SQL_USERNAME", settings.azure_settings.USERNAME)
password = os.getenv("AZURE_SQL_PASSWORD", settings.azure_settings.PASSWORD)
drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]

# Auxiliar functions , login and landing page
# -----------------------------------------------

def load_json(file_name):
    with open(f"data/{file_name}.json","r",encoding="utf-8") as file : 
        return json.load(file)

def home(request): 
    welcome_message = True
    return render(request,'base.html',{'welcome_message': welcome_message})


def signup(request):
    welcome_message = False
    if request.method == 'GET':
        return render(request,'signup.html',
        {
            'form': UserCreationForm,
            'welcome_message': welcome_message 
        })

    else : 
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(username=request.POST['username'], password =
                request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('/landing')
        except Exception as e: 
            return render (request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'User already exists'
            })
        
    return render (request, 'signup.html', {
        'form': UserCreationForm,
        'error': 'Password do not match'        
    })


@login_required
def signout(request): 
    print("Logging out")
    logout(request)
    return redirect(home)


def signin(request):
    welcome_message = False
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'welcome_message': welcome_message
        })
    else: 
        user = authenticate(request,username=request.POST['username'], password = request.POST['password'])
        if user is None :
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            }) 
        else :
            login(request, user)
            return redirect ('/landing')

def landing(request): 
    equipments = load_json("equipments")
    selected_equipment = ""
    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})

# Equipments design functions
# -----------------------------------------------

def absortion_column(request): 
    
    if request.method == 'GET':

        equipments = load_json("equipments")
        selected_equipment = "absortion_column.html"
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": ""})

    else : 
        try:
            publish_mode = request.POST.get('publish_mode')

            if publish_mode == "true":

                HE = request.POST.get('HE')
                HETP = request.POST.get('HETP')
                Xn = request.POST.get('Xn')
                Yn = request.POST.get('Yn')
                ns = request.POST.get('ns')
                parameters = request.POST.get('absortion_column_payload')
                absortion_column_payload = ast.literal_eval(parameters)
                x = absortion_column_payload['x']
                y = absortion_column_payload['y']
                x_starting_point = absortion_column_payload['x_starting_point']
                y_starting_point = absortion_column_payload['y_starting_point']
                absortion_column_parameters = { 'HE' : HE , 'HETP' : HETP , 'Xn' : Xn , 'Yn' : Yn ,  'ns' : ns}

                try: 

                    #absortion_column_publish(driver, server, database, UID, PWD, HE, HETP, Xn, ns)
                    equipments = load_json("equipments")
                    selected_equipment = "absortion_column_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment ,
                         "absortion_column_parameters": absortion_column_parameters, "absortion_column_payload": absortion_column_payload,
                         "success":"Equipment configuration published successfully.","error": ""})
 
                except Exception as e:                     
                    print(e)            
                    error ="Error saving config in database"
                    equipments = load_json("equipments")
                    selected_equipment = "absortion_column_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment ,
                         "absortion_column_parameters": absortion_column_parameters, "absortion_column_payload": absortion_column_payload,
                         "success":"","error": error})
 

            # Input validations
            # -----------------

            if request.POST["x_starting_point"] == "" or request.POST["y_starting_point"] == "" or request.POST["HETP"] == "" : 
                error = "Please fill in all the fields and press calculate again."
                equipments = load_json("equipments")
                selected_equipment = "absortion_column.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            
            # Absortion column url 
            # --------------------

            absortion_column_url = os.getenv("URL_ABSORTION_COLUMN",settings.url_settings.absortion_column)

            x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16] # H2O mols/NaOH
            y = [0.001, 0.0028, 0.0067, 0.01, 0.0126, 0.0142, 0.0157, 0.0170, 0.0177, 0.0190, 0.0202] # H2O mols/dry air mols
            x_starting_point = float(request.POST["x_starting_point"]) # H2O mols/NaOH
            y_starting_point = float(request.POST["y_starting_point"]) # H2O mols/dry air mols
            HETP = float(request.POST["HETP"]) # m
                
            # Absortion column payload
            # ------------------------
        
            absortion_column_payload = {
                "x": x,
                "y": y,
                "HETP": HETP,
                "x_starting_point": x_starting_point,
                "y_starting_point": y_starting_point
            }

            response = requests.post(absortion_column_url, data=json.dumps(absortion_column_payload))
            absortion_column_parameters = response.json()
            
            equipments = load_json("equipments")
            selected_equipment = "absortion_column_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment ,
                         "absortion_column_parameters": absortion_column_parameters, "absortion_column_payload": absortion_column_payload,
                         "success":"", "error":""})

        except Exception as e: 
            print(e)            
            equipments = load_json("equipments")
            selected_equipment = "absortion_column.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": "Error submiting form, please contact your admin"})


    
def compressor(request): 

    if request.method == 'GET':
        
        equipments = load_json("equipments")
        selected_equipment = "compressor.html"
        
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})

    else : 

        try:

            publish_mode = request.POST.get('publish_mode')

            if publish_mode == "true":
                m = request.POST.get('m')
                W_total = request.POST.get('W_total')
                P_real = request.POST.get('P_real')
                parameters = request.POST.get('compressor_payload')
                compressor_payload = ast.literal_eval(parameters)
                compressor_parameters = { 'm' : m , 'W_total' : W_total , 'P_real' : P_real }

                try: 
                    #compressor_publish(driver, server, database, UID, PWD, m, W_total, P_real):
                    equipments = load_json("equipments")
                    selected_equipment = "compressor_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , 
                    "compressor_parameters": compressor_parameters, "compressor_payload": compressor_payload,  "success":"Equipment configuration published successfully.","error": ""})
 
                except Exception as e:                     
                    print(e)            
                    error ="Error saving config in database"
                    equipments = load_json("equipments")
                    selected_equipment = "absortion_column_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment ,
                         "absortion_column_parameters": absortion_column_parameters, "absortion_column_payload": absortion_column_payload,
                         "success":"","error": error})


            # Input validations
            # -----------------
            
            if  request.POST["P1"] == "" or request.POST["P2"] == "" or request.POST["Vm"] == "" or request.POST["T"] == "" or request.POST["Q"] == "" or request.POST["rho"] == "" : 
             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "compressor.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Compressor url 
            # --------------------
            
            compressor_url = os.getenv("URL_COMPRESSOR",settings.url_settings.compressor)
                
            # Compressor payload
            # ------------------------

            P1 = float(request.POST["P1"]) # Pa
            P2 = float(request.POST["P2"]) # Pa
            Vm = float(request.POST["Vm"]) # m³/kmol
            T = float(request.POST["T"]) # K
            Q = float(request.POST["Q"]) # m³/s
            rho = float(request.POST["rho"])
            R = float(8.314) # J / mol · K 
            compressor_payload = {
                "P1": P1,
                "P2": P2,
                "Vm": Vm,
                "T": T,
                "Q": Q,
                "R": R,
                "rho":rho,
                "submit": False
            }

            response = requests.post(compressor_url, data=json.dumps(compressor_payload))
            compressor_parameters = response.json()

            equipments = load_json("equipments")
            selected_equipment = "compressor_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , 
            "compressor_parameters": compressor_parameters, "compressor_payload": compressor_payload, "success": "", "error": ""})

        except Exception as e: 
            print(e)            
            equipments = load_json("equipments")
            selected_equipment = "compressor.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": "Error submiting form, please contact your admin"})



def distillator_column(request): 
  
    if request.method == 'GET':
        
        equipments = load_json("equipments")
        selected_equipment = "distillator_column.html"

        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})

    else : 

        try:

            publish_mode = request.POST.get('publish_mode')

            if publish_mode == "true":
                P_in = request.POST.get('P_in')
                T_in = request.POST.get('T_in')
                N2_out = request.POST.get('N2')
                H2_out = request.POST.get('H2')
                O2_out = request.POST.get('O2')

                efficiency = request.POST.get('efficiency')
                parameters = request.POST.get('distillator_payload')

                distillator_payload = ast.literal_eval(parameters)
                distillator_parameters = { 'P_in' : P_in , 'T_in' : T_in , 'N2_out' : N2_out , 'H2_out' : H2_out , 'O2_out' : O2_out , 'efficiency' : efficiency }

                try: 
                    #distillator_column_publish(driver, server, database, UID, PWD,N2_out,O2_out,Ar_out)
                    equipments = load_json("equipments")
                    selected_equipment = "distillator_column_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "distillator_parameters": distillator_parameters, "distillator_payload" : distillator_payload, "success": "Equipment configuration published successfully.", "error": ""})

                except Exception as e:         
                    print(e)            
                    error ="Error saving config in database"
                    equipments = load_json("equipments")
                    selected_equipment = "distillator_column_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "distillator_parameters": distillator_parameters, "distillator_payload" : distillator_payload, "success": "", "error": ""})




            # Input validations
            # -----------------
            
            if  request.POST["P_in"] == "" or request.POST["T_in"] == "" or request.POST["flow_rate"] == "" or request.POST["energy_consumed"] == "" or request.POST["efficiency"] == "" : 
             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "distillator_column.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Distillator url 
            # --------------------
            
            distillator_url = os.getenv("URL_DISTILLATOR_COLUMN",settings.url_settings.distillator_column)
                
            # Distillator payload
            # ------------------------

            P_in = float(request.POST["P_in"]) # Pa
            T_in = float(request.POST["T_in"]) # K
            flow_rate = float(request.POST["flow_rate"]) # 
            energy_consumed = float(request.POST["energy_consumed"]) # Kw
            efficiency = float(request.POST["efficiency"]) #  
            submit = False

            distillator_payload = {
                "P_in": P_in,
                "T_in": T_in,
                "flow_rate": flow_rate,
                "energy_consumed": energy_consumed,
                "efficiency": efficiency,
                "submit": submit
            }

            response = requests.post(distillator_url, data=json.dumps(distillator_payload))
            distillator_parameters = response.json()
            print(f"Distillator Parameters {distillator_parameters}")

            equipments = load_json("equipments")
            selected_equipment = "distillator_column_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "distillator_parameters": distillator_parameters, "distillator_payload" : distillator_payload, "success": "", "error": ""})

        except Exception as e:
            print(e) 
            equipments = load_json("equipments")
            selected_equipment = "distillator_column.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": "Error submiting form, please contact your admin"})


def heat_exchanger(request): 

    if request.method == 'GET':

        equipments = load_json("equipments")
        selected_equipment = "heat_exchanger.html"
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})
    
    else:

        try:

            publish_mode = request.POST.get('publish_mode')
            
            if publish_mode == "true":

                Q_air = request.POST.get('Q_air')
                Q_nitrogen = request.POST.get('Q_nitrogen')
                delta_T_ml = request.POST.get('delta_T_ml')
                delta_P_air = request.POST.get('delta_P_air')
                m_cooling = request.POST.get('m_cooling')
                A_tubes = request.POST.get('A_tubes')
                v_air = request.POST.get('v_air')
                f_air = request.POST.get('f_air')
                n = request.POST.get('n')
                delta_P_nitrogen = request.POST.get('delta_P_nitrogen')
                v_nitrogen = request.POST.get('v_nitrogen')
                reynolds_nitrogen = request.POST.get('reynolds_nitrogen')
                reynolds_air = request.POST.get('reynolds_air')
                f_nitrogen = request.POST.get('f_nitrogen')

                parameters = request.POST.get('heat_exchanger_payload')

                heat_exchanger_payload = ast.literal_eval(parameters)

                heat_exchanger_parameters = {
                    'Q_air': Q_air,
                    'Q_nitrogen': Q_nitrogen,
                    'delta_T_ml': delta_T_ml,
                    'delta_P_air' : delta_P_air,
                    'm_cooling': m_cooling,
                    'A_tubes': A_tubes,
                    'v_air': v_air,
                    'f_air': f_air,
                    'n': n,
                    'delta_P_nitrogen': delta_P_nitrogen,
                    'v_nitrogen': v_nitrogen,
                    'reynolds_nitrogen': reynolds_nitrogen,
                    'f_nitrogen': f_nitrogen,
                    'reynolds_air' : reynolds_air
                }

                try: 
                    #distillator_column_publish(driver, server, database, UID, PWD,N2_out,O2_out,Ar_out)
                    equipments = load_json("equipments")
                    selected_equipment = "heat_exchanger_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , 
                    "heat_exchanger_parameters": heat_exchanger_parameters, "heat_exchanger_payload": heat_exchanger_payload, "success": "Equipment configuration published successfully.", "error": ""})

                except Exception as e:         
                    print(e)            
                    error ="Error saving config in database"
                    equipments = load_json("equipments")
                    selected_equipment = "heat_exchanger_design.html"
                    return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , 
                    "heat_exchanger_parameters": heat_exchanger_parameters, "heat_exchanger_payload": heat_exchanger_payload, "success": "", "error": ""})

            # Input validations
            # -----------------

            if (request.POST["m_air"] == "" or request.POST["T_air_in"] == "" or request.POST["T_air_out"] == "" or
                request.POST["T_cooling_flow_in"] == "" or request.POST["T_cooling_flow_out"] == "" or request.POST["m_nitrogen"] == "" or
                request.POST["D"] == "" or request.POST["L"] == "" or request.POST["n"] == ""):

             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "heat_exchanger.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Heat exchanger url 
            # ------------------------
            
            heat_exchanger_url = os.getenv("URL_HEAT_EXCHANGER",settings.url_settings.heat_exchanger)
                
            # Heat exchanger payload
            # ------------------------

            # Heat exchanger parameters
        
            m_air = float(request.POST["m_air"])  # kg/s
            T_air_in = float(request.POST["T_air_in"])  # K
            T_air_out = float(request.POST["T_air_out"]) # K
            T_cooling_flow_in = float(request.POST["T_cooling_flow_in"])  # K (phase change liquide nytrogen)
            T_cooling_flow_out = float(request.POST["T_cooling_flow_out"])  # K
            m_nitrogen = float(request.POST["m_nitrogen"])  # kg/s
            D = float(request.POST["D"])  # m (tubes diameter )
            n = float(request.POST["n"])  # number of tubes
            L = float(request.POST["L"])  # m (exchange length)

            # Heat calorific capacity parameters
            
            C_p_air = 1005  # J/kg·K (air heat capacity)
            C_p_nitrogen_liquid = 2.9 * 1000  # J/kg·K (nytrogen liquide heat capacity J/kg·K)

            # Reynolds parameters
            
            rho_air = float(1.18)  # kg/m³
            mu_air = float(0.0000217)  # Pa·s
            rho_nitrogen = 800  # kg/m³ (nytrogen líquide density)
            mu_nitrogen = float(0.00019)  # Pa·s (liquide nytrógen viscosity)
            submit = True

            heat_exchanger_payload = {

                "m_air" : m_air,  
                "T_air_in" : T_air_in,
                "T_air_out" : T_air_out,
                "T_cooling_flow_in" : T_cooling_flow_in,
                "T_cooling_flow_out" : T_cooling_flow_out,
                "m_nitrogen" : m_nitrogen,
                "D" : D,
                "n" : n,
                "L" : L,

                # Heat calorific capacity parameters
                
                "C_p_air" : C_p_air, 
                "C_p_nitrogen_liquid" : C_p_nitrogen_liquid,  

                # Reynolds parameters
                
                "rho_air" : rho_air,
                "mu_air" : mu_air,
                "rho_nitrogen" : rho_nitrogen,
                "mu_nitrogen" : mu_nitrogen,
                "submit" : submit

            }

            response = requests.post(heat_exchanger_url, data=json.dumps(heat_exchanger_payload))
            heat_exchanger_parameters = response.json()
            print(f"Heat Exchanger Parameters : {heat_exchanger_parameters}")

            equipments = load_json("equipments")
            selected_equipment = "heat_exchanger_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , 
            "heat_exchanger_parameters": heat_exchanger_parameters, "heat_exchanger_payload": heat_exchanger_payload, "success": "", "error": ""})

        except Exception as e: 
            print(e)            
            equipments = load_json("equipments")
            selected_equipment = "heat_exchanger.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": "Error submiting form, please contact your admin"})



def valve_joule_thompson(request): 
    if request.method == 'GET':
    
        equipments = load_json("equipments")
        selected_equipment = "valve_joule_thompson.html"
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})
        
    else:

        try:

            # Input validations
            # -----------------
            
            if (request.POST["P_in"] == "" or request.POST["T_in"] == "" or request.POST["P_out"] == "" or
                request.POST["gas"] == "") :
             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "valve_joule_thompson.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Valve Joule Thompson url 
            # --------------------
            
            valve_joule_thompson_url = os.getenv("URL_VALVE_JOULE_THOMPSON",settings.url_settings.valve_joule_thompson)
                
            # Valve Joule Thompson payload
            # ------------------------

            # Valve Joule Thompson parameters

            gas = request.POST["gas"]  # gas name        
            P_in = float(request.POST["P_in"])  # kg/s
            T_in = float(request.POST["T_in"])  # K
            P_out = float(request.POST["P_out"]) # K
            submit = True

            valve_joule_thompson_payload = {

                "gas" : gas,  
                "P_in" : P_in,
                "T_in" : T_in,
                "P_out" : P_out,
                "submit" : submit

            }

            response = requests.post(valve_joule_thompson_url, data=json.dumps(valve_joule_thompson_payload))
            joule_thompson_valve_parameters = response.json()
            print(f"Joule Thompson Parameters : {joule_thompson_valve_parameters}")

            equipments = load_json("equipments")
            selected_equipment = "valve_joule_thompson_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "joule_thompson_valve_parameters": joule_thompson_valve_parameters, "error": ""})

        except Exception as e: 
            print(e)            
            equipments = load_json("equipments")
            selected_equipment = "valve_joule_thompson.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": "Error submiting form, please contact your admin"})
