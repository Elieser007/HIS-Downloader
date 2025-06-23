import os
import time

from datetime import datetime

from variables import (
    LISTA_ESTABLECIMIENTOS_AVANZADO,
    DIR_REGISTRO_DIARIO_AVANZADO,
    DIR_PLANTILLA_REGISTRO_DIARIO_AVANZADO,
    REGISTRO_DIARIO_AVANZADO_BASE_SHEET_NAME,
    downloaded_dir_registro_diario_avanzado_with_start_end,
)

import tkinter as tk
from ttkwidgets import CheckboxTreeview, Calendar
from ttkwidgets.autocomplete import AutocompleteCombobox
from playwright.sync_api import Playwright
from openpyxl import load_workbook

from modules.generics import divide_range_in_days, login


def get_form_registro_diario_avanzado(page):
    page.frame_locator('frame[name="menuFrame"]').get_by_text(
        "Informe Avanzado"
    ).click()
    page.frame_locator('frame[name="menuFrame"]').get_by_role(
        "link", name="▾ Registro Diario de Consultas Region"
    ).click()


def registro_diario_avanzado_downloader(
    playwright: Playwright, startDate, endDate, seleccionados, diag_new, unify_base
):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://hisguaira.mspbs.gov.py/ambulatoria/")
    login(page)
    get_form_registro_diario_avanzado(page)
    date_range = divide_range_in_days(startDate, endDate)
    SAVE_AS_DOWNLOAD = downloaded_dir_registro_diario_avanzado_with_start_end(
        startDate, endDate
    )

    for selected in seleccionados:
        page.frame_locator('frame[name="mainFrame"]').locator(
            '//*[@id="form1"]/div/div[1]/div/span/span[1]/span/span[2]'
        ).click()
        time.sleep(1)
        page.frame_locator('frame[name="mainFrame"]').get_by_role(
            "option", name=selected, exact=True
        ).click()
        time.sleep(1)

        for date in date_range:
            page.frame_locator('frame[name="mainFrame"]').locator(
                'input[name="startDate"]'
            ).fill(date[0])
            page.frame_locator('frame[name="mainFrame"]').locator(
                'input[name="endDate"]'
            ).fill(date[1])
            if diag_new:
                page.frame_locator('frame[name="mainFrame"]').get_by_label("Si").nth(
                    1
                ).check()
            time.sleep(1)
            page.frame_locator('frame[name="mainFrame"]').get_by_role(
                "button", name="Generar"
            ).click()
            time.sleep(1)

            try:
                with page.expect_download(timeout=1200000) as download_info:
                    page.frame_locator('frame[name="mainFrame"]').locator(
                        "#form1"
                    ).get_by_role("img").click()
                download = download_info.value
            except:
                login(page)
                get_form_registro_diario_avanzado(page)
                page.frame_locator('frame[name="mainFrame"]').locator(
                    'input[name="startDate"]'
                ).fill(date[0])
                page.frame_locator('frame[name="mainFrame"]').locator(
                    'input[name="endDate"]'
                ).fill(date[1])
                if diag_new:
                    page.frame_locator('frame[name="mainFrame"]').get_by_label(
                        "Si"
                    ).nth(1).check()
                page.frame_locator('frame[name="mainFrame"]').get_by_role(
                    "button", name="Generar"
                ).click()
                time.sleep(1)
                with page.expect_download(timeout=1200000) as download_info:
                    page.frame_locator('frame[name="mainFrame"]').locator(
                        "#form1"
                    ).get_by_role("img").click()
                download = download_info.value

            download.save_as(SAVE_AS_DOWNLOAD + download.suggested_filename)
            time.sleep(3)

    context.close()
    browser.close()
    if unify_base:
        unify_base_registro_diario_avanzado(SAVE_AS_DOWNLOAD)


def form_download_registro_diario_avanzado(playwright):
    root = tk.Tk()
    root.geometry("600x500")
    root.title("Descargar Registro Diario Avanzado")
    global diag_new
    diag_new = False
    global unify_base
    unify_base = True
    # --- Configuración de columnas (opcional pero recomendado para control de redimensionamiento) ---
    root.grid_columnconfigure(0, weight=1)  # Columna 0 (izquierda) se expande
    root.grid_columnconfigure(1, weight=1)  # Columna 1 (derecha) se expande
    root.grid_rowconfigure(0, weight=1)  # Fila 0 se expande

    # --- Sección Izquierda ---
    frame_izquierda = tk.Frame(
        root,
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
        root,
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
        root,
        width=200,
        height=300,
        highlightbackground="gray",
        highlightthickness=1,
        pady=5
    )
    # grid(row, column) - colocamos el frame en la fila 1, columna 0,1
    frame_central.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    tree_label = tk.Label(frame_izquierda, text="Seleccione Establecimientos")
    tree_label.pack()
    tree = CheckboxTreeview(frame_izquierda)
    tree.insert("", "end", "todos", text="Seleccionar Todos")
    for dep in LISTA_ESTABLECIMIENTOS_AVANZADO:
        print(dep["departamento"])
        tree.insert(
            "todos",
            "end",
            f"dep_{dep['departamento']}",
            text=dep["departamento"],
        )
        for dist in dep["distritos"]:
            print(dist["distrito"])
            tree.insert(
                f"dep_{dep['departamento']}",
                "end",
                f"dist_{dist['distrito']}",
                text=dist["distrito"],
            )
            for est in dist['establecimientos']:
                print(est["text"])
                tree.insert(
                f"dist_{dist['distrito']}",
                "end",
                f"{dist['distrito']}_{est['text']}",
                text=est["text"],
            )

    tree.pack()

    def def_diag_new():
        global diag_new
        diag_new = not diag_new

    def def_unify_base():
        global unify_base
        unify_base = not unify_base

    v_d_new = tk.BooleanVar()
    d_new = tk.Checkbutton(
        frame_izquierda,
        text="¿Diagnostico Nuevo?",
        variable=v_d_new,
        onvalue=True,
        offvalue=False,
        command=def_diag_new,
    )
    d_new.pack()

    v_u_base = tk.BooleanVar()
    u_base = tk.Checkbutton(
        frame_izquierda,
        text="¿Unificar y crear Base después de descargar?",
        variable=v_u_base,
        onvalue=True,
        offvalue=False,
        command=def_unify_base,
    )
    u_base.pack()
    u_base.select()

    start_label = tk.Label(frame_derecha, text="Fecha de Inicio")
    start_label.pack()
    start_date = Calendar(
        frame_derecha,
        selectforeground="white",
        selectbackground="red",
        locale="es",
    )
    start_date.pack()

    end_label = tk.Label(frame_derecha, text="Fecha de Termino")
    end_label.pack()
    end_date = Calendar(
        frame_derecha,
        selectforeground="white",
        selectbackground="red",
        locale="es",
    )
    end_date.pack()

    tk.Button(
        frame_central,
        pady=2,
        text="Descargar Registro Diario",
        command=lambda: root.quit(),
    ).pack(pady=5)
    root.mainloop()
    seleccionados = tree.get_checked()
    start_selected = str(start_date.selection).split(" ")[0]
    end_selected = str(end_date.selection).split(" ")[0]
    registro_diario_avanzado_downloader(
        playwright, start_selected, end_selected, seleccionados, diag_new, unify_base
    )
    root.quit()


def form_crear_base_registro_diario_avanzado():
    root = tk.Tk()
    root.geometry("400x200")
    path_dir = os.scandir(DIR_REGISTRO_DIARIO_AVANZADO)
    list_values = []
    for path in path_dir:
        list_values.append(path.name)
    combo_label = tk.Label(root, text="Seleccione Carpeta de Archivos Descargados")
    combo_label.pack()
    combo_box = AutocompleteCombobox(root, width=60, completevalues=list_values)
    combo_box.pack()
    tk.Button(
        root,
        pady=2,
        text="Crear Base de Registro Diario Avanzado",
        command=lambda: root.quit(),
    ).pack(pady=5)
    root.mainloop()
    unify_base_registro_diario_avanzado(combo_box.get())
    root.quit()


def unify_base_registro_diario_avanzado(folder_selected):

    wb_base = load_workbook(DIR_PLANTILLA_REGISTRO_DIARIO_AVANZADO)
    ws_base = wb_base[REGISTRO_DIARIO_AVANZADO_BASE_SHEET_NAME]

    fila_insercion_base = 3

    ultimo_insertado = fila_insercion_base

    INFORME_REGISTRO_DIARIO_AVANZADO_SHEET_NAME = "reporte_registro_diario_consult"
    fila_copia_informe = 7

    column_number_format = [11]
    column_date_format = [1]

    files = os.scandir(os.path.join(DIR_REGISTRO_DIARIO_AVANZADO, folder_selected))
    desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    for file in files:
        wb = load_workbook(file.path)
        ws = wb[INFORME_REGISTRO_DIARIO_AVANZADO_SHEET_NAME]

        filas = ws[f"A{fila_copia_informe}" :f"BX{ws.max_row}"]

        for fila in filas:
            for celda in fila:
                if celda.column in column_number_format:
                    num_int = 0
                    try:
                        num_int = int(celda.value)
                    except ValueError:
                        num_int = celda.value
                    ws_base.cell(row=ultimo_insertado, column=celda.column).value = (
                        num_int
                    )
                elif celda.column in column_date_format:
                    date_format = None
                    try:
                        date_format = datetime.strptime(celda.value, "%Y-%m-%d").date()
                    except ValueError:
                        date_format = celda.value
                    ws_base.cell(row=ultimo_insertado, column=celda.column).value = (
                        date_format
                    )
                else:
                    ws_base.cell(row=ultimo_insertado, column=celda.column).value = (
                        celda.value
                    )

            ultimo_insertado = ultimo_insertado + 1

        wb.close()
    wb_base.save(
        os.path.join(
            desktop,
            f"Registro_Diario_Avanzado_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs.xlsx'))}",
        )
    )
    wb_base.close()
