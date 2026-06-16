# Tablero de Autorizaciones — Relación de facturas con cierre

Dashboard interactivo (`tablero.html`) que **se enlaza con un Excel compartido en
OneDrive** y lo procesa en el navegador (con [SheetJS]). No tiene los datos
embebidos: descarga el archivo desde el enlace de OneDrive y arma indicadores,
gráficos y la tabla al vuelo.

## Conectar con OneDrive (paso a paso)

1. En OneDrive, abre el menú del archivo `.xlsx` → **Compartir** → **“Cualquiera
   con el enlace”** → **Copiar enlace**.
2. Abre `tablero.html`, pega el enlace en **“Conectar con los datos de OneDrive”**
   y pulsa **Conectar**. El enlace se **recuerda** en ese navegador, así que la
   próxima vez carga solo.
3. Usa **“Copiar enlace del tablero”** para obtener una URL del tablero con el
   enlace ya incluido (`...#data=...`) y compartirla con tu equipo.

> **Importante (cuentas empresariales / Microsoft 365):** por seguridad, el
> navegador suele **bloquear la descarga directa** desde OneDrive/SharePoint
> (política CORS). Si ocurre, el tablero muestra **“Abrir y descargar desde
> OneDrive”**: descarga el archivo y luego **arrástralo** al tablero (o usa
> “Seleccionar archivo…”). Es una limitación de Microsoft, no del tablero.

Si necesitas que la carga sea **automática y privada** (sin descargar a mano y
sin exponer datos), el camino robusto es conectarse con **inicio de sesión de
Microsoft (Microsoft Graph)**; requiere registrar una app en Azure. Puedo
implementarlo cuando quieras.

## Estructura esperada del Excel

La primera hoja debe tener estos encabezados (los mismos del archivo original):

`Fuente del documento`, `Nro de movimiento`, `Fecha movimiento`,
`Código Reponsable`, `tipo_ser`, `hc`, `Ingreso`, `cierre`, `Valor Documento`,
`Nombre del usuario`, `Primer Apellido del usuario`,
`Segundo Apellido del usuario` (las columnas `encusu` y `Fecha`, si existen, se
ignoran).

## Qué muestra

- **KPIs:** total de facturas, valor total, valor promedio, % cerradas, sin
  cierre y pacientes únicos (HC).
- **Gráficos** (Chart.js): tendencia diaria (facturas + valor), estado de cierre,
  valor por tipo de servicio, top 10 usuarios por n.º y por valor, facturas por
  fuente y top 10 responsables por valor.
- **Filtros** combinables y **tabla** paginada/ordenable con exportación a **CSV**.

> Requiere conexión a internet (Chart.js y SheetJS se cargan por CDN). Con
> **“Cargar otro archivo…”** puedes analizar cualquier Excel con esta estructura.

## Orden de carga de datos

1. Enlace embebido en la URL del tablero (`#data=…`).
2. Enlace de OneDrive recordado en el navegador.
3. Archivo de **ejemplo** del repositorio (`datos_tablero.xlsx`, anonimizado).
4. Conector manual (pegar enlace de OneDrive o arrastrar el archivo).

## Dónde abrir el tablero

- **Local:** descarga el repo y ejecuta `python3 -m http.server`; abre
  `http://localhost:8000/tablero.html`.
- **GitHub Pages:** Settings → Pages (workflow incluido en
  `.github/workflows/pages.yml`).
- **Doble clic:** abre `tablero.html` directamente y conéctate a OneDrive.

## Privacidad

El archivo de ejemplo del repositorio (`datos_tablero.xlsx`) está **anonimizado**
(sin `encusu`, con `hc` seudonimizada). Si conectas tu propio OneDrive, el tablero
usa tus datos tal cual: en ese caso mantén el archivo en OneDrive con permisos
adecuados y evita publicar datos sensibles en repos públicos.

## Archivos

| Archivo | Descripción |
|---|---|
| `tablero.html` | El dashboard. Se enlaza con el Excel de OneDrive. |
| `datos_tablero.xlsx` | Datos **anonimizados** de ejemplo / respaldo. |
| `anonimizar_excel.py` | Genera el Excel anonimizado a partir del original. |
| `.github/workflows/pages.yml` | Publica el tablero en GitHub Pages. |

[SheetJS]: https://sheetjs.com/
