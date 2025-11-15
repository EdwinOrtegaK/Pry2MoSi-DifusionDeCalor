# src/scenarios.py

from .config import SimulationConfig

def escenario_borde_superior_caliente():
    """
    Escenario 1:
    - Placa 1m x 1m
    - Bordes izquierdo, derecho e inferior a 0°C
    - Borde superior a 100°C
    - Temperatura inicial interior 0°C
    """
    return SimulationConfig(
        nx=41,
        ny=41,
        Lx=1.0,
        Ly=1.0,
        alpha=1.0e-4,    # valor ejemplo
        dt=0.1,          # afinar luego con la condición de estabilidad
        t_final=50.0,
        T_left=0.0,
        T_right=0.0,
        T_top=100.0,
        T_bottom=0.0,
        T_initial=0.0,
    )

def escenario_centro_caliente():
    """
    Escenario 2:
    - Toda la placa a 0°C
    - Bordes a 0°C
    - Pero se podría calentar una región central al inicio (eso lo aplicamos
      directamente a la matriz T luego de crear el solver).
    """
    return SimulationConfig(
        nx=41,
        ny=41,
        Lx=1.0,
        Ly=1.0,
        alpha=1.0e-4,
        dt=0.1,
        t_final=50.0,
        T_left=0.0,
        T_right=0.0,
        T_top=0.0,
        T_bottom=0.0,
        T_initial=0.0,
    )