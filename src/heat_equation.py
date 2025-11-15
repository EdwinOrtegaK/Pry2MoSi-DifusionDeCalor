# src/heat_equation.py

import numpy as np
from .config import SimulationConfig

class HeatEquationSolver:
    def __init__(self, config: SimulationConfig):
        self.cfg = config

        # Discretización espacial
        self.dx = config.Lx / (config.nx - 1)
        self.dy = config.Ly / (config.ny - 1)

        # Coeficientes de estabilidad (r_x, r_y)
        self.r_x = config.alpha * config.dt / (self.dx ** 2)
        self.r_y = config.alpha * config.dt / (self.dy ** 2)

        # Matriz de temperatura T (nx x ny)
        self.T = np.full((config.nx, config.ny), config.T_initial, dtype=float)

        # Aplicar condiciones de frontera iniciales
        self._apply_boundary_conditions()

        # Verificación de estabilidad (simple, la afinamos después si hace falta)
        if self.r_x + self.r_y > 0.5:
            print("[ADVERTENCIA] r_x + r_y > 0.5, el esquema puede ser inestable.")

    def _apply_boundary_conditions(self):
        """Aplica las condiciones de frontera tipo Dirichlet constantes."""
        cfg = self.cfg

        # Bordes: asumimos que el índice 0 y -1 corresponden a las fronteras
        self.T[0, :]   = cfg.T_left    # borde izquierdo (x = 0)
        self.T[-1, :]  = cfg.T_right   # borde derecho (x = Lx)
        self.T[:, 0]   = cfg.T_bottom  # borde inferior (y = 0)
        self.T[:, -1]  = cfg.T_top     # borde superior (y = Ly)

    def step(self):
        """
        Realiza un paso de tiempo usando el esquema explícito:

        T_{i,j}^{n+1} = T_{i,j}^n
                        + r_x (T_{i+1,j}^n + T_{i-1,j}^n - 2 T_{i,j}^n)
                        + r_y (T_{i,j+1}^n + T_{i,j-1}^n - 2 T_{i,j}^n)
        """

        T_new = self.T.copy()
        nx, ny = self.T.shape

        # Actualizar solo nodos interiores (sin tocar bordes)
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                T_ij = self.T[i, j]
                T_ip1 = self.T[i + 1, j]
                T_im1 = self.T[i - 1, j]
                T_jp1 = self.T[i, j + 1]
                T_jm1 = self.T[i, j - 1]

                T_new[i, j] = (
                    T_ij
                    + self.r_x * (T_ip1 + T_im1 - 2.0 * T_ij)
                    + self.r_y * (T_jp1 + T_jm1 - 2.0 * T_ij)
                )

        self.T = T_new
        self._apply_boundary_conditions()

    def run(self, store_every: int = 0):
        """
        Ejecuta la simulación completa desde t=0 hasta t_final.

        Parámetros:
        - store_every: si > 0, almacena la matriz T cada 'store_every' pasos.

        Retorna:
        - times: lista de tiempos almacenados
        - snapshots: lista de matrices T (np.array) correspondientes a esos tiempos
        """
        cfg = self.cfg
        n_steps = int(cfg.t_final / cfg.dt)

        times = []
        snapshots = []

        t = 0.0
        for step in range(n_steps):
            self.step()
            t += cfg.dt

            if store_every > 0 and step % store_every == 0:
                times.append(t)
                snapshots.append(self.T.copy())

        return times, snapshots