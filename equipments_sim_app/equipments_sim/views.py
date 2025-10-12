from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import requests
import json

# Views definition
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
        except IntegrityError:
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

def absortion_column(request): 
    
    if request.method == 'GET':

        equipments = load_json("equipments")
        selected_equipment = "absortion_column.html"
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": ""})

    else : 
        try:

            # Input validations
            # -----------------

            if request.POST["x_starting_point"] == "" or request.POST["y_starting_point"] == "" or request.POST["HETP"] == "" : 
                error = "Please fill in all the fields and press calculate again."
                equipments = load_json("equipments")
                selected_equipment = "absortion_column.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Absortion column url 
            # --------------------
            
            absortion_column_url = "http://localhost:7071/api/http_absortion_column_1"

            x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16]
            y = [0.001, 0.0028, 0.0067, 0.01, 0.0126, 0.0142, 0.0157, 0.0170, 0.0177, 0.0190, 0.0202]
            x_starting_point = float(request.POST["x_starting_point"])
            y_starting_point = float(request.POST["y_starting_point"])
            HETP = float(request.POST["HETP"])
                
            # Absortion column payload
            # ------------------------
        
            absortion_column_payload = {
                "x": x,
                "y": y,
                "HETP": HETP,
                "x_starting_point": x_starting_point,
                "y_starting_point": y_starting_point,
                "submit": False
            }

            response = requests.post(absortion_column_url, data=json.dumps(absortion_column_payload))
            absortion_column_parameters = response.json()
            print(f"Absortion Column Parameters {absortion_column_parameters}")

            equipments = load_json("equipments")
            selected_equipment = "absortion_column_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "absortion_column_parameters": absortion_column_parameters, "error": ""})

        except IntegrityError:
            equipments = load_json("equipments")
            selected_equipment = "absortion_column.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": IntegrityError})


    
def compressor(request): 

    if request.method == 'GET':
        
        equipments = load_json("equipments")
        selected_equipment = "compressor.html"
        
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})

    else : 

        try:

            # Input validations
            # -----------------
            
            if  request.POST["P1"] == "" or request.POST["P2"] == "" or request.POST["Vm"] == "" or request.POST["T"] == "" or request.POST["Q"] == "" or request.POST["rho"] == "" : 
             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "compressor.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Compressor url 
            # --------------------
            
            compressor_url = "http://localhost:7071/api/http_compressor_1"
                
            # Compressor payload
            # ------------------------

            P1 = float(request.POST["P1"])
            P2 = float(request.POST["P2"])
            Vm = float(request.POST["Vm"])
            T = float(request.POST["T"])
            Q = float(request.POST["Q"])
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
            print(f"Compressor Parameters {compressor_parameters}")

            equipments = load_json("equipments")
            selected_equipment = "compressor_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "compressor_parameters": compressor_parameters, "error": ""})

        except IntegrityError:
            equipments = load_json("equipments")
            selected_equipment = "compressor.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": IntegrityError})



def distillator_column(request): 
  
    if request.method == 'GET':
        
        equipments = load_json("equipments")
        selected_equipment = "distillator_column.html"

        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})

    else : 

        try:

            # Input validations
            # -----------------
            
            if  request.POST["P_in"] == "" or request.POST["T_in"] == "" or request.POST["flow_rate"] == "" or request.POST["energy_consumed"] == "" or request.POST["efficiency"] == "" : 
             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "distillator.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Distillator url 
            # --------------------
            
            distillator_url = "http://localhost:7071/api/http_distillator_column_1"
                
            # Distillator payload
            # ------------------------

            P_in = float(request.POST["P_in"])
            T_in = float(request.POST["T_in"])
            flow_rate = float(request.POST["flow_rate"])
            energy_consumed = float(request.POST["energy_consumed"])
            efficiency = float(request.POST["efficiency"]) # J / mol · K 
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
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "distillator_parameters": distillator_parameters, "error": ""})

        except IntegrityError:
            equipments = load_json("equipments")
            selected_equipment = "distillator.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": IntegrityError})


def heat_exchanger(request): 
    """
    
        # Support Note : 
        # ------------------------------------------
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

    if request.method == 'GET':

        equipments = load_json("equipments")
        selected_equipment = "heat_exchanger.html"
        return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment})
    
    else:

        try:

            # Input validations
            # -----------------
            if (request.POST["m_air"] == "" or request.POST["T_air_in"] == "" or request.POST["T_air_out"] == "" or
                request.POST["T_cooling_flow_in"] == "" or request.POST["T_cooling_flow_out"] == "" or request.POST["m_nitrogen"] == "" or
                request.POST["D"] == "" or request.POST["L"] == "" or request.POST["n"] == ""):

             
                error = "Please fill in all the fields and press calculate again."
             
                equipments = load_json("equipments")
                selected_equipment = "distillator.html"
                return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": error})
            

            # Heat exchanger url 
            # --------------------
            
            heat_exchanger_url = "http://localhost:7071/api/http_heatexchanger_1"
                
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
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "heat_exchanger_parameters": heat_exchanger_parameters, "error": ""})

        except IntegrityError:
            equipments = load_json("equipments")
            selected_equipment = "heat_exchanger.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": IntegrityError})



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
            

            # Heat exchanger url 
            # --------------------
            
            heat_exchanger_url = "http://localhost:7071/api/http_valve_joule_thompson_1"
                
            # Heat exchanger payload
            # ------------------------

            # Heat exchanger parameters

            gas = request.POST["gas"]  # gas name        
            P_in = float(request.POST["P_in"])  # kg/s
            T_in = float(request.POST["T_in"])  # K
            P_out = float(request.POST["P_out"]) # K
            submit = True

            heat_exchanger_payload = {

                "gas" : gas,  
                "P_in" : P_in,
                "T_in" : T_in,
                "P_out" : P_out,
                "submit" : submit

            }

            response = requests.post(heat_exchanger_url, data=json.dumps(heat_exchanger_payload))
            joule_thompson_valve_parameters = response.json()
            print(f"Joule Thompson Parameters : {joule_thompson_valve_parameters}")

            equipments = load_json("equipments")
            selected_equipment = "valve_joule_thompson_design.html"
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment , "joule_thompson_valve_parameters": joule_thompson_valve_parameters, "error": ""})

        except IntegrityError:
            equipments = load_json("equipments")
            selected_equipment = "valve_joule_thompson.html"    
            return render(request,'landing.html', {"equipments" : equipments, "selected_equipment" : selected_equipment, "error": IntegrityError})
