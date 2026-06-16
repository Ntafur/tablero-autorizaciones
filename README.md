# Tablero de Autorizaciones — Relación de facturas con cierre

Dashboard interactivo (`tablero.html`) que lee el Excel **anonimizado** desde
este repositorio **privado** y lo procesa en el navegador (con [SheetJS]).
La lectura se hace con la **API de contenidos de GitHub** usando un **token de
solo lectura que cada usuario pega una vez** (no hay secretos dentro del
archivo). Funciona incluso abriendo `tablero.html` con doble clic, porque la
API de GitHub permite CORS.

## Puesta en marcha (una sola vez)

### 1) Hacer el repositorio privado
En GitHub: **Settings → General → Danger Zone → Change repository visibility →
Make private**. (El Excel publicado ya está anonimizado; ver más abajo.)

### 2) Crear un token de solo lectura (fino)
En **https://github.com/settings/personal-access-tokens/new**:
- **Resource owner:** Ntafur
- **Repository access:** *Only select repositories* → `tablero-autorizaciones`
- **Permissions → Repository permissions → Contents:** **Read-only**
- *Generate token* y **copia** el valor (`github_pat_…`).

> Cada persona que use el tablero necesita: (a) ser **colaboradora** del repo
> privado y (b) **su propio** token. El token se guarda **solo en su navegador**.

### 3) Conectar
Abre `tablero.html`, pega el token en **“Conectar con el repositorio privado”**
y pulsa **Conectar**. Queda recordado; la próxima vez carga solo. Desde la barra
superior puedes **reconectar** con otro token o **“Olvidar token”**.

## Orden de carga de datos

1. Token de GitHub recordado en el navegador → API privada del repo.
2. Archivo en el **mismo origen** (`./datos_tablero.xlsx`) sin token, útil al
   servir la carpeta con un servidor local.
3. Conector manual: pegar token o **arrastrar/seleccionar** el `.xlsx`.

## Qué muestra

- **KPIs:** total de facturas, valor total, valor promedio, % cerradas, sin
  cierre y pacientes únicos (HC).
- **Gráficos** (Chart.js): tendencia diaria, estado de cierre, valor por tipo de
  servicio, top 10 usuarios por n.º y por valor, facturas por fuente y top 10
  responsables por valor.
- **Filtros** combinables y **tabla** paginada/ordenable con exportación a **CSV**.

> Requiere internet (Chart.js y SheetJS por CDN, y la API de GitHub). Con
> **“Cargar archivo…”** puedes analizar cualquier Excel con esta estructura.

## Estructura esperada del Excel

`Fuente del documento`, `Nro de movimiento`, `Fecha movimiento`,
`Código Reponsable`, `tipo_ser`, `hc`, `Ingreso`, `cierre`, `Valor Documento`,
`Nombre del usuario`, `Primer Apellido del usuario`,
`Segundo Apellido del usuario` (`encusu` y `Fecha`, si existen, se ignoran).

## Privacidad

El Excel del repo (`datos_tablero.xlsx`) está **anonimizado**: sin `encusu`
(documento) y con `hc` **seudonimizada**. Aun así, el repo se mantiene
**privado** y el acceso requiere un **token de solo lectura** por usuario. El
Excel original (con datos sensibles) **no se versiona** (`.gitignore`).

### Regenerar el Excel anonimizado
```bash
pip install openpyxl
python3 anonimizar_excel.py archivo_original.xlsx datos_tablero.xlsx
```

## Archivos

| Archivo | Descripción |
|---|---|
| `tablero.html` | El dashboard. Lee el Excel del repo privado con tu token. |
| `datos_tablero.xlsx` | Datos **anonimizados** que consume el tablero. |
| `anonimizar_excel.py` | Genera el Excel anonimizado a partir del original. |

[SheetJS]: https://sheetjs.com/
