import numpy as np 
import logging
from tabulate import tabulate
import numpy as np
from sklearn.metrics import r2_score

class AbsorptionColumn:
    def __init__(self, x, y, HETP,x_starting_point,y_starting_point):
        self.x = x
        self.y = y
        self.HETP = HETP
        self.x_vals = [x_starting_point]
        self.y_vals = [y_starting_point]    

    def design(self):
        # 3rd-degree polynomial regression for equilibrium curve

        model = np.poly1d(np.polyfit(self.x, self.y, 3))
        myline = np.linspace(0, 16, 100)

        logging.info("\nRegression equation for equilibrium curve:")
        logging.info(model)
        logging.info(f"\nR² = {r2_score(self.y, model(self.x))}")
        
        # (L/V) min - Operating line at minimum solvent flow
        x_op =[2,6]
        y_op =[0.003, 0.0097]        
        # Note : This comment code is the exercise operative parameters for dry the input air current
        # keep it here as orientative data 
        # ---------------------------------------------------
        #x_op = [2.22, 6]
        #y_op = [0.0048, 0.0126]
        model2 = np.poly1d(np.polyfit(x_op, y_op, 1))

        logging.info("\nRegression equation for (L/V) min:")
        logging.info(model2)
        logging.info(f"\nR² = {r2_score(y_op, model2(x_op))}")

        # Increase flow rate by 40%
        
        a = np.polyfit(x_op, y_op, 1)
        new_slope = a[0] * 1.4  # Adjust slope

        # Calculate Xn for new operating line
        
        intercept = -0.00161358
        Y_nplus_one = 0.019
        Xn = (Y_nplus_one - intercept) / new_slope
        logging.info(f"\nCalculated Xn = {Xn}")

        # New operating line with increased solvent
        
        x_new_op = [2.22, Xn]
        y_new_op = [0.0048, Y_nplus_one]
        model2 = np.poly1d(np.polyfit(x_new_op, y_new_op, 1))
        

        logging.info("\nRegression equation for new operating line (40% more solvent):")
        logging.info(model2)

        # Define f(x) and its derivative fp(x) for Newton-Raphson
        
        def f(x, y):
            return 6.139e-6 * x**3 - 0.0003032 * x**2 + 0.005088 * x - 0.008814 - y

        def fp(x):
            return 3 * 6.139e-6 * x**2 - 2 * 0.0003032 * x + 0.005088

        # Newton-Raphson for equilibrium stages calculation
        
        logging.info("\nConcentrations at equilibrium stages:")
        logging.info("--------------------------------------")

        i = 0
        epsilon = 0.001
        x_vals = self.x_vals  # Initialize x values
        y_vals = self.y_vals  # Initialize y values (starting point)

        xv = 0.1
        xN = 0

        while xN <= Xn:
            xN = xv - (f(xv, y_vals[i]) / fp(xv))  # Newton-Raphson iteration
            if abs(xv - xN) > epsilon:
                xv = xN
            elif xN <= Xn:
                x_vals.append(xN)
                y_vals.append(model2(xN))  # Compute new y from the operating line equation
                logging.info(f"Stage {i+1}: x = {xN:.4f}, y = {y_vals[i+1]:.4f}")
                i += 1

        ns = i  # Number of stages
        logging.info(f"\nNumber of theoretical stages = {ns}")

        i=1 
        while i<ns:

            # Horizontal

            x1=[self.x[i-1],self.x[i]]
            y1=[self.y[i-1],self.y[i]]
            
            # Vertical

            x1=[self.x[i],self.x[i]]
            logging.info(f"x[{i}] = {self.x[i]}, y[{i}] = {self.y[i]}")
            y1=[self.y[i],self.y[i+1]]
            
            i+=1
        
        if i>=ns:
            x1=[self.x[i-1],self.x[i]]
            y1=[self.y[i],self.y[i]]
            logging.info(f"x[{i}] = {self.x[i]}, y[{i}] = {self.y[i]}")
            
        # Packed column height calculation

        HETP = self.HETP  # Height Equivalent to a Theoretical Plate (m)
        HE = HETP * ns

        # Out Gas Concentration 

        Yn = y_vals[-1]
        logging.info(f"Liquid molar fraction Xn:{Xn}. Gas molar fraction Yn:{Yn}")
        logging.info(f"Packing height = {HE} m")
        return [HE, HETP, Xn, ns , Yn]



