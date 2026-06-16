#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Tablero de Autorizaciones.

Lee un archivo Excel con la "Relación de facturas con cierre" y produce un
archivo HTML autocontenido (tablero.html) con un dashboard interactivo:
KPIs, gráficos y tabla de detalle con filtros, todo del lado del navegador.

Uso:
    python3 generar_tablero.py [ruta_al_excel.xlsx] [salida.html]

Si no se pasan argumentos usa los valores por defecto definidos abajo.
"""
import sys
import os
import json
import datetime
from collections import OrderedDict

import openpyxl

# --------------------------------------------------------------------------
# Configuración por defecto
# --------------------------------------------------------------------------
DEFAULT_XLSX = "dcd6d21b-Vista_Cuadr_cula__relacion_de_facturas_con_cierre_07.xlsx"
DEFAULT_OUT = "tablero.html"

# Nombres de las columnas esperadas en el Excel
COL_FUENTE = "Fuente del documento"
COL_MOV = "Nro de movimiento"
COL_FECHA_MOV = "Fecha movimiento"
COL_RESP = "Código Reponsable"
COL_TIPO = "tipo_ser"
COL_HC = "hc"
COL_INGRESO = "Ingreso"
COL_FECHA = "Fecha"
COL_CIERRE = "cierre"
COL_VALOR = "Valor Documento"
COL_ENCUSU = "encusu"
COL_NOMBRE = "Nombre del usuario"
COL_AP1 = "Primer Apellido del usuario"
COL_AP2 = "Segundo Apellido del usuario"


def s(v):
    """Normaliza un valor a string limpio."""
    if v is None:
        return ""
    return str(v).strip()


def leer_excel(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    header = [s(h) for h in next(it)]
    idx = {h: i for i, h in enumerate(header)}

    faltantes = [c for c in (COL_FUENTE, COL_FECHA_MOV, COL_TIPO, COL_CIERRE,
                             COL_VALOR, COL_NOMBRE) if c not in idx]
    if faltantes:
        raise SystemExit("Faltan columnas en el Excel: %s\nEncontradas: %s"
                         % (faltantes, header))

    registros = []
    for r in it:
        if r is None:
            continue
        fm = r[idx[COL_FECHA_MOV]]
        if isinstance(fm, datetime.datetime):
            fecha = fm.date()
        elif isinstance(fm, datetime.date):
            fecha = fm
        else:
            fecha = None
        valor = r[idx[COL_VALOR]]
        try:
            valor = int(round(float(valor))) if valor not in (None, "") else 0
        except (TypeError, ValueError):
            valor = 0
        ingreso = r[idx[COL_INGRESO]] if COL_INGRESO in idx else None
        try:
            ingreso = int(ingreso) if ingreso not in (None, "") else None
        except (TypeError, ValueError):
            ingreso = None

        nombre = " ".join(p for p in (
            s(r[idx[COL_NOMBRE]]) if COL_NOMBRE in idx else "",
            s(r[idx[COL_AP1]]) if COL_AP1 in idx else "",
            s(r[idx[COL_AP2]]) if COL_AP2 in idx else "",
        ) if p).strip() or "(sin nombre)"

        registros.append({
            "fecha": fecha,
            "fuente": s(r[idx[COL_FUENTE]]) or "(sin fuente)",
            "tipo": s(r[idx[COL_TIPO]]) or "(sin tipo)",
            "cierre": s(r[idx[COL_CIERRE]]),
            "valor": valor,
            "resp": s(r[idx[COL_RESP]]) if COL_RESP in idx else "",
            "ingreso": ingreso,
            "usuario": nombre,
            "encusu": s(r[idx[COL_ENCUSU]]) if COL_ENCUSU in idx else "",
            "hc": s(r[idx[COL_HC]]) if COL_HC in idx else "",
            "mov": s(r[idx[COL_MOV]]) if COL_MOV in idx else "",
        })
    return registros


def construir_payload(registros):
    # Solo fechas válidas para definir el rango base
    fechas = [r["fecha"] for r in registros if r["fecha"] is not None]
    fecha_min = min(fechas) if fechas else datetime.date.today()
    fecha_max = max(fechas) if fechas else datetime.date.today()

    # Diccionarios para codificar strings repetidos (reduce tamaño del HTML)
    def dic():
        return OrderedDict()
    usuarios, responsables, fuentes, tipos = dic(), dic(), dic(), dic()
    cierres = OrderedDict([("S", 0), ("N", 1), ("Sin cierre", 2)])

    def idx_de(d, k):
        if k not in d:
            d[k] = len(d)
        return d[k]

    filas = []
    for r in registros:
        d = (r["fecha"] - fecha_min).days if r["fecha"] is not None else -1
        cierre_lbl = "S" if r["cierre"] == "S" else ("N" if r["cierre"] == "N" else "Sin cierre")
        filas.append([
            d,
            idx_de(fuentes, r["fuente"]),
            idx_de(tipos, r["tipo"]),
            cierres[cierre_lbl],
            r["valor"],
            idx_de(responsables, r["resp"]) if r["resp"] else -1,
            r["ingreso"] if r["ingreso"] is not None else -1,
            idx_de(usuarios, r["usuario"]),
            r["hc"],
            r["mov"],
        ])

    payload = {
        "meta": {
            "generado": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "fechaMin": fecha_min.isoformat(),
            "fechaMax": fecha_max.isoformat(),
            "totalFilas": len(filas),
        },
        "fechaBase": fecha_min.isoformat(),
        "dim": {
            "usuarios": list(usuarios.keys()),
            "responsables": list(responsables.keys()),
            "fuentes": list(fuentes.keys()),
            "tipos": list(tipos.keys()),
            "cierres": list(cierres.keys()),
        },
        # [d, fuenteIdx, tipoIdx, cierreIdx, valor, respIdx, ingreso, usuarioIdx, hc, mov]
        "rows": filas,
    }
    return payload


def main():
    xlsx = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_XLSX
    out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT
    if not os.path.exists(xlsx):
        raise SystemExit("No se encontró el Excel: %s" % xlsx)

    print("Leyendo %s ..." % xlsx)
    registros = leer_excel(xlsx)
    print("  %d registros leídos" % len(registros))

    payload = construir_payload(registros)
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # Evita que '</script>' dentro de los datos cierre el bloque <script>
    data_json = data_json.replace("</", "<\\/")

    html = PLANTILLA_HTML.replace("/*__DATA__*/", data_json)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    kb = os.path.getsize(out) / 1024
    print("Tablero generado: %s (%.0f KB)" % (out, kb))


# La plantilla HTML se importa desde plantilla.py para mantener este archivo legible.
from plantilla import PLANTILLA_HTML  # noqa: E402

if __name__ == "__main__":
    main()
