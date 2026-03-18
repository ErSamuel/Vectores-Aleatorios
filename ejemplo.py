import numpy as np
import scipy.stats as stats

#Ejemplo 5.4
# --- SIMULACIÓN DE MONTE CARLO ---
#Validacion mediante metodo de montecarlo para el problema de los estacionamientos
def simulacion():
    n_sims = 100000
    # Generamos 200 departamentos por cada una de las 100,000 simulaciones
    data = np.random.choice(autos, size=(n_sims, n_deps), p=probs)
    suma_autos = data.sum(axis=1)
    
    # Calculamos el percentil 95 de los resultados simulados
    percentil_95 = np.percentile(suma_autos, 95)
    return percentil_95

# 1. Configuración del problema
n_deps = 200                        # Número de departamentos
autos = np.array([0, 1, 2])         # Posibles números de autos por departamento
probs = np.array([0.1, 0.6, 0.3])   # Probabilidades de tener 0, 1 o 2 autos respectivamente
certeza = 0.95

# 2. Cálculos teóricos para un departamento
mu = np.sum(autos * probs)                               # Media de autos por departamento
var = np.sum((autos**2) * probs) - mu**2      # Varianza de autos por departamento

# 3. Parámetros para el total (TCL)
mu_total = n_deps * mu                                   # Media total de autos esperada
sigma_total = np.sqrt(n_deps * var)                      # Desviación estándar total de autos esperada

# 4. Encontrar el cuantil 0.95 de la distribución normal
# Queremos N tal que P(S <= N) = 0.95
n_espacios = stats.norm.ppf(certeza, loc=mu_total, scale=sigma_total)   # Cuantil 0.95 de la distribución normal con media mu_total y desviación sigma_total

print(f"Media de autos esperada: {mu_total}")
print(f"Número de espacios necesarios (teórico): {n_espacios:.2f}")
print(f"Debes construir: {int(np.ceil(n_espacios))} espacios.")

print(f"Resultado según simulación: {int(np.ceil(simulacion()))}")