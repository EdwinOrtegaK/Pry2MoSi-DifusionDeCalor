# src/scenarios.py

from .config import SimulationConfig

def escenario_borde_superior_caliente():
    """
    Escenario 1:
    - Placa 1m x 1m
    - Bordes izquierdo, derecho e inferior a 0°C
    - Borde superior a 100°C (fijo en el tiempo)
    - Temperatura inicial interior 0°C
    - Simulación larga para observar la difusión en el tiempo.
    """
    return SimulationConfig(
        nx=41,
        ny=41,
        Lx=1.0,
        Ly=1.0,
        alpha=1.0e-4,    # valor ejemplo
        dt=0.1,          # consistente con estabilidad
        t_final=2500.0,  # simulación larga
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
      directamente a la matriz T luego de crear el solver)
    """
    return SimulationConfig(
        nx=41,
        ny=41,
        Lx=1.0,
        Ly=1.0,
        alpha=1.0e-4,
        dt=0.1,
        t_final=300.0,
        T_left=0.0,
        T_right=0.0,
        T_top=0.0,
        T_bottom=0.0,
        T_initial=0.0,
    )

def escenario_puntos_calientes_aleatorios():
    """
    Escenario 3:
    - Bordes a 0°C
    - Temperatura inicial 0°C en toda la placa
    - Varios puntos calientes se colocan en posiciones aleatorias al inicio
    """
    return SimulationConfig(
        nx=41,
        ny=41,
        Lx=1.0,
        Ly=1.0,
        alpha=1.0e-4,
        dt=0.1,
        t_final=300.0,
        T_left=0.0,
        T_right=0.0,
        T_top=0.0,
        T_bottom=0.0,
        T_initial=0.0,
    )
