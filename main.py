import tkinter as tk
import subprocess

from playwright.sync_api import sync_playwright

from modules.registro_diario import (
    form_crear_base_registro_diario,
    form_download_registro_diario,
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
    ventana.geometry("300x600")
    ventana.title("Selector de Opciones")

    tk.Button(
        ventana,
        pady=4,
        text="Descargar Registro Diario",
        command=lambda: form_download_registro_diario(playwright),
    ).pack()

    tk.Button(
        ventana,
        pady=4,
        text="Re-Crear Base Registro Diario",
        command=lambda: form_crear_base_registro_diario(),
    ).pack()

    tk.Button(
        ventana,
        pady=4,
        text="Abrit Carpeta de Archivos Descargados",
        command=lambda: subprocess.Popen(f"explorer {DOWNLOADED_DIR}"),
    ).pack()

    tk.Label(ventana, text="Credenciales de Acceso").pack(pady=15)

    tk.Label(ventana, text="Usuario").pack()
    username_var = tk.StringVar()
    username_var.set(USERNAME)
    username = tk.Entry(ventana, width=30, textvariable=username_var).pack()
    tk.Label(ventana, text="Contraseña").pack()
    password_var = tk.StringVar()
    password_var.set(PASSWORD)
    password = tk.Entry(ventana, show="*", width=30, textvariable=password_var).pack()

    list_values = []

    tree_label = tk.Label(ventana, text="Seleccione Establecimientos Habilitados")
    tree_label.pack()
    tree = CheckboxTreeview(ventana)
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

    combo_label = tk.Label(ventana, text="Establecimiento Principal de Login")
    combo_label.pack()
    combo_box = AutocompleteCombobox(ventana, width=30, completevalues=list_values)
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
        ventana,
        pady=4,
        text="Guardar Credenciales",
        command=lambda: save_credentials(
            ventana, username_var, password_var, combo_box, tree
        ),
    ).pack()

    ventana.focus_set()
    ventana.mainloop()
    ventana.quit()
    exit()
