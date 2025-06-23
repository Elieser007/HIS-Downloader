import tkinter as tk
import subprocess

from playwright.sync_api import sync_playwright

from modules.registro_diario import (
    form_crear_base_registro_diario,
    form_download_registro_diario,
)
from modules.registro_diario_avanzado import (
    form_crear_base_registro_diario_avanzado,
    form_download_registro_diario_avanzado,
)

from variables import (
    USERNAME,
    PASSWORD,
    ESTABLECIMIENTO_LOGIN,
    ESTABLECIMIENTOS,
    LISTA_ESTABLECIMIENTOS,
    CREDENTIALS_FILE_NAME,
    DOWNLOADED_DIR,
)
import json
from ttkwidgets import CheckboxTreeview
from ttkwidgets.autocomplete import AutocompleteCombobox


with sync_playwright() as playwright:
    ventana = tk.Tk()
    ventana.geometry("600x700")
    ventana.title("Selector de Opciones")
    # --- Configuración de columnas (opcional pero recomendado para control de redimensionamiento) ---
    ventana.grid_columnconfigure(0, weight=1)  # Columna 0 (izquierda) se expande
    ventana.grid_columnconfigure(1, weight=1)  # Columna 1 (derecha) se expande
    ventana.grid_rowconfigure(0, weight=1)  # Fila 0 se expande

    # --- Sección Izquierda ---
    frame_izquierda = tk.Frame(
        ventana,
        width=200,
        height=300,
        highlightbackground="gray",
        highlightthickness=1,
        pady=5
    )
    # grid(row, column) - colocamos el frame en la fila 0, columna 0
    frame_izquierda.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

    # --- Sección Derecha ---
    frame_derecha = tk.Frame(
        ventana,
        width=200,
        height=300,
        highlightbackground="gray",
        highlightthickness=1,
        pady=5
    )
    # grid(row, column) - colocamos el frame en la fila 0, columna 1
    frame_derecha.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

    # --- Sección Central ---
    frame_central = tk.Frame(
        ventana,
        width=200,
        height=300,
        highlightbackground="gray",
        highlightthickness=1,
        pady=5
    )
    # grid(row, column) - colocamos el frame en la fila 1, columna 0,1
    frame_central.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    tk.Label(frame_izquierda, text="Opciones de Descarga Normal").pack()

    tk.Label(
        frame_izquierda,
        text="⚠️Importante!!!\nEl HIS solo habilita 5 registros diarios por mes\ndesde junio del 2025, si hace ENOS\nsolo podra hacer 5 en 1 mes, se\nle recomienda solo usarlo cada semana hasta\nque se encuentre una solución.",
        background="red",
        foreground="white",
    ).pack()

    tk.Button(
        frame_izquierda,
        pady=4,
        text="Descargar Registro Diario",
        command=lambda: form_download_registro_diario(playwright),
    ).pack()

    tk.Button(
        frame_izquierda,
        pady=4,
        text="Re-Crear Base Registro Diario",
        command=lambda: form_crear_base_registro_diario(),
    ).pack()
    tk.Label(frame_derecha, text="Opciones de Descarga Avanzada").pack()

    tk.Button(
        frame_derecha,
        pady=4,
        text="Descargar Registro Diario Avanzado",
        command=lambda: form_download_registro_diario_avanzado(playwright),
    ).pack()

    tk.Button(
        frame_derecha,
        pady=4,
        text="Re-Crear Base Registro Diario Avanzado",
        command=lambda: form_crear_base_registro_diario_avanzado(),
    ).pack()

    tk.Button(
        frame_central,
        pady=4,
        text="Abrir Carpeta de Archivos Descargados",
        command=lambda: subprocess.Popen(f"explorer {DOWNLOADED_DIR}"),
    ).pack()
    tk.Label(frame_central, text="Credenciales de Acceso").pack(pady=15)

    tk.Label(frame_central, text="Usuario").pack()
    username_var = tk.StringVar()
    username_var.set(USERNAME)
    username = tk.Entry(frame_central, width=30, textvariable=username_var).pack()
    tk.Label(frame_central, text="Contraseña").pack()
    password_var = tk.StringVar()
    password_var.set(PASSWORD)
    password = tk.Entry(
        frame_central, show="*", width=30, textvariable=password_var
    ).pack()

    list_values = []

    tree_label = tk.Label(frame_central, text="Seleccione Establecimientos Habilitados")
    tree_label.pack()
    tree = CheckboxTreeview(frame_central)
    tree.insert("", "end", "todos", text="Seleccionar Todos")
    for est in LISTA_ESTABLECIMIENTOS:
        list_values.append(est["nombre_establecimiento"])
        tree.insert(
            "todos",
            "end",
            est["nombre_establecimiento"],
            text=est["nombre_establecimiento"],
        )
    tree.pack()

    if len(ESTABLECIMIENTOS) == len(LISTA_ESTABLECIMIENTOS):
        tree.change_state("todos", state="checked")
    elif (
        len(ESTABLECIMIENTOS) < len(LISTA_ESTABLECIMIENTOS)
        and len(ESTABLECIMIENTOS) > 0
    ):
        tree.change_state("todos", state="tristate")
    else:
        tree.change_state("todos", state="unchecked")

    for est in ESTABLECIMIENTOS:
        tree.change_state(est, state="checked")

    combo_label = tk.Label(frame_central, text="Establecimiento Principal de Login")
    combo_label.pack()
    combo_box = AutocompleteCombobox(
        frame_central, width=30, completevalues=list_values
    )
    combo_box.set(ESTABLECIMIENTO_LOGIN)
    combo_box.pack()

    def save_credentials(ventana, username_var, password_var, combo_box, tree):
        with open(CREDENTIALS_FILE_NAME, "w") as f:
            json.dump(
                {
                    "username": username_var.get(),
                    "password": password_var.get(),
                    "establecimiento_login": combo_box.get(),
                    "establecimientos": tree.get_checked(),
                },
                f,
            )
        ventana.destroy()
        tk.messagebox.showinfo(
            "Guardado",
            "Credenciales guardadas con éxito, vuelva a ejecutar el programa",
        )
        exit()

    tk.Button(
        frame_central,
        pady=4,
        text="Guardar Credenciales",
        command=lambda: save_credentials(
            frame_central, username_var, password_var, combo_box, tree
        ),
    ).pack()

    ventana.focus_set()
    ventana.mainloop()
    ventana.quit()
    exit()
