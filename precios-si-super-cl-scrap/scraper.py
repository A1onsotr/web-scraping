from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from datetime import datetime
import time
from curl_cffi import requests
import random
from pathlib import Path
import time, random


def limpiar_precio(txt):
    """'$3.990' -> 3990"""
    if not txt:
        return None
    digitos = re.sub(r"[^\d]", "", txt)
    return int(digitos) if digitos else None

def extraer_producto(soup):
    '''
    soup : html de la categoría de la i-esima pagina.
    '''
    fecha = datetime.now()  
    filas = []
    # Cada tarjeta: el div padre que contiene .plp_card
    for tarjeta in soup.select("div.pb-2.w-full"):
        if tarjeta.select_one("div.plp_card") is None:
            continue

        # --- Nombre y marca (h3 y p dentro del <a>) ---
        tag_nombre = tarjeta.select_one("h3")
        nombre = tag_nombre.get_text(" ", strip=True) if tag_nombre else None

        tag_marca = tarjeta.select_one("a p")
        marca = tag_marca.get_text(" ", strip=True) if tag_marca else None

        # --- Datos extra del JSON del <a> (opcional) ---
        categoria = sku = url = None
        tag_a = tarjeta.select_one("a[data-gtm-product-click]")
        if tag_a:
            url = tag_a.get("href")
            try:
                datos = json.loads(tag_a["data-gtm-product-click"])
                categoria = datos.get("category")
                sku = datos.get("refId")
            except json.JSONDecodeError:
                pass

        # --- Bloque de precio ---
        precio_actual = precio_antes = cantidad = precio_kg = None

        cp = tarjeta.select_one("div.items-baseline.font-bold")
        if cp:
            textos_directos = cp.find_all(string=True, recursive=False)
            precio_actual = limpiar_precio(" ".join(textos_directos))

            tag_tachado = cp.select_one("span.line-through")
            if tag_tachado:
                precio_antes = limpiar_precio(tag_tachado.get_text())

            for sp in cp.select("span.text-grey-dark"):
                if "line-through" not in sp.get("class", []):
                    cantidad = sp.get_text(" ", strip=True).replace("x", "", 1).strip()

        tag_kg = tarjeta.select_one("div.ppum-price-container span")
        if tag_kg:
            precio_kg = limpiar_precio(tag_kg.get_text())

        filas.append({
            "nombre": nombre,
            "marca": marca,
            "precio": precio_actual,
            "precio_antes": precio_antes,
            "cantidad": cantidad,
            "precio_x_kg": precio_kg,
            "categoria": categoria,
            "sku": sku,
            "url": url,
            "fecha": fecha.strftime("%Y-%m-%d"),
        })


    return filas


def extraccion_pagina(BASE_URL,categoria):
    sesion = requests.Session()          # fuera del while: se crea UNA vez
    filas_total = []
    pagina = 1

    while True:
        url = f"{BASE_URL}/{categoria}?page={pagina}"

        # --- Reintentos con espera creciente (reemplaza tu requests.get) ---
        resp = None
        for intento in range(3):
            try:
                resp = sesion.get(url, impersonate="chrome", timeout=15)
            except Exception as e:
                print(f"Página {pagina}, intento {intento + 1}: {e}")
                resp = None
            if resp is not None and resp.status_code == 200:
                break
            time.sleep(5 * (intento + 1))

        if resp is None or resp.status_code != 200:
            print(f"Página {pagina}: no se pudo descargar, termino.")
            break

        soup = BeautifulSoup(resp.text, "html.parser")

        filas = extraer_producto(soup)
        if not filas:
            break

        filas_total += filas
        print(f"Página {pagina}: {len(filas)} productos | acumulado: {len(filas_total)}")

        pagina += 1

        # --- Pausa variable entre páginas (al final de cada vuelta) ---
        time.sleep(random.uniform(1.5, 4))

    return filas_total


pd.set_option('display.max_columns', None)


DATA = Path("datos")

def guardar(filas, categoria, fecha):
    """
    Guarda las filas de una categoría en datos/<fecha>/<categoria>.parquet
    - Misma fecha y categoría: sobrescribe (sin duplicados).
    - Fecha nueva: crea carpeta nueva, el histórico no se toca.
    - filas vacías: no guarda nada y conserva el archivo anterior.
    Devuelve la ruta guardada, o None si no se guardó.
    """
    if not filas:
        print(f"{categoria}: sin datos, no se guarda")
        return None

    carpeta = DATA / fecha
    carpeta.mkdir(parents=True, exist_ok=True)

    destino = carpeta / f"{categoria}.parquet"
    tmp = carpeta / f"{categoria}.parquet.tmp"

    try:
        pd.DataFrame(filas).to_parquet(tmp, index=False)
        tmp.replace(destino)          # reemplazo atómico
    except Exception as e:
        print(f"{categoria}: error al guardar ({e})")
        if tmp.exists():
            tmp.unlink()              # limpia el temporal si algo falló
        return None

    print(f"{categoria}: {len(filas)} filas -> {destino}")
    return destino

from config import BASE_URL, CATEGORIAS

BASE_URL = BASE_URL
categorias = CATEGORIAS


fecha = datetime.now().strftime("%Y-%m-%d")   # una sola vez, antes del loop

random.shuffle(categorías)

for categoria in categorias:
    filas = extraccion_pagina(BASE_URL, categoria)   # debe DEVOLVER la lista de dicts
    guardar(filas, categoria, fecha)
    time.sleep(random.uniform(8, 20))
