# src/visualize.py

import os
import numpy as np
import matplotlib.pyplot as plt

def plot_heatmap(T: np.ndarray, title: str = "", save_path: str | None = None):
    """
    Grafica un mapa de calor 2D de la matriz de temperatura T.

    Parámetros:
    - T: matriz 2D (nx x ny)
    - title: título de la figura
    - save_path: si no es None, guarda la figura en esa ruta.
    """
    plt.figure()
    plt.imshow(T.T, origin="lower", aspect="equal")
    plt.colorbar(label="Temperatura")
    plt.title(title)

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()