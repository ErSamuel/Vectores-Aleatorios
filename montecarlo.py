import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# Definimos la función y los parámetros
def f(x):
    return np.exp(x)
#NOTA: si quieres cambiar la función, asegúrate de actualizar también el valor exacto de la integral y el título del gráfico.
a, b = 0, 1
exact_value = spi.quad(f, a, b)[0]  # Valor exacto de la integral
# Se usa n muestras para ver los valores de la curva
n = int(input("Ingrese el número de muestras (N): "))

np.random.seed(42) #secuencia de números aleatorios fija para reproducibilidad

# Generamos todas las muestras de una vez
x_samples = np.random.uniform(a, b, n)
y_samples = f(x_samples)

# Se calcula la estimación de Montecarlo paso a paso (convergencia)
# np.cumsum va sumando: [y1, y1+y2, y1+y2+y3, ...]
# np.arange(1, n+1) crea el denominador: [1, 2, 3, ...]
cumulative_sum = np.cumsum(y_samples)
n_values = np.arange(1, n + 1)

# El promedio acumulado multiplicado por la longitud del intervalo (b-a = 1)
convergence_curve = (cumulative_sum / n_values) * (b - a)
error=np.abs(convergence_curve - exact_value)  # Error absoluto en cada paso
#Genera el gráfico
plt.figure(figsize=(10, 6))

# Graficamos la curva de convergencia
plt.plot(n_values, convergence_curve, color='blue', label=f'Estimación ({convergence_curve[-1]})\nError ({error[-1]})', linewidth=1.5)

# Trazamos una línea horizontal roja para el valor exacto
plt.axhline(y=exact_value, color='red', linestyle='--', label=f'Valor Exacto ({exact_value})', linewidth=2)

# Configuracion etiquetas y diseño
plt.title('Convergencia del Método de Montecarlo para $\int_0^1 e^x dx$', fontsize=14)
plt.xlabel(f'Número de muestras {n}', fontsize=12)
plt.ylabel('Valor Estimado', fontsize=12)
plt.xscale('log') # Escala logarítmica en X para ver mejor los primeros saltos
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(fontsize=12)

# Mostramos el gráfico
plt.show()