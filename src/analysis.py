# src/analysis.py

from dataclasses import dataclass
from typing import List
import numpy as np
from .config import SimulationConfig

@dataclass
class SimulationStats:
    t_final: float
    T_min: float
    T_max: float
    T_mean: float
    total_energy: float  # suma de temperaturas como indicador global

def compute_stats(T: np.ndarray, cfg: SimulationConfig, t_final: float) -> SimulationStats:
    """
    Calcula métricas básicas de la temperatura en la placa.
    """
    T_min = float(T.min())
    T_max = float(T.max())
    T_mean = float(T.mean())
    total_energy = float(T.sum())

    return SimulationStats(
        t_final=t_final,
        T_min=T_min,
        T_max=T_max,
        T_mean=T_mean,
        total_energy=total_energy,
    )

def print_stats(label: str, stats: SimulationStats):
    """
    Imprime métricas de forma legible para el análisis.
    """
    print(f"\n=== Estadísticas del escenario: {label} ===")
    print(f"Tiempo final           : {stats.t_final:.2f} s")
    print(f"Temperatura mínima     : {stats.T_min:.4f}")
    print(f"Temperatura máxima     : {stats.T_max:.4f}")
    print(f"Temperatura promedio   : {stats.T_mean:.4f}")
    print(f"Energía total (sum(T)) : {stats.total_energy:.4f}")

@dataclass
class TimeSeriesStats:
    times: List[float]
    T_min: List[float]
    T_max: List[float]
    T_mean: List[float]
    total_energy: List[float]

def compute_time_series_stats(times, snapshots) -> TimeSeriesStats:
    """
    Calcula estadísticas para cada snapshot en el tiempo.
    """
    T_min_list: List[float] = []
    T_max_list: List[float] = []
    T_mean_list: List[float] = []
    energy_list: List[float] = []

    for T in snapshots:
        T_min_list.append(float(T.min()))
        T_max_list.append(float(T.max()))
        T_mean_list.append(float(T.mean()))
        energy_list.append(float(T.sum()))

    return TimeSeriesStats(
        times=list(times),
        T_min=T_min_list,
        T_max=T_max_list,
        T_mean=T_mean_list,
        total_energy=energy_list,
    )
