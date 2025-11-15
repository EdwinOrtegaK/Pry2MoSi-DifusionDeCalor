# src/visualize.py

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

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

def animate_heatmap(times, snapshots, title_prefix: str = "", save_path: str | None = None):
    """
    Crea una animación simple de la evolución de la temperatura en la placa.

    Parámetros:
    - times: lista de tiempos
    - snapshots: lista de matrices T (np.ndarray) en esos tiempos
    - title_prefix: prefijo del título de la animación
    - save_path: si no es None, guarda la animación como GIF (usa Pillow).
    """
    if not snapshots:
        print("[WARN] No hay snapshots para animar.")
        return

    fig, ax = plt.subplots()
    im = ax.imshow(snapshots[0].T, origin="lower", aspect="equal")
    plt.colorbar(im, ax=ax, label="Temperatura")

    title = ax.set_title(f"{title_prefix} t = {times[0]:.2f} s")

    def update(frame):
        im.set_data(snapshots[frame].T)
        title.set_text(f"{title_prefix} t = {times[frame]:.2f} s")
        return im, title

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(snapshots),
        interval=100,
        blit=False,
    )

    if save_path is not None:
        # Guarda como GIF con Pillow
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        ani.save(save_path, writer="pillow", fps=10)
        plt.close(fig)
    else:
        plt.show()


def plot_time_series(times, values, ylabel: str, title: str, save_path: str | None = None):
    """
    Grafica una serie de tiempo sencilla (por ejemplo, temperatura media vs tiempo).
    """
    plt.figure()
    plt.plot(times, values)
    plt.xlabel("Tiempo (s)")
    plt.ylabel(ylabel)
    plt.title(title)

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()
