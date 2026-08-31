import re
from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
CARPETA_CSV = Path(__file__).resolve().parent.parent.parent / "data"  


def nombre_tabla_valido(nombre_archivo: str) -> str:
    """'olist_order_items_dataset.csv' -> 'order_items'"""
    nombre = nombre_archivo.replace(".csv", "").lower()
    nombre = nombre.replace("olist_", "").replace("_dataset", "")
    nombre = re.sub(r"[^a-z0-9]+", "_", nombre)
    return nombre.strip("_")


def main():
    engine = create_engine(DB_URL)
    archivos = sorted(CARPETA_CSV.glob("*.csv"))

    if not archivos:
        print(f"No se encontraron archivos .csv en {CARPETA_CSV.resolve()}")
        return

    print(f"Encontrados {len(archivos)} archivos .csv\n")

    for archivo in archivos:
        tabla = nombre_tabla_valido(archivo.name)
        print(f"Leyendo {archivo.name} -> tabla '{tabla}' ...")

        df = pd.read_csv(archivo)
        df.to_sql(tabla, engine, if_exists="replace", index=False)

        print(f"  {df.shape[0]} filas, {df.shape[1]} columnas cargadas.\n")

    print("Listo.", DB_URL)


if __name__ == "__main__":
    main()