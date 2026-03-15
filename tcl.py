import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli, poisson, nbinom, expon

def imprimir_parametros(discreta,p1, p2):
    muestra= f"p={p1}" if discreta == 'Bernoulli' else f"λ={p1}" if discreta == 'Poisson' or discreta == 'Exponencial' else f"r={p1}, p={p2}" if discreta == 'Binomial Negativa' else f"λ={p1}"
    return muestra

def graficar_comparacion(dist_nombre, tipo_grafico, lista_N):
    # Parámetros matemáticos predefinidos para la demostración
    p_bern = 0.5
    lam_pois = 5.0
    r_nbinom, p_nbinom = 5, 0.5
    lam_exp = 1.0

    # Preparamos una cuadrícula de 2x2 para las 4 muestras
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    fig.suptitle(f"Análisis de {dist_nombre} con 4 Tamaños de Muestra", fontsize=16, fontweight='bold')

    for i, N in enumerate(lista_N):
        ax = axes[i]
        parametro2=None
        # 1. Generación de datos simulados y funciones teóricas
        if dist_nombre == 'Bernoulli':
            datos = bernoulli.rvs(p_bern, size=N)
            x_teo = np.array([0, 1])
            pdf_teo = bernoulli.pmf(x_teo, p_bern)
            cdf_teo = bernoulli.cdf(x_teo, p_bern)

            parametro1=p_bern
            es_discreta = True
        elif dist_nombre == 'Poisson':
            datos = poisson.rvs(lam_pois, size=N)
            x_teo = np.arange(0, max(datos) + 2)
            pdf_teo = poisson.pmf(x_teo, lam_pois)
            cdf_teo = poisson.cdf(x_teo, lam_pois)

            parametro1=lam_pois
            es_discreta = True
        elif dist_nombre == 'Binomial Negativa':
            datos = nbinom.rvs(r_nbinom, p_nbinom, size=N)
            x_teo = np.arange(0, max(datos) + 2)
            pdf_teo = nbinom.pmf(x_teo, r_nbinom, p_nbinom)
            cdf_teo = nbinom.cdf(x_teo, r_nbinom, p_nbinom)

            parametro1=r_nbinom
            parametro2=p_nbinom
            es_discreta = True
        elif dist_nombre == 'Exponencial':
            datos = expon.rvs(scale=1/lam_exp, size=N)
            x_teo = np.linspace(0, max(datos) if len(datos) > 0 else 5, 100)
            pdf_teo = expon.pdf(x_teo, scale=1/lam_exp)
            cdf_teo = expon.cdf(x_teo, scale=1/lam_exp)
            
            parametro1=lam_exp
            es_discreta = False

        # 2. Dibujado de las gráficas según la opción
        if tipo_grafico == '1' or tipo_grafico == '2': 
            # Histograma + Función de Masa/Densidad
            if es_discreta:
                bins = np.arange(min(datos) - 0.5, max(datos) + 1.5, 1)
                ax.hist(datos, bins=bins, density=True, alpha=0.5, color='skyblue', edgecolor='black', label='Simulación')
                ax.plot(x_teo, pdf_teo, 'ro', ms=6, label='PMF Teórica')
                ax.vlines(x_teo, 0, pdf_teo, colors='red', lw=2, alpha=0.7)
            else:
                ax.hist(datos, bins=30, density=True, alpha=0.5, color='lightgreen', edgecolor='black', label='Simulación')
                ax.plot(x_teo, pdf_teo, 'r-', lw=2, label='PDF Teórica')
            
            ax.set_title(f"Muestra: N = {N}/{imprimir_parametros(dist_nombre, parametro1, parametro2)}")
            ax.set_ylabel("Frecuencia Relativa")

        elif tipo_grafico == '3': 
            # Función de Distribución Acumulada (CDF Empírica vs Teórica)
            if es_discreta:
                # CDF Empírica escalonada
                ax.hist(datos, bins=np.arange(min(datos)-0.5, max(datos)+1.5, 1), density=True, cumulative=True, histtype='step', color='blue', lw=2, label='CDF Simulada')
                ax.step(x_teo, cdf_teo, where='post', color='red', lw=2, linestyle='--', label='CDF Teórica')
            else:
                ax.hist(datos, bins=50, density=True, cumulative=True, histtype='step', color='green', lw=2, label='CDF Simulada')
                ax.plot(x_teo, cdf_teo, 'r--', lw=2, label='CDF Teórica')
            
            ax.set_title(f"Acumulada: N = {N}/{imprimir_parametros(dist_nombre, parametro1, parametro2)}")
            ax.set_ylabel("Probabilidad Acumulada")

        ax.legend(loc='lower right' if tipo_grafico == '3' else 'upper right')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def menu_principal():
    distribuciones = {'1': 'Bernoulli', '2': 'Exponencial', '3': 'Poisson', '4': 'Binomial Negativa'}
    
    while True:
        print("\n" + "="*50)
        print("  COMPARADOR DE DISTRIBUCIONES (4 MUESTRAS)")
        print("="*50)
        for key, value in distribuciones.items():
            print(f"[{key}] {value}")
        print("[5] Salir")
        
        opc_dist = input("Elige una distribución -> ")
        if opc_dist == '5': break
        if opc_dist not in distribuciones: continue

        dist_seleccionada = distribuciones[opc_dist]

        # Pedir exactamente 4 tamaños de muestra
        lista_N = []
        print(f"\nIntroduce los 4 tamaños de muestra para {dist_seleccionada}:")
        for i in range(1, 5):
            while True:
                try:
                    n = int(input(f"  Tamaño de la muestra {i}: "))
                    if n > 0:
                        lista_N.append(n)
                        break
                    print("  El número debe ser mayor a 0.")
                except ValueError:
                    print("  Por favor, introduce un número entero.")

        print("\n¿Qué gráfica deseas comparar?")
        print("[1] Histograma y Función de Densidad/Masa")
        print("[2] Función de Distribución Acumulada (CDF)")
        opc_graf = input("Opción -> ")
        
        # Agrupé las opciones 1 y 2 de tu petición original para que el histograma 
        # siempre muestre la curva teórica encima, ya que es la mejor forma de comparar.
        if opc_graf in ['1', '2']:
            graficar_comparacion(dist_seleccionada, '1' if opc_graf == '1' else '3', lista_N)

if __name__ == "__main__":
    menu_principal()