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

def plot_space_time_heatmap(
    snapshots,
    times,
    axis: str = "y",
    index: int | None = None,
    title: str = "",
    save_path: str | None = None,
):
    """
    Mapa de calor tiempo–espacio para una fila o columna fija de la placa.

    Parámetros:
    - snapshots: lista de matrices 2D (nx x ny) con la temperatura.
    - times: lista de tiempos correspondientes a cada snapshot.
    - axis:
        "y"  -> fija una COLUMNA y se ve cómo cambia a lo largo de y (vertical).
        "x"  -> fija una FILA y se ve cómo cambia a lo largo de x (horizontal).
    - index: índice de la fila/columna fija. Si es None, se usa el centro.
    - title: título de la figura.
    - save_path: ruta para guardar la imagen (opcional).
    """

    if len(snapshots) == 0:
        return  # nada que graficar

    # Apilamos en un solo array: (nt, nx, ny)
    data_3d = np.stack(snapshots, axis=0)  # shape (nt, nx, ny)
    nt, nx, ny = data_3d.shape

    # Elegimos fila/columna
    if axis == "y":
        # fijamos una columna i, variamos sobre j (vertical)
        if index is None:
            index = nx // 2
        space_profile = data_3d[:, index, :]   # shape (nt, ny)
        n_space = ny
        x_label = "Índice espacial (eje y)"
    else:
        # fijamos una fila j, variamos sobre i (horizontal)
        if index is None:
            index = ny // 2
        space_profile = data_3d[:, :, index]   # shape (nt, nx)
        n_space = nx
        x_label = "Índice espacial (eje x)"

    # Creamos el mapa tiempo–espacio
    plt.figure()
    im = plt.imshow(
        space_profile,
        origin="lower",
        aspect="auto",
        cmap="viridis",
        extent=[0, n_space - 1, times[0], times[-1]],
    )
    cbar = plt.colorbar(im)
    cbar.set_label("Temperatura")

    plt.xlabel(x_label)
    plt.ylabel("Tiempo (s)")
    if not title:
        title = "Mapa tiempo–espacio de temperatura"
    plt.title(title)

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()

