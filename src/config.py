# src/config.py

from dataclasses import dataclass

@dataclass
class SimulationConfig:
    # Discretización espacial
    nx: int              # número de nodos en x
    ny: int              # número de nodos en y
    Lx: float            # longitud de la placa en x (m)
    Ly: float            # longitud de la placa en y (m)

    # Propiedades físicas
    alpha: float         # difusividad térmica (m^2/s)

    # Discretización temporal
    dt: float            # paso de tiempo (s)
    t_final: float       # tiempo total de simulación (s)

    # Condiciones de frontera (Dirichlet constantes)
    T_left: float        # temperatura borde izquierdo
    T_right: float       # temperatura borde derecho
    T_top: float         # temperatura borde superior
    T_bottom: float      # temperatura borde inferior

    # Condición inicial (temperatura base de la placa)
    T_initial: float     # temperatura inicial en el interior