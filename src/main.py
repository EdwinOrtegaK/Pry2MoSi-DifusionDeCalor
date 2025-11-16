# src/main.py

import os
import numpy as np

from .scenarios import (
    escenario_borde_superior_caliente,
    escenario_centro_caliente,
    escenario_puntos_calientes_aleatorios,
)
from .heat_equation import HeatEquationSolver
from .analysis import (
    compute_stats,
    print_stats,
    compute_time_series_stats,
)
from .visualize import (
    plot_heatmap,
    animate_heatmap,
    plot_time_series,
    plot_space_time_heatmap,
)


def correr_escenario_borde_superior():
    """
    Escenario 1:
    - Borde superior mantenido a 100°C
    - Resto de bordes a 0°C
    - Simulación larga (t_final grande) para analizar la difusión.
    """
    cfg = escenario_borde_superior_caliente()
    solver = HeatEquationSolver(cfg)

    # Guardamos snapshots cada cierto número de pasos
    # Con t_final=5000 y dt=0.1 -> 50000 pasos
    # store_every=200 -> ~250 snapshots
    times, snapshots = solver.run(store_every=200)

    # Estado final
    if snapshots:
        T_final = snapshots[-1]
    else:
        T_final = solver.T

    # Guardar datos numéricos
    os.makedirs("results/datos", exist_ok=True)
    np.save("results/datos/T_final_borde_superior.npy", T_final)

    # Estadísticas al tiempo final
    stats = compute_stats(T_final, cfg, cfg.t_final)
    print_stats("Borde superior caliente", stats)

    # Heatmap estado final
    plot_heatmap(
        T_final,
        title=f"Escenario borde superior caliente (t = {cfg.t_final} s)",
        save_path="results/figuras/borde_superior_final.png",
    )

    # Series de tiempo y animación (si hubo snapshots)
    if snapshots:
        ts_stats = compute_time_series_stats(times, snapshots)

        # Curva de temperatura promedio vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.T_mean,
            ylabel="Temperatura promedio",
            title="Temperatura promedio vs tiempo (borde superior caliente)",
            save_path="results/figuras/borde_superior_Tmean_vs_t.png",
        )

        # Curva de energía total vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.total_energy,
            ylabel="Energía total (sum(T))",
            title="Energía total vs tiempo (borde superior caliente)",
            save_path="results/figuras/borde_superior_energy_vs_t.png",
        )

        # Mapa tiempo–espacio en la columna central
        plot_space_time_heatmap(
            snapshots,
            times,
            axis="y",  # fijamos una columna y vemos cómo baja el calor desde el borde
            index=cfg.nx // 2,  # columna central de la placa
            title="Mapa tiempo–espacio (columna central, borde superior caliente)",
            save_path="results/figuras/borde_superior_space_time_col_central.png",
        )

        # GIF de la evolución
        animate_heatmap(
            times,
            snapshots,
            title_prefix="Escenario borde superior caliente",
            save_path="results/figuras/borde_superior_anim.gif",
        )

def correr_escenario_centro_caliente():
    """
    Escenario 2:
    - Bordes a 0°C
    - Región central inicialmente caliente (100°C)
    - Difusión radial desde el centro (simulación más corta).
    """
    cfg = escenario_centro_caliente()
    solver = HeatEquationSolver(cfg)

    # Definir región central caliente en la condición inicial
    nx, ny = solver.T.shape
    cx, cy = nx // 2, ny // 2
    radio = min(nx, ny) // 8  # tamaño del "punto" caliente

    for i in range(cx - radio, cx + radio):
        if i < 0 or i >= nx:
            continue
        for j in range(cy - radio, cy + radio):
            if j < 0 or j >= ny:
                continue
            solver.T[i, j] = 100.0

    # Asegurar que los bordes respeten las condiciones de frontera
    solver._apply_boundary_conditions()

    # Simulación más corta, pero con snapshots para GIF
    times, snapshots = solver.run(store_every=10)

    if snapshots:
        T_final = snapshots[-1]
    else:
        T_final = solver.T

    # Guardar datos numéricos
    os.makedirs("results/datos", exist_ok=True)
    np.save("results/datos/T_final_centro_caliente.npy", T_final)

    # Estadísticas básicas al final
    stats = compute_stats(T_final, cfg, cfg.t_final)
    print_stats("Centro caliente", stats)

    # Heatmap estado final
    plot_heatmap(
        T_final,
        title=f"Escenario centro caliente (t = {cfg.t_final} s)",
        save_path="results/figuras/centro_caliente_final.png",
    )

    # GIF de la evolución
    if snapshots:
        ts_stats = compute_time_series_stats(times, snapshots)

        # Curva de temperatura promedio vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.T_mean,
            ylabel="Temperatura promedio",
            title="Temperatura promedio vs tiempo (centro caliente)",
            save_path="results/figuras/centro_caliente_Tmean_vs_t.png",
        )

        # Curva de temperatura máxima vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.T_max,
            ylabel="Temperatura máxima",
            title="Temperatura máxima vs tiempo (centro caliente)",
            save_path="results/figuras/centro_caliente_Tmax_vs_t.png",
        )

        # Curva de energía total vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.total_energy,
            ylabel="Energía total (sum(T))",
            title="Energía total vs tiempo (centro caliente)",
            save_path="results/figuras/centro_caliente_energy_vs_t.png",
        )

        plot_space_time_heatmap(
            snapshots,
            times,
            axis="y",
            index=cfg.nx // 2,
            title="Mapa tiempo–espacio (columna central, centro caliente)",
            save_path="results/figuras/centro_caliente_space_time_col_central.png",
        )

        animate_heatmap(
            times,
            snapshots,
            title_prefix="Escenario centro caliente",
            save_path="results/figuras/centro_caliente_anim.gif",
        )

def correr_escenario_puntos_aleatorios(num_puntos: int = 4, semilla: int | None = None):
    """
    Escenario 3:
    - Varios puntos calientes se colocan en posiciones aleatorias al inicio.
    - Bordes a 0°C.
    - Se observa cómo el calor se difunde y se disipa con el tiempo.

    num_puntos: cantidad de focos calientes aleatorios.
    semilla: si es None, los puntos cambian en cada ejecución;
             si se da un entero, la simulación es reproducible.
    """
    cfg = escenario_puntos_calientes_aleatorios()
    solver = HeatEquationSolver(cfg)

    nx, ny = solver.T.shape

    # Generador aleatorio
    if semilla is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(seed=semilla)

    # Parches en posiciones aleatorias
    patch_side = 5 # (5x5)
    half = patch_side // 2  # = 2

    for _ in range(num_puntos):
        # Elegimos centros suficientemente lejos de los bordes
        i = int(rng.integers(half, nx - half))
        j = int(rng.integers(half, ny - half))

        solver.T[i - half:i + half + 1, j - half:j + half + 1] = 100.0

    # Respetar condiciones de frontera (bordes a 0°C)
    solver._apply_boundary_conditions()

    # Correr simulación con snapshots para análisis y GIF
    times, snapshots = solver.run(store_every=10)

    if snapshots:
        T_final = snapshots[-1]
    else:
        T_final = solver.T

    # Guardar datos numéricos
    os.makedirs("results/datos", exist_ok=True)
    np.save("results/datos/T_final_puntos_aleatorios.npy", T_final)

    # Estadísticas al tiempo final
    stats = compute_stats(T_final, cfg, cfg.t_final)
    print_stats("Puntos calientes aleatorios", stats)

    # Heatmap final
    plot_heatmap(
        T_final,
        title=f"Escenario puntos calientes aleatorios (t = {cfg.t_final} s)",
        save_path="results/figuras/puntos_aleatorios_final.png",
    )

    # Series de tiempo y GIF
    if snapshots:
        ts_stats = compute_time_series_stats(times, snapshots)

        # Temperatura promedio vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.T_mean,
            ylabel="Temperatura promedio",
            title="Temperatura promedio vs tiempo (puntos aleatorios)",
            save_path="results/figuras/puntos_aleatorios_Tmean_vs_t.png",
        )

        # Energía total vs tiempo
        plot_time_series(
            ts_stats.times,
            ts_stats.total_energy,
            ylabel="Energía total (sum(T))",
            title="Energía total vs tiempo (puntos aleatorios)",
            save_path="results/figuras/puntos_aleatorios_energy_vs_t.png",
        )

        # GIF de la evolución
        animate_heatmap(
            times,
            snapshots,
            title_prefix="Escenario puntos calientes aleatorios",
            save_path="results/figuras/puntos_aleatorios_anim.gif",
        )

def main():
    """
    Ejecuta los escenarios definidos.
    """
    correr_escenario_borde_superior()
    correr_escenario_centro_caliente()
    correr_escenario_puntos_aleatorios() 

if __name__ == "__main__":
    main()
