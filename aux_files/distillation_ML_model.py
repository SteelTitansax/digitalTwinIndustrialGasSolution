import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Cargamos los datos generados
df = pd.read_csv("asu_column_data.csv")

# Definimos variables de entrada (X) y salida (y)
X = df[["P_in", "T_in", "flow_rate", "energy_consumed", "Efficiency"]]
y = df[["H2_out", "N2_out", "O2_out"]]

# Dividimos en entrenamiento y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creamos el modelo de regresión lineal
model = LinearRegression()

# Entrenamos el modelo
model.fit(X_train, y_train)

# Predicciones para evaluar
y_pred = model.predict(X_test)

# Métricas de evaluación
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.5f}")
print(f"R2 Score: {r2:.5f}")

# Guardamos el modelo entrenado en un archivo .pkl
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "logistic_regression.pkl")  # mismo nombre que usa la función de Azure
joblib.dump(model, model_path)
print(f"Modelo guardado correctamente en: {model_path}")
