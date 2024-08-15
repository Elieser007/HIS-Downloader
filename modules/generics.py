import time
import datetime

from variables import USERNAME, PASSWORD, ESTABLECIMIENTO_LOGIN


def divide_range_in_days(start_date: str, end_date: str):
    # example start_date='2023-03-22', end_date='2024-03-22'
    start = start_date.split("-")
    end = end_date.split("-")

    fecha_inicio = datetime.date(int(start[0]), int(start[1]), int(start[2]))
    fecha_fin = datetime.date(int(end[0]), int(end[1]), int(end[2]))

    intervalo_dias = 31
    lista_subrangos = []

    while fecha_inicio <= fecha_fin:
        fecha_siguiente = fecha_inicio + datetime.timedelta(days=intervalo_dias - 1)
        if fecha_siguiente > fecha_fin:
            fecha_siguiente = fecha_fin
        lista_subrangos.append(
            [fecha_inicio.strftime("%Y-%m-%d"), fecha_siguiente.strftime("%Y-%m-%d")]
        )
        fecha_inicio = fecha_siguiente + datetime.timedelta(days=1)

    return lista_subrangos


def login(page):
    page.get_by_placeholder("Usuario").click()
    page.get_by_placeholder("Usuario").fill(USERNAME)
    page.get_by_placeholder("Contraseña").click()
    page.get_by_placeholder("Contraseña").fill(PASSWORD)
    time.sleep(2)
    page.locator("i").click()
    page.get_by_role("searchbox").fill(ESTABLECIMIENTO_LOGIN)
    page.get_by_role("searchbox").press("Enter")
    time.sleep(1)
    page.get_by_role("button", name="Ingresar").click()


def logout(page):
    page.frame_locator('frame[name="mainFrame"]').get_by_role("link", name="").click()
    page.frame_locator('frame[name="mainFrame"]').get_by_role(
        "link", name=" Salir"
    ).click()
