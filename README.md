# Tablero de Autorizaciones — Relación de facturas con cierre

Dashboard interactivo (un solo archivo HTML) para analizar la *relación de
facturas con cierre*. Se genera a partir de un archivo Excel y queda
**autocontenido**: los datos van embebidos, así que basta con abrir
`tablero.html` en cualquier navegador (doble clic), sin servidor ni
instalación.

## ¿Qué incluye?

- **Indicadores (KPIs):** total de facturas, valor total, valor promedio,
  % cerradas, facturas sin cierre y pacientes únicos (HC).
- **Gráficos** (Chart.js):
  - Facturas y valor por día (tendencia).
  - Estado de cierre (S / N / Sin cierre).
  - Valor por tipo de servicio.
  - Top 10 usuarios por n.º de facturas y por valor.
  - Facturas por fuente del documento.
  - Top 10 responsables por valor.
- **Filtros** combinables: rango de fechas, estado de cierre, tipo de
  servicio, fuente, usuario y búsqueda libre (HC, movimiento, usuario o
  responsable). Todo se recalcula al instante.
- **Tabla de detalle** paginada y ordenable, con **exportación a CSV** de la
  vista filtrada.

> Los gráficos usan Chart.js vía CDN (requiere conexión a internet la primera
> vez). Si no hay conexión, los KPIs, los filtros y la tabla siguen
> funcionando.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `tablero.html` | **El dashboard.** Ábrelo directamente en el navegador. |
| `generar_tablero.py` | Script que lee el Excel y genera `tablero.html`. |
| `plantilla.py` | Plantilla HTML/CSS/JS usada por el generador. |

## Regenerar el tablero con datos nuevos

Requisitos: Python 3 y `openpyxl`.

```bash
pip install openpyxl
python3 generar_tablero.py "ruta/al/archivo.xlsx" tablero.html
```

Si no se pasan argumentos, el script busca el Excel por su nombre por defecto
y escribe `tablero.html`.

### Columnas esperadas en el Excel

`Fuente del documento`, `Nro de movimiento`, `Fecha movimiento`,
`Código Reponsable`, `tipo_ser`, `hc`, `Ingreso`, `Fecha`, `cierre`,
`Valor Documento`, `encusu`, `Nombre del usuario`,
`Primer Apellido del usuario`, `Segundo Apellido del usuario`.

## Nota sobre datos sensibles

El archivo Excel de origen **no se versiona** en este repositorio (ver
`.gitignore`), ya que contiene identificadores como el documento del usuario
(`encusu`), que el tablero no necesita. El `tablero.html` generado sí incluye
los datos requeridos para el análisis (incluidos números de historia clínica
y nombres de usuarios). Trátalo como información interna.
