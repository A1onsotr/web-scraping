# Seguimiento de precios

Script en Python que recolecta precios públicos de un supermercado online chileno (SI)), para analizar cómo cambian los precios en el tiempo.

## Qué hace

- Recorre las categorías y sus páginas de productos.
- Extrae nombre, marca, precio, precio anterior, cantidad, precio por kg, SKU y URL.
- Guarda un archivo Parquet por día y categoría (`datos/AAAA-MM-DD/<categoria>.parquet`).
- Si una categoría no se descarga completa, no la guarda.

## Requisitos

- Python 3.10 o superior

```bash
pip install -r requirements.txt
```

## Uso

```bash
python scraper.py
```

Los datos quedan en la carpeta `datos/`, que no se incluye en el repositorio.

## Configuración

1. Copia la plantilla:
   ```bash
   cp config.example.py config.py
   ```
2. Edita `config.py` con la URL base del sitio y las categorías a recorrer.
3. Ejecuta `python scraper.py`.


## Ejemplo de lectura del histórico

```python
from pathlib import Path
import pandas as pd

archivos = Path("datos").glob("*/*.parquet")
df = pd.concat((pd.read_parquet(f) for f in archivos), ignore_index=True)
```

## Estructura de los datos

| Columna                   | Descripción                                    |
|---------------------------|------------------------------------------------|
| `fecha`                   | Día de la recolección                          |
| `nombre`, `marca`         | Producto y marca                               |
| `precio`, `precio_antes`  | Precio actual y precio tachado (si hay oferta) |
| `cantidad`, `precio_x_kg` | Formato y precio por kilo                      |
| `categoria`, `sku`, `url` | Categoría, código de referencia y enlace       |

## Uso responsable

Este proyecto es de carácter personal y educativo.

- Si el sitio te bloquea o te pide detenerte, detén el script.
- No se incluyen ni se redistribuyen los datos recolectados.

## Aviso

Proyecto independiente, sin relación con la empresa propietaria del sitio.
