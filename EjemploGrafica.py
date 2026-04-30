import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import mplcursors


def window_creation():
    window = tk.Tk()
    window.title("Keithley - gráfica interactiva")
    window.geometry("1000x650")

    # -----------------------------
    # Frame para la gráfica
    # -----------------------------
    frame_grafica = tk.LabelFrame(window, text="Gráfica interactiva")
    frame_grafica.place(x=20, y=20, width=950, height=580)

    # -----------------------------
    # Etiqueta para mostrar valores seleccionados
    # -----------------------------
    lbl_info = tk.Label(window, text="Selecciona un punto para ver sus valores", anchor="w")
    lbl_info.place(x=20, y=610, width=950)

    # -----------------------------
    # Crear figura
    # -----------------------------
    fig = Figure(figsize=(8, 4.8), dpi=100)
    ax = fig.add_subplot(111)

    ax.set_title("Curva I-V")
    ax.set_xlabel("Voltaje (V)")
    ax.set_ylabel("Corriente (A)")
    ax.grid(True)

    # Datos de ejemplo
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [0, 0.08, 0.22, 0.55, 0.95, 1.50, 2.10]

    # Dibujar línea y puntos
    line, = ax.plot(x, y, marker="o", linewidth=1.5)

    # -----------------------------
    # Canvas en tkinter
    # -----------------------------
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # -----------------------------
    # Barra de navegación interactiva
    # -----------------------------
    toolbar = NavigationToolbar2Tk(canvas, frame_grafica)
    toolbar.update()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # -----------------------------
    # Cursor interactivo para ver valores
    # -----------------------------
    cursor = mplcursors.cursor(line, hover=False)

    @cursor.connect("add")
    def on_add(sel):
        x_sel, y_sel = sel.target
        texto = f"x = {x_sel:.4f}\ny = {y_sel:.4f}"
        sel.annotation.set_text(texto)
        lbl_info.config(text=f"Punto seleccionado -> x = {x_sel:.4f}, y = {y_sel:.4f}")

    window.mainloop()


window_creation()