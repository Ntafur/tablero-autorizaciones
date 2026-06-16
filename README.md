# Tablero de Autorizaciones — Relación de facturas con cierre

Dashboard interactivo (`tablero.html`) que **lee el Excel directamente desde
este repositorio** y lo procesa en el navegador (con [SheetJS]). No tiene los
datos embebidos: descarga `datos_tablero.xlsx` y arma los indicadores, gráficos
y la tabla al vuelo.

## ¿Qué muestra?

- **Indicadores (KPIs):** total de facturas, valor total, valor promedio,
  % cerradas, facturas sin cierre y pacientes únicos (HC).
- **Gráficos** (Chart.js): tendencia diaria (facturas + valor), estado de
  cierre, valor por tipo de servicio, top 10 usuarios por n.º y por valor,
  facturas por fuente y top 10 responsables por valor.
- **Filtros** combinables: fechas, estado de cierre, tipo, fuente, usuario y
  búsqueda libre (HC, movimiento, usuario, responsable).
- **Tabla de detalle** paginada y ordenable, con exportación a **CSV**.

## Cómo se enlaza con el Excel del repositorio

Al abrir `tablero.html`, intenta cargar el Excel en este orden:

1. **Ruta relativa** `datos_tablero.xlsx` — funciona cuando el HTML y el Excel
   se sirven juntos (GitHub Pages o un servidor local).
2. **URL cruda de GitHub** `raw.githubusercontent.com/.../main/datos_tablero.xlsx`
   — funciona incluso abriendo el HTML desde el disco, siempre que el repo sea
   **público**.
3. Si nada de lo anterior funciona (repo privado, sin internet), aparece un
   **cargador manual**: arrastrar y soltar, seleccionar archivo o pegar una URL.

> Requiere conexión a internet la primera vez (Chart.js y SheetJS se cargan por
> CDN). Con el botón **“Cargar otro archivo…”** puedes analizar otro Excel con
> la misma estructura sin tocar el código.

### Formas recomendadas de verlo

- **GitHub Pages:** Settings → Pages → Deploy from a branch. Luego abre
  `https://ntafur.github.io/tablero-autorizaciones/tablero.html`.
- **Local:** descarga el repo y ejecuta `python3 -m http.server` en la carpeta;
  abre `http://localhost:8000/tablero.html`.
- **Doble clic:** al abrir el archivo directamente, se carga desde la URL cruda
  de GitHub (repo público) o con el cargador manual.

## Privacidad de los datos

El Excel publicado (`datos_tablero.xlsx`) está **anonimizado**:

- Se eliminó la columna `encusu` (documento de identidad del usuario).
- Se eliminó la columna libre `Fecha` (no usada).
- La historia clínica `hc` está **seudonimizada** con un código irreversible
  (`P-xxxxxxxxxxxx`), de modo que se conserva el conteo de pacientes únicos sin
  exponer el número real.

El Excel original (con datos sensibles) **no se versiona** (ver `.gitignore`).

### Regenerar el Excel anonimizado

Requisitos: Python 3 y `openpyxl`.

```bash
pip install openpyxl
python3 anonimizar_excel.py archivo_original.xlsx datos_tablero.xlsx
```

Columnas esperadas en el Excel original: `Fuente del documento`,
`Nro de movimiento`, `Fecha movimiento`, `Código Reponsable`, `tipo_ser`,
`hc`, `Ingreso`, `Fecha`, `cierre`, `Valor Documento`, `encusu`,
`Nombre del usuario`, `Primer Apellido del usuario`,
`Segundo Apellido del usuario`.

## Archivos

| Archivo | Descripción |
|---|---|
| `tablero.html` | El dashboard. Lee el Excel desde el repositorio. |
| `datos_tablero.xlsx` | Datos **anonimizados** que consume el tablero. |
| `anonimizar_excel.py` | Genera el Excel anonimizado a partir del original. |

[SheetJS]: https://sheetjs.com/
