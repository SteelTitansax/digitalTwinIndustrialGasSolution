import pandas as pd
import numpy as np

# Número de muestras
n_samples = 500
np.random.seed(42)

# Valores de entrada base
P_in_base = 101325       # Pa
T_in_base = 77                  # K
flow_rate_base = 0.85 
energy_consumed_base = 277  # kWh aprox
Efficiency_base = 0.9

# Generamos pequeñas variaciones alrededor de la configuración deseada
P_in = P_in_base + np.random.normal(0, 1000, n_samples)
T_in = T_in_base + np.random.normal(0, 1, n_samples)
flow_rate = flow_rate_base + np.random.normal(0, 10, n_samples)
energy_consumed = energy_consumed_base + np.random.normal(0, 20, n_samples)
Efficiency = Efficiency_base + np.random.normal(0, 0.01, n_samples)

# Salidas: H2, N2, O2 altas, Ar muy baja
H2_out = np.random.uniform(0.25, 0.35, n_samples)
N2_out = np.random.uniform(0.35, 0.45, n_samples)
O2_out = np.random.uniform(0.20, 0.30, n_samples)
Ar_out = np.random.uniform(0.001, 0.01, n_samples)

# Normalizamos para que la suma sea 1
total = H2_out + N2_out + O2_out + Ar_out
H2_out /= total
N2_out /= total
O2_out /= total
Ar_out /= total

# Creamos DataFrame
df = pd.DataFrame({
    "P_in": P_in,
    "T_in": T_in,
    "flow_rate": flow_rate,
    "energy_consumed": energy_consumed,
    "Efficiency": Efficiency,
    "H2_out": H2_out,
    "N2_out": N2_out,
    "O2_out": O2_out,
    "Ar_out": Ar_out
})

# Guardamos CSV
df.to_csv("asu_column_data_low_temp.csv", index=False)
print("CSV generado correctamente: asu_column_data_low_temp.csv")

