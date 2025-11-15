# src/main.py

import os
import numpy as np

from .scenarios import (
    escenario_borde_superior_caliente,
    escenario_centro_caliente,
)
from .heat_equation import HeatEquationSolver
from .analysis import (
    compute_stats,
    print_stats,
    compute_time_series_stats,
)
from .visualize import plot_heatmap, animate_heatmap, plot_time_series


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

        animate_heatmap(
            times,
            snapshots,
            title_prefix="Escenario centro caliente",
            save_path="results/figuras/centro_caliente_anim.gif",
        )

def main():
    """
    Ejecuta los escenarios definidos.
    """
    correr_escenario_borde_superior()
    correr_escenario_centro_caliente()

if __name__ == "__main__":
    main()
