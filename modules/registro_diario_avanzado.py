import os
import time
import locale

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
from openpyxl.utils import column_index_from_string
import pandas as pd

from modules.generics import divide_range_in_days, login, get_desktop_path


def get_form_registro_diario_avanzado(page):
    page.frame_locator('frame[name="menuFrame"]').get_by_text(
        "Informe Avanzado"
    ).click()
    page.frame_locator('frame[name="menuFrame"]').get_by_role(
        "link", name="▾ Registro Diario de Consultas Region"
    ).click()


def get_establecimientos(seleccionados, establecimientos, distrito):
    ESTABLECIMIENTOS_SELECCIONADOS = []
    TOTAL_ESTABLECIMIENTOS = len(establecimientos)
    for est in establecimientos:
        if f"{distrito}_{est['text']}" in seleccionados:
            ESTABLECIMIENTOS_SELECCIONADOS.append(est)
    if len(ESTABLECIMIENTOS_SELECCIONADOS) == TOTAL_ESTABLECIMIENTOS:
        return True
    if len(ESTABLECIMIENTOS_SELECCIONADOS) == 0:
        return False
    return ESTABLECIMIENTOS_SELECCIONADOS


def get_selected_data(seleccionados):
    # Variable para almacenar los departamentos y distritos seleccionados
    # y los establecimientos seleccionados
    SELECTED = []
    # Iteramos sobre la lista de establecimientos avanzados
    for dep in LISTA_ESTABLECIMIENTOS_AVANZADO:
        # Inicializamos la lista de departamentos y distritos seleccionados
        DISTRITO = []
        # Inicializamos la variable para saber si se seleccionaron todos los
        # establecimientos de un distrito empezamos con True
        ALL_DISTRITO = True
        # Iteramos sobre los distritos de cada departamento
        for dist in dep["distritos"]:
            # Obtenemos los el estado de los establecimientos seleccionados
            # True si se seleccionaron todos
            # False si no se seleccionó ninguno
            # Lista de establecimientos seleccionados si se seleccionaron algunos
            status = get_establecimientos(
                seleccionados, dist["establecimientos"], dist["distrito"]
            )
            # Si el estado es True, significa que se seleccionaron todos establecimientos
            if status is True:
                # Agregamos el distrito que están seleccionado con todos los
                # establecimientos
                DISTRITO.append(
                    {"distrito": dist["distrito"], "establecimientos": "ALL"}
                )
            # Si el estado es False, significa que no se seleccionó ningún establecimiento
            elif status is False:
                # Cambiamos la variable ALL_DISTRITO a False
                # si pasa una vez por esta condición ya se queda en False para este distrito
                ALL_DISTRITO = False
                # y no se agrega el distrito a la lista de distritos seleccionados
                continue
            # Si el estado es una lista, significa que se seleccionaron algunos establecimientos
            else:
                # Cambiamos la variable ALL_DISTRITO a False
                # si pasa una vez por esta condición ya se queda en False para este distrito
                ALL_DISTRITO = False
                # y SI se agrega el distrito la lista y sus establecimientos seleccionados
                DISTRITO.append(
                    {
                        "distrito": dist["distrito"],
                        "establecimientos": [est["text"] for est in status],
                    }
                )
        # Agregamos el departamento y sus distritos seleccionados a la lista de SELECTED
        SELECTED.append(
            {
                "departamento": dep["departamento"],
                # Si ALL_DISTRITO es True, significa que se seleccionaron todos los distritos sino se agrega la lista de distritos seleccionados
                "distritos": "ALL" if ALL_DISTRITO else DISTRITO,
            }
        )
    return SELECTED


def select_departamento(page, departamento):
    time.sleep(1)
    page.locator('frame[name="mainFrame"]').content_frame.locator(
        "#reporte_codigo_departamento"
    ).select_option(departamento)
    time.sleep(1)


def select_distrito(page, distrito):
    time.sleep(1)
    page.locator('frame[name="mainFrame"]').content_frame.locator(
        "#reporte_codigo_distrito"
    ).select_option(distrito)
    time.sleep(1)


def select_establecimiento(page, establecimiento):
    time.sleep(1)
    page.locator('frame[name="mainFrame"]').content_frame.locator(
        "#reporte_codigo_establecimiento"
    ).select_option(establecimiento)
    time.sleep(1)


def download_loop(page, date_range, diag_new, SAVE_AS_DOWNLOAD):
    # Recorremos el rango de fechas
    for date in date_range:
        # Asignamos la fecha de inicio
        page.locator('frame[name="mainFrame"]').content_frame.locator(
            'input[name="startDate"]'
        ).fill(date[0])
        # Asignamos la fecha de fin
        page.locator('frame[name="mainFrame"]').content_frame.locator(
            'input[name="endDate"]'
        ).fill(date[1])
        # si diagnostico nuevo se seleccionó
        if diag_new:
            # seleccionamos el radio button de diagnostico nuevo
            page.locator('frame[name="mainFrame"]').content_frame.get_by_role(
                "radio", name="Si"
            ).nth(1).check()
        time.sleep(1)
        print("--------------------------------------------------")
        print("Fechas=" + date[0] + " - " + date[1])
        print("--------------------------------------------------")

        # Hacemos click en el botón de generar
        page.locator('frame[name="mainFrame"]').content_frame.get_by_role(
            "button", name="Generar"
        ).click()
        time.sleep(1)
        # Activamos la espera de descarga
        with page.expect_download(timeout=1200000) as download_info:
            # Hacemos click en el botón de descargar
            page.frame_locator('frame[name="mainFrame"]').locator("#form1").get_by_role(
                "img"
            ).click()
        # Obtenemos la información de la descarga
        download = download_info.value
        # Guardamos el archivo descargado en la carpeta especificada
        download.save_as(SAVE_AS_DOWNLOAD + download.suggested_filename)
        time.sleep(3)


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
    SELECTED = get_selected_data(seleccionados)

    # Empezamos a recorrer la lista de SELECTED
    for selected in SELECTED:
        if selected["distritos"] == "ALL":
            select_departamento(page, selected["departamento"])
            print("Seleccionamos solo el departamento:", selected["departamento"])
            time.sleep(1)
            download_loop(page, date_range, diag_new, SAVE_AS_DOWNLOAD)
        elif isinstance(selected["distritos"], list):
            for dist in selected["distritos"]:
                select_departamento(page, selected["departamento"])
                if dist["establecimientos"] == "ALL":
                    select_distrito(page, dist["distrito"])
                    print("Seleccionamos solo el distrito", dist["distrito"])
                    download_loop(page, date_range, diag_new, SAVE_AS_DOWNLOAD)
                else:
                    for est in dist["establecimientos"]:
                        select_distrito(page, dist["distrito"])
                        select_establecimiento(page, est)
                        print("Seleccionamos el establecimiento", est)
                        download_loop(page, date_range, diag_new, SAVE_AS_DOWNLOAD)

    context.close()
    browser.close()
    if unify_base:
        unify_base_registro_diario_avanzado(SAVE_AS_DOWNLOAD)


def form_download_registro_diario_avanzado(playwright):
    root = tk.Tk()
    root.geometry("700x500")
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
        pady=5,
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
        pady=5,
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
        pady=5,
    )
    # grid(row, column) - colocamos el frame en la fila 1, columna 0,1
    frame_central.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
    tree_label = tk.Label(frame_izquierda, text="Seleccione Establecimientos")
    tree_label.pack()
    tree = CheckboxTreeview(frame_izquierda)
    tree.insert("", "end", "todos", text="Seleccionar Todos")
    for dep in LISTA_ESTABLECIMIENTOS_AVANZADO:
        tree.insert(
            "todos",
            "end",
            f"dep_{dep['departamento']}",
            text=dep["departamento"],
        )
        for dist in dep["distritos"]:
            tree.insert(
                f"dep_{dep['departamento']}",
                "end",
                f"dist_{dist['distrito']}",
                text=dist["distrito"],
            )
            for est in dist["establecimientos"]:
                tree.insert(
                    f"dist_{dist['distrito']}",
                    "end",
                    f"{dist['distrito']}_{est['text']}",
                    text=est["text"],
                )

    tree.pack(ipadx=35,ipady=50)

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
        locale=locale.getdefaultlocale()[0] or "es",
    )
    start_date.pack()

    end_label = tk.Label(frame_derecha, text="Fecha de Termino")
    end_label.pack()
    end_date = Calendar(
        frame_derecha,
        selectforeground="white",
        selectbackground="red",
        locale=locale.getdefaultlocale()[0] or "es",
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


def resize_excel_table(wb, ws, table_name, last_row):
    """
    Redimensiona una tabla de Excel en memoria usando openpyxl.
    
    Argumentos:
        wb: Workbook de openpyxl.
        ws: Worksheet de openpyxl.
        table_name (str): Nombre de la tabla a redimensionar.
        last_row (int): La nueva fila final para la tabla.
    """
    try:
        table = None
        for tbl in ws.tables.values():
            if tbl.name == table_name:
                table = tbl
                break
        
        if table is None:
            raise ValueError(f"Tabla '{table_name}' no encontrada en la hoja '{ws.title}'")
        
        # Parse referencia actual de la tabla, ej: "A1:Z10"
        ref_parts = table.ref.split(':')
        start_cell = ws[ref_parts[0]]
        end_cell = ws[ref_parts[1]]
        
        # Nueva celda final: misma columna, nueva última fila
        new_end_cell = ws.cell(row=last_row, column=end_cell.column)
        
        # Construir nueva referencia
        new_ref = f"{start_cell.coordinate}:{new_end_cell.coordinate}"
        
        # Actualizar referencia de la tabla
        table.ref = new_ref
        
        print(f"La tabla '{table_name}' ha sido redimensionada con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al redimensionar la tabla: {e}")

def unify_base_registro_diario_avanzado(folder_selected):
    """Unifica y optimiza archivos de Registro Diario Avanzado usando pandas y openpyxl."""
    wb_base = load_workbook(DIR_PLANTILLA_REGISTRO_DIARIO_AVANZADO, keep_vba=True)
    ws_base = wb_base[REGISTRO_DIARIO_AVANZADO_BASE_SHEET_NAME]

    fila_insercion_base = 3
    INFORME_REGISTRO_DIARIO_AVANZADO_SHEET_NAME = "reporte_registro_diario_consult"
    fila_copia_informe = 7

    column_number_format = [11]
    column_date_format = [1]
    column_with_formula = ["BL"]  # Lista de letras de columnas que contienen fórmulas
    
    REGISTRO_DIARIO_AVANZADO_TABLE_NAME = "BASE"

    files = sorted(os.scandir(os.path.join(DIR_REGISTRO_DIARIO_AVANZADO, folder_selected)),
                   key=lambda f: f.name)
    desktop = get_desktop_path()
    
    ultimo_insertado = fila_insercion_base
    all_dfs = []
    
    for file in files:
        try:
            # Lectura con pandas para mejor performance
            df = pd.read_excel(
                file.path,
                sheet_name=INFORME_REGISTRO_DIARIO_AVANZADO_SHEET_NAME,
                skiprows=fila_copia_informe - 1
            )
            
            # Convertir a tipos apropiados
            df = df.astype(object)
            
            # Formatear columnas numéricas
            for col in column_number_format:
                if col <= len(df.columns):
                    df.iloc[:, col - 1] = pd.to_numeric(
                        df.iloc[:, col - 1], errors='coerce'
                    ).fillna(0).astype(int)
            
            # Formatear columnas de fecha
            for col in column_date_format:
                if col <= len(df.columns):
                    df.iloc[:, col - 1] = pd.to_datetime(
                        df.iloc[:, col - 1], errors='coerce'
                    ).dt.date
            
            if not df.empty:
                all_dfs.append(df)
                
        except Exception as e:
            print(f"Error procesando archivo {file.name}: {e}")
            continue
    
    if all_dfs:
        df_total = pd.concat(all_dfs, ignore_index=True)
        
        duplicate_counts = (
            df_total.groupby(list(df_total.columns), dropna=False)
            .size()
            .reset_index(name="count")
        )
        duplicate_exact = duplicate_counts[duplicate_counts["count"] > 1]
        if not duplicate_exact.empty:
            key_positions = [0, 3, 5, 7]
            key_columns = [
                df_total.columns[pos]
                for pos in key_positions
                if pos < len(df_total.columns)
            ]
            print("Duplicados exactos detectados en todos los archivos:")
            print(
                duplicate_exact[
                    [*key_columns, "count"]
                ].to_string(index=False)
            )
            print(
                "Estos registros tienen todas las columnas iguales y aparecen más de una vez. "
                "Solo se guardará una copia de cada uno en el archivo final."
            )
        
        # Mantener solo una copia de cada fila duplicada exacta
        df_total = df_total.drop_duplicates(keep="first")
        
        # Insertar datos en el workbook (sin incluir columnas con fórmulas)
        for _, row in df_total.iterrows():
            for col_idx, value in enumerate(row, start=1):
                ws_base.cell(row=ultimo_insertado, column=col_idx).value = value
            ultimo_insertado += 1
    else:
        print("No se encontraron datos para procesar en la carpeta seleccionada.")
    
    # Extender fórmulas a las nuevas filas en las columnas especificadas
    for col_letter in column_with_formula:
        col_num = column_index_from_string(col_letter)
        reference_formula = ws_base.cell(row=fila_insercion_base, column=col_num).value
        if reference_formula and isinstance(reference_formula, str) and reference_formula.startswith('='):
            for row in range(fila_insercion_base + 1, ultimo_insertado):
                ws_base.cell(row=row, column=col_num).value = reference_formula
    
    # Guardamos el archivo con los nuevos datos
    file_path_output = os.path.join(
        desktop,
        f"Registro_Diario_Avanzado_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}.xlsm",
    )
    wb_base.save(file_path_output)
    
    # Redimensionar la tabla SOLO si hay al menos una fila de datos
    final_data_row = ultimo_insertado - 1
    if final_data_row >= 3:  # El encabezado está en la fila 2, los datos en la 3 en adelante
        resize_excel_table(
            wb=wb_base,
            ws=ws_base,
            table_name=REGISTRO_DIARIO_AVANZADO_TABLE_NAME,
            last_row=final_data_row
        )
        wb_base.save(file_path_output)
    
    wb_base.close()
    print(f"Archivo guardado en: {file_path_output}")