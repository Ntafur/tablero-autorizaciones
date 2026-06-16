# -*- coding: utf-8 -*-
"""Plantilla HTML del tablero. El marcador /*__DATA__*/ se reemplaza por el JSON."""

PLANTILLA_HTML = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tablero de Autorizaciones · Relación de facturas con cierre</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root{
    --bg:#eef2f7; --card:#ffffff; --ink:#1f2937; --muted:#6b7280;
    --line:#e5e7eb; --primary:#4f46e5; --primary-d:#4338ca;
    --green:#10b981; --red:#ef4444; --amber:#f59e0b; --sky:#0ea5e9;
    --shadow:0 1px 2px rgba(16,24,40,.06),0 4px 16px rgba(16,24,40,.06);
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{
    font-family:"Segoe UI",system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;
    background:var(--bg); color:var(--ink); font-size:14px; line-height:1.45;
  }
  a{color:var(--primary)}
  .wrap{max-width:1360px;margin:0 auto;padding:18px 20px 60px}

  header.topbar{
    background:linear-gradient(120deg,#312e81 0%,#4f46e5 55%,#0ea5e9 100%);
    color:#fff;border-radius:16px;padding:22px 26px;box-shadow:var(--shadow);
    display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;
  }
  header.topbar h1{margin:0;font-size:22px;letter-spacing:.2px}
  header.topbar p{margin:4px 0 0;opacity:.9;font-size:13px}
  .badges{display:flex;gap:10px;flex-wrap:wrap}
  .badge{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);
    padding:8px 12px;border-radius:10px;font-size:12px;backdrop-filter:blur(3px)}
  .badge b{display:block;font-size:15px;margin-top:2px}

  .panel{background:var(--card);border:1px solid var(--line);border-radius:14px;
    box-shadow:var(--shadow);padding:16px}
  .section-title{font-size:12px;text-transform:uppercase;letter-spacing:.08em;
    color:var(--muted);margin:22px 4px 10px;font-weight:700}

  /* Filtros */
  .filters{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-top:16px}
  .filters .field{display:flex;flex-direction:column;gap:4px}
  .filters label{font-size:11px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
  .filters input,.filters select{
    padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:#fff;
    font-size:13px;color:var(--ink);width:100%}
  .filters input:focus,.filters select:focus{outline:2px solid #c7d2fe;border-color:var(--primary)}
  .filters .actions{grid-column:1/-1;display:flex;gap:10px;align-items:center;justify-content:flex-end}
  .btn{border:1px solid var(--line);background:#fff;color:var(--ink);padding:8px 14px;
    border-radius:9px;cursor:pointer;font-size:13px;font-weight:600}
  .btn:hover{background:#f8fafc}
  .btn.primary{background:var(--primary);border-color:var(--primary);color:#fff}
  .btn.primary:hover{background:var(--primary-d)}

  /* KPIs */
  .kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-top:8px}
  .kpi{position:relative;overflow:hidden}
  .kpi .k-label{font-size:12px;color:var(--muted);font-weight:600}
  .kpi .k-value{font-size:24px;font-weight:800;margin-top:6px;letter-spacing:-.5px}
  .kpi .k-sub{font-size:12px;color:var(--muted);margin-top:2px}
  .kpi::after{content:"";position:absolute;right:-16px;top:-16px;width:60px;height:60px;
    border-radius:50%;opacity:.12}
  .kpi.c1::after{background:var(--primary)} .kpi.c2::after{background:var(--green)}
  .kpi.c3::after{background:var(--sky)} .kpi.c4::after{background:var(--amber)}
  .kpi.c5::after{background:var(--red)} .kpi.c6::after{background:#8b5cf6}

  /* Gráficos */
  .charts{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
  .chart-card h3{margin:0 0 10px;font-size:14px}
  .chart-card .canvas-box{position:relative;height:300px}
  .chart-card.full{grid-column:1/-1}
  .chart-card.full .canvas-box{height:320px}

  /* Tabla */
  .table-tools{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}
  .table-tools .count{font-size:13px;color:var(--muted)}
  .table-scroll{overflow:auto;border:1px solid var(--line);border-radius:10px}
  table{border-collapse:collapse;width:100%;font-size:13px;white-space:nowrap}
  thead th{position:sticky;top:0;background:#f8fafc;text-align:left;padding:10px 12px;
    font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);
    border-bottom:1px solid var(--line);cursor:pointer;user-select:none}
  thead th:hover{color:var(--ink)}
  thead th .arrow{opacity:.4;font-size:10px}
  tbody td{padding:9px 12px;border-bottom:1px solid #f1f5f9}
  tbody tr:hover{background:#f8fafc}
  td.num{text-align:right;font-variant-numeric:tabular-nums}
  .pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700}
  .pill.s{background:#dcfce7;color:#166534}
  .pill.n{background:#fee2e2;color:#991b1b}
  .pill.x{background:#fef3c7;color:#92400e}
  .pager{display:flex;gap:8px;align-items:center;justify-content:flex-end;margin-top:12px}
  .pager button{min-width:36px}
  .pager .info{font-size:13px;color:var(--muted);margin-right:auto}

  footer{margin-top:26px;color:var(--muted);font-size:12px;line-height:1.7}
  footer code{background:#fff;border:1px solid var(--line);padding:1px 6px;border-radius:6px}
  .nochart{display:flex;align-items:center;justify-content:center;height:100%;color:var(--muted);
    text-align:center;font-size:13px;padding:0 20px}

  @media (max-width:1024px){.filters{grid-template-columns:repeat(3,1fr)}.kpis{grid-template-columns:repeat(3,1fr)}}
  @media (max-width:680px){.filters{grid-template-columns:repeat(2,1fr)}.kpis{grid-template-columns:repeat(2,1fr)}.charts{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">

  <header class="topbar">
    <div>
      <h1>Tablero de Autorizaciones</h1>
      <p>Relación de facturas con cierre · análisis interactivo</p>
    </div>
    <div class="badges" id="headerBadges"></div>
  </header>

  <div class="section-title">Filtros</div>
  <div class="panel filters" id="filters">
    <div class="field"><label>Fecha desde</label><input type="date" id="fDesde"></div>
    <div class="field"><label>Fecha hasta</label><input type="date" id="fHasta"></div>
    <div class="field"><label>Estado de cierre</label><select id="fCierre"></select></div>
    <div class="field"><label>Tipo de servicio</label><select id="fTipo"></select></div>
    <div class="field"><label>Fuente</label><select id="fFuente"></select></div>
    <div class="field"><label>Usuario</label><select id="fUsuario"></select></div>
    <div class="field" style="grid-column:1/-1"><label>Buscar (HC, movimiento, usuario, responsable)</label><input type="text" id="fBuscar" placeholder="Escriba para filtrar..."></div>
    <div class="actions">
      <span class="count" id="filterMsg"></span>
      <button class="btn" id="btnLimpiar">Limpiar filtros</button>
    </div>
  </div>

  <div class="section-title">Indicadores</div>
  <div class="kpis" id="kpis"></div>

  <div class="section-title">Tendencia</div>
  <div class="charts">
    <div class="panel chart-card full"><h3>Facturas y valor por día</h3><div class="canvas-box"><canvas id="chTiempo"></canvas></div></div>
  </div>

  <div class="section-title">Distribuciones</div>
  <div class="charts">
    <div class="panel chart-card"><h3>Estado de cierre (n.º de facturas)</h3><div class="canvas-box"><canvas id="chCierre"></canvas></div></div>
    <div class="panel chart-card"><h3>Valor por tipo de servicio</h3><div class="canvas-box"><canvas id="chTipo"></canvas></div></div>
    <div class="panel chart-card"><h3>Top 10 usuarios por n.º de facturas</h3><div class="canvas-box"><canvas id="chUsuCount"></canvas></div></div>
    <div class="panel chart-card"><h3>Top 10 usuarios por valor</h3><div class="canvas-box"><canvas id="chUsuValor"></canvas></div></div>
    <div class="panel chart-card"><h3>Facturas por fuente del documento</h3><div class="canvas-box"><canvas id="chFuente"></canvas></div></div>
    <div class="panel chart-card"><h3>Top 10 responsables por valor</h3><div class="canvas-box"><canvas id="chResp"></canvas></div></div>
  </div>

  <div class="section-title">Detalle de facturas</div>
  <div class="panel">
    <div class="table-tools">
      <span class="count" id="tableCount"></span>
      <button class="btn primary" id="btnCsv">Exportar CSV</button>
    </div>
    <div class="table-scroll">
      <table id="tabla">
        <thead><tr id="theadRow"></tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <div class="pager">
      <span class="info" id="pageInfo"></span>
      <button class="btn" id="pgFirst">«</button>
      <button class="btn" id="pgPrev">‹</button>
      <button class="btn" id="pgNext">›</button>
      <button class="btn" id="pgLast">»</button>
    </div>
  </div>

  <footer>
    <div><b>Acerca de los datos.</b> Cada fila es un movimiento/factura. <b>Cierre</b>: S = cerrada, N = no cerrada, "Sin cierre" = sin marca.
    <b>HC</b> = historia clínica (paciente), <b>Tipo</b> = tipo de servicio, <b>Fuente</b> = fuente del documento, <b>Responsable</b> = código responsable.</div>
    <div id="footMeta" style="margin-top:6px"></div>
  </footer>

</div>

<script>
const DATA = /*__DATA__*/;

// ----------------------------------------------------------------------
// Utilidades de formato
// ----------------------------------------------------------------------
const nfInt = new Intl.NumberFormat("es-CO");
const nfCop = new Intl.NumberFormat("es-CO",{style:"currency",currency:"COP",maximumFractionDigits:0});
function money(n){ return nfCop.format(n||0); }
function int(n){ return nfInt.format(n||0); }
function compact(n){
  const a=Math.abs(n||0);
  if(a>=1e12) return (n/1e12).toLocaleString("es-CO",{maximumFractionDigits:1})+" B";
  if(a>=1e6)  return (n/1e6 ).toLocaleString("es-CO",{maximumFractionDigits:0})+" M";
  if(a>=1e3)  return (n/1e3 ).toLocaleString("es-CO",{maximumFractionDigits:0})+" K";
  return int(n);
}
const baseDate = new Date(DATA.fechaBase+"T00:00:00");
function dateFromIdx(d){ const t=new Date(baseDate); t.setDate(t.getDate()+d); return t; }
function fmtDate(d){
  if(d<0) return "—";
  const t=dateFromIdx(d);
  return ("0"+t.getDate()).slice(-2)+"/"+("0"+(t.getMonth()+1)).slice(-2)+"/"+t.getFullYear();
}
function isoDate(d){ const t=dateFromIdx(d); return t.toISOString().slice(0,10); }

// Índices de columnas en cada fila
const C = {d:0,fuente:1,tipo:2,cierre:3,valor:4,resp:5,ingreso:6,usuario:7,hc:8,mov:9};
const DIM = DATA.dim;
const ROWS = DATA.rows;
const cierreClase = ["s","n","x"];      // S / N / Sin cierre

// Paleta categórica
const PAL = ["#4f46e5","#0ea5e9","#10b981","#f59e0b","#ef4444","#8b5cf6","#ec4899","#14b8a6","#f97316","#64748b","#22c55e","#eab308"];

// ----------------------------------------------------------------------
// Poblar filtros
// ----------------------------------------------------------------------
function fillSelect(el, items, allLabel){
  let html = "<option value=\"-1\">"+allLabel+"</option>";
  items.forEach(function(it){ html += "<option value=\""+it.v+"\">"+it.t+"</option>"; });
  el.innerHTML = html;
}
function withIndex(arr){ return arr.map(function(t,i){return {v:i,t:t};}); }

const elDesde=document.getElementById("fDesde"), elHasta=document.getElementById("fHasta");
const elCierre=document.getElementById("fCierre"), elTipo=document.getElementById("fTipo");
const elFuente=document.getElementById("fFuente"), elUsuario=document.getElementById("fUsuario");
const elBuscar=document.getElementById("fBuscar");

elDesde.value = DATA.meta.fechaMin; elDesde.min = DATA.meta.fechaMin; elDesde.max = DATA.meta.fechaMax;
elHasta.value = DATA.meta.fechaMax; elHasta.min = DATA.meta.fechaMin; elHasta.max = DATA.meta.fechaMax;
fillSelect(elCierre, withIndex(DIM.cierres), "Todos");
fillSelect(elTipo, withIndex(DIM.tipos), "Todos");
fillSelect(elFuente, withIndex(DIM.fuentes), "Todas");
// usuarios ordenados alfabéticamente conservando su índice original
fillSelect(elUsuario, DIM.usuarios.map(function(t,i){return {v:i,t:t};})
  .sort(function(a,b){return a.t.localeCompare(b.t,"es");}), "Todos");

// ----------------------------------------------------------------------
// Estado y filtrado
// ----------------------------------------------------------------------
let filtered = ROWS;
let sortState = {col:C.d, dir:-1};   // por fecha desc
let page = 0;
const PAGE_SIZE = 25;

function readFilters(){
  const desde = elDesde.value ? Math.round((new Date(elDesde.value+"T00:00:00")-baseDate)/86400000) : -1e9;
  const hasta = elHasta.value ? Math.round((new Date(elHasta.value+"T00:00:00")-baseDate)/86400000) : 1e9;
  return {
    desde:desde, hasta:hasta,
    cierre:parseInt(elCierre.value,10),
    tipo:parseInt(elTipo.value,10),
    fuente:parseInt(elFuente.value,10),
    usuario:parseInt(elUsuario.value,10),
    q:(elBuscar.value||"").trim().toLowerCase()
  };
}

function applyFilters(){
  const f = readFilters();
  filtered = ROWS.filter(function(r){
    if(r[C.d]>=0 && (r[C.d]<f.desde || r[C.d]>f.hasta)) return false;
    if(f.cierre>=0 && r[C.cierre]!==f.cierre) return false;
    if(f.tipo>=0 && r[C.tipo]!==f.tipo) return false;
    if(f.fuente>=0 && r[C.fuente]!==f.fuente) return false;
    if(f.usuario>=0 && r[C.usuario]!==f.usuario) return false;
    if(f.q){
      const hay = (r[C.hc]+" "+r[C.mov]+" "+DIM.usuarios[r[C.usuario]]+" "+
                   (r[C.resp]>=0?DIM.responsables[r[C.resp]]:"")).toLowerCase();
      if(hay.indexOf(f.q)===-1) return false;
    }
    return true;
  });
  page = 0;
  sortFiltered();
}

function sortFiltered(){
  const col=sortState.col, dir=sortState.dir;
  filtered.sort(function(a,b){
    let x=a[col], y=b[col];
    if(col===C.hc || col===C.mov){ x=x||""; y=y||""; return x.localeCompare(y,"es",{numeric:true})*dir; }
    if(col===C.usuario){ return DIM.usuarios[x].localeCompare(DIM.usuarios[y],"es")*dir; }
    if(col===C.resp){ x=x>=0?DIM.responsables[x]:""; y=y>=0?DIM.responsables[y]:""; return String(x).localeCompare(String(y),"es",{numeric:true})*dir; }
    return (x-y)*dir;
  });
}

// ----------------------------------------------------------------------
// KPIs
// ----------------------------------------------------------------------
function renderKpis(){
  let total=filtered.length, suma=0, cerr=0, sinCierre=0;
  const hcSet=new Set();
  for(let i=0;i<filtered.length;i++){
    const r=filtered[i];
    suma+=r[C.valor];
    if(r[C.cierre]===0) cerr++;
    if(r[C.cierre]===2) sinCierre++;
    if(r[C.hc]) hcSet.add(r[C.hc]);
  }
  const prom = total? suma/total : 0;
  const pctCerr = total? (cerr/total*100) : 0;
  const cards=[
    {c:"c1",label:"Total facturas",value:int(total),sub:"movimientos filtrados"},
    {c:"c2",label:"Valor total",value:money(suma),sub:compact(suma)+" COP"},
    {c:"c3",label:"Valor promedio",value:money(Math.round(prom)),sub:"por factura"},
    {c:"c4",label:"Cerradas (S)",value:pctCerr.toFixed(1)+"%",sub:int(cerr)+" facturas"},
    {c:"c5",label:"Sin cierre",value:int(sinCierre),sub:"requieren gestión"},
    {c:"c6",label:"Pacientes (HC)",value:int(hcSet.size),sub:"historias únicas"},
  ];
  document.getElementById("kpis").innerHTML = cards.map(function(k){
    return "<div class=\"panel kpi "+k.c+"\"><div class=\"k-label\">"+k.label+"</div>"+
           "<div class=\"k-value\">"+k.value+"</div><div class=\"k-sub\">"+k.sub+"</div></div>";
  }).join("");
}

// ----------------------------------------------------------------------
// Gráficos
// ----------------------------------------------------------------------
const charts={};
const hasChart = (typeof Chart!=="undefined");
function noChart(id){
  const cv=document.getElementById(id); const box=cv.parentElement;
  box.innerHTML="<div class=\"nochart\">No se pudo cargar Chart.js (¿sin conexión?).<br>Los indicadores y la tabla siguen disponibles.</div>";
}
Chart && (Chart.defaults.font.family = getComputedStyle(document.body).fontFamily);
Chart && (Chart.defaults.color = "#6b7280");

function topN(counter, n){
  return Object.keys(counter).map(function(k){return [k,counter[k]];})
    .sort(function(a,b){return b[1]-a[1];}).slice(0,n);
}

function buildAggregates(){
  const days={}, cierre=[0,0,0], tipoVal={}, usuCount={}, usuVal={}, fuenteCount={}, respVal={};
  for(let i=0;i<filtered.length;i++){
    const r=filtered[i], v=r[C.valor];
    if(r[C.d]>=0){ if(!days[r[C.d]]) days[r[C.d]]=[0,0]; days[r[C.d]][0]++; days[r[C.d]][1]+=v; }
    cierre[r[C.cierre]]++;
    tipoVal[r[C.tipo]]=(tipoVal[r[C.tipo]]||0)+v;
    usuCount[r[C.usuario]]=(usuCount[r[C.usuario]]||0)+1;
    usuVal[r[C.usuario]]=(usuVal[r[C.usuario]]||0)+v;
    fuenteCount[r[C.fuente]]=(fuenteCount[r[C.fuente]]||0)+1;
    if(r[C.resp]>=0) respVal[r[C.resp]]=(respVal[r[C.resp]]||0)+v;
  }
  return {days,cierre,tipoVal,usuCount,usuVal,fuenteCount,respVal};
}

function renderCharts(){
  if(!hasChart) return;
  const a=buildAggregates();

  // Tendencia diaria
  const dayKeys=Object.keys(a.days).map(Number).sort(function(x,y){return x-y;});
  const labels=dayKeys.map(fmtDate);
  const cnt=dayKeys.map(function(d){return a.days[d][0];});
  const val=dayKeys.map(function(d){return a.days[d][1];});
  upsert("chTiempo",{
    type:"bar",
    data:{labels:labels,datasets:[
      {type:"bar",label:"Facturas",data:cnt,backgroundColor:"rgba(79,70,229,.7)",yAxisID:"y",order:2},
      {type:"line",label:"Valor",data:val,borderColor:"#0ea5e9",backgroundColor:"rgba(14,165,233,.15)",
        borderWidth:2,tension:.3,fill:true,yAxisID:"y1",order:1,pointRadius:2}
    ]},
    options:baseOpts({
      scales:{
        y:{position:"left",title:{display:true,text:"Facturas"},ticks:{precision:0}},
        y1:{position:"right",grid:{drawOnChartArea:false},title:{display:true,text:"Valor"},
            ticks:{callback:function(v){return compact(v);}}}
      },
      plugins:{tooltip:{callbacks:{label:function(c){
        return c.dataset.label+": "+(c.dataset.yAxisID==="y1"?money(c.parsed.y):int(c.parsed.y));}}}}
    })
  });

  // Estado de cierre (dona)
  upsert("chCierre",{
    type:"doughnut",
    data:{labels:DIM.cierres,datasets:[{data:a.cierre,
      backgroundColor:["#10b981","#ef4444","#f59e0b"],borderWidth:2,borderColor:"#fff"}]},
    options:baseOpts({cutout:"58%",plugins:{legend:{position:"bottom"},
      tooltip:{callbacks:{label:function(c){const t=a.cierre.reduce(function(s,x){return s+x;},0);
        return c.label+": "+int(c.parsed)+" ("+(t?(c.parsed/t*100).toFixed(1):0)+"%)";}}}}})
  });

  // Valor por tipo de servicio
  const tipoKeys=Object.keys(a.tipoVal).sort(function(x,y){return a.tipoVal[y]-a.tipoVal[x];});
  upsert("chTipo",{
    type:"bar",
    data:{labels:tipoKeys.map(function(k){return "Tipo "+DIM.tipos[k];}),
      datasets:[{label:"Valor",data:tipoKeys.map(function(k){return a.tipoVal[k];}),
        backgroundColor:tipoKeys.map(function(_,i){return PAL[i%PAL.length];})}]},
    options:baseOpts({plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return money(c.parsed.y);}}}},
      scales:{y:{ticks:{callback:function(v){return compact(v);}}}}})
  });

  // Top usuarios por n.º
  barTop("chUsuCount", topN(a.usuCount,10), function(k){return DIM.usuarios[k];},
         function(v){return v;}, "#4f46e5", int, true);
  // Top usuarios por valor
  barTop("chUsuValor", topN(a.usuVal,10), function(k){return DIM.usuarios[k];},
         function(v){return v;}, "#0ea5e9", money, true);

  // Facturas por fuente
  const fKeys=Object.keys(a.fuenteCount).sort(function(x,y){return a.fuenteCount[y]-a.fuenteCount[x];});
  upsert("chFuente",{
    type:"bar",
    data:{labels:fKeys.map(function(k){return DIM.fuentes[k];}),
      datasets:[{label:"Facturas",data:fKeys.map(function(k){return a.fuenteCount[k];}),
        backgroundColor:fKeys.map(function(_,i){return PAL[i%PAL.length];})}]},
    options:baseOpts({plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return int(c.parsed.y)+" facturas";}}}},
      scales:{y:{ticks:{precision:0}}}})
  });

  // Top responsables por valor
  barTop("chResp", topN(a.respVal,10), function(k){return "Resp. "+DIM.responsables[k];},
         function(v){return v;}, "#8b5cf6", money, true);
}

function barTop(id, pairs, labelFn, valFn, color, fmt, horizontal){
  upsert(id,{
    type:"bar",
    data:{labels:pairs.map(function(p){return labelFn(p[0]);}),
      datasets:[{label:"",data:pairs.map(function(p){return valFn(p[1]);}),backgroundColor:color,borderRadius:4}]},
    options:baseOpts({
      indexAxis:horizontal?"y":"x",
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){
        return fmt(horizontal?c.parsed.x:c.parsed.y);}}}},
      scales: horizontal
        ? {x:{ticks:{callback:function(v){return compact(v);}}}}
        : {y:{ticks:{callback:function(v){return compact(v);}}}}
    })
  });
}

function baseOpts(extra){
  const base={responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false}},
    animation:{duration:300}};
  return Object.assign(base, extra||{});
}
function upsert(id,cfg){
  if(charts[id]){ charts[id].data=cfg.data; charts[id].options=cfg.options; charts[id].config.type=cfg.type; charts[id].update(); }
  else { charts[id]=new Chart(document.getElementById(id), cfg); }
}

// ----------------------------------------------------------------------
// Tabla
// ----------------------------------------------------------------------
const COLS=[
  {key:C.mov,label:"Movimiento"},
  {key:C.d,label:"Fecha"},
  {key:C.fuente,label:"Fuente"},
  {key:C.tipo,label:"Tipo"},
  {key:C.hc,label:"HC"},
  {key:C.ingreso,label:"Ingreso",num:true},
  {key:C.cierre,label:"Cierre"},
  {key:C.valor,label:"Valor",num:true},
  {key:C.usuario,label:"Usuario"},
  {key:C.resp,label:"Responsable"},
];
function renderHead(){
  document.getElementById("theadRow").innerHTML = COLS.map(function(c){
    const arrow = sortState.col===c.key ? (sortState.dir>0?" ▲":" ▼") : "";
    return "<th data-col=\""+c.key+"\">"+c.label+"<span class=\"arrow\">"+(arrow||" ↕")+"</span></th>";
  }).join("");
  Array.prototype.forEach.call(document.querySelectorAll("#theadRow th"), function(th){
    th.addEventListener("click", function(){
      const col=parseInt(th.getAttribute("data-col"),10);
      if(sortState.col===col) sortState.dir*=-1; else { sortState.col=col; sortState.dir=1; }
      sortFiltered(); renderHead(); renderTable();
    });
  });
}
function cellValue(r,c){
  switch(c.key){
    case C.d: return fmtDate(r[C.d]);
    case C.fuente: return DIM.fuentes[r[C.fuente]];
    case C.tipo: return DIM.tipos[r[C.tipo]];
    case C.cierre: {const v=r[C.cierre];return "<span class=\"pill "+cierreClase[v]+"\">"+DIM.cierres[v]+"</span>";}
    case C.valor: return money(r[C.valor]);
    case C.ingreso: return r[C.ingreso]>=0?int(r[C.ingreso]):"—";
    case C.usuario: return DIM.usuarios[r[C.usuario]];
    case C.resp: return r[C.resp]>=0?DIM.responsables[r[C.resp]]:"—";
    case C.hc: return r[C.hc]||"—";
    case C.mov: return r[C.mov]||"—";
    default: return "";
  }
}
function renderTable(){
  const pages=Math.max(1,Math.ceil(filtered.length/PAGE_SIZE));
  if(page>=pages) page=pages-1; if(page<0) page=0;
  const start=page*PAGE_SIZE, slice=filtered.slice(start,start+PAGE_SIZE);
  document.getElementById("tbody").innerHTML = slice.map(function(r){
    return "<tr>"+COLS.map(function(c){
      return "<td"+(c.num?" class=\"num\"":"")+">"+cellValue(r,c)+"</td>";
    }).join("")+"</tr>";
  }).join("") || "<tr><td colspan=\""+COLS.length+"\" style=\"padding:24px;text-align:center;color:#6b7280\">Sin resultados para los filtros aplicados.</td></tr>";
  const showFrom = filtered.length? start+1 : 0;
  const showTo = Math.min(start+PAGE_SIZE, filtered.length);
  document.getElementById("pageInfo").textContent =
    "Mostrando "+int(showFrom)+"–"+int(showTo)+" de "+int(filtered.length)+" · página "+(page+1)+"/"+pages;
  document.getElementById("tableCount").textContent = int(filtered.length)+" facturas en la vista actual";
}

// ----------------------------------------------------------------------
// CSV
// ----------------------------------------------------------------------
function exportCsv(){
  const sep=";";
  const head=["Movimiento","Fecha","Fuente","Tipo","HC","Ingreso","Cierre","Valor","Usuario","Responsable"];
  const lines=[head.join(sep)];
  function esc(s){ s=String(s==null?"":s); return /[";\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s; }
  for(let i=0;i<filtered.length;i++){
    const r=filtered[i];
    lines.push([
      r[C.mov], r[C.d]>=0?isoDate(r[C.d]):"", DIM.fuentes[r[C.fuente]], DIM.tipos[r[C.tipo]],
      r[C.hc], r[C.ingreso]>=0?r[C.ingreso]:"", DIM.cierres[r[C.cierre]], r[C.valor],
      DIM.usuarios[r[C.usuario]], r[C.resp]>=0?DIM.responsables[r[C.resp]]:""
    ].map(esc).join(sep));
  }
  const blob=new Blob(["﻿"+lines.join("\r\n")],{type:"text/csv;charset=utf-8;"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url; a.download="facturas_filtradas.csv"; document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}

// ----------------------------------------------------------------------
// Encabezado / meta
// ----------------------------------------------------------------------
function renderHeaderBadges(){
  let suma=0; for(let i=0;i<ROWS.length;i++) suma+=ROWS[i][C.valor];
  const b=[
    {l:"Facturas",v:int(ROWS.length)},
    {l:"Valor total",v:compact(suma)+" COP"},
    {l:"Periodo",v:fmtDate(0)+" – "+fmtDate(Math.round((new Date(DATA.meta.fechaMax+"T00:00:00")-baseDate)/86400000))},
    {l:"Usuarios",v:int(DIM.usuarios.length)},
  ];
  document.getElementById("headerBadges").innerHTML = b.map(function(x){
    return "<div class=\"badge\">"+x.l+"<b>"+x.v+"</b></div>";
  }).join("");
  document.getElementById("footMeta").innerHTML =
    "Generado el "+DATA.meta.generado+" · "+int(DATA.meta.totalFilas)+" registros · "+
    int(DIM.responsables.length)+" responsables · fuente: archivo Excel <code>relación de facturas con cierre</code>.";
}

// ----------------------------------------------------------------------
// Render global y eventos
// ----------------------------------------------------------------------
function renderAll(){
  renderKpis(); renderCharts(); renderHead(); renderTable();
  const f=readFilters();
  const activos = (f.cierre>=0)+(f.tipo>=0)+(f.fuente>=0)+(f.usuario>=0)+(f.q?1:0);
  document.getElementById("filterMsg").textContent =
    int(filtered.length)+" de "+int(ROWS.length)+" facturas"+(activos?" · "+activos+" filtro(s) activo(s)":"");
}
function refilterAndRender(){ applyFilters(); renderAll(); }

let debounce;
function onFilterChange(){ clearTimeout(debounce); debounce=setTimeout(refilterAndRender,120); }
[elDesde,elHasta,elCierre,elTipo,elFuente,elUsuario].forEach(function(e){e.addEventListener("change",refilterAndRender);});
elBuscar.addEventListener("input", onFilterChange);

document.getElementById("btnLimpiar").addEventListener("click", function(){
  elDesde.value=DATA.meta.fechaMin; elHasta.value=DATA.meta.fechaMax;
  elCierre.value="-1"; elTipo.value="-1"; elFuente.value="-1"; elUsuario.value="-1"; elBuscar.value="";
  refilterAndRender();
});
document.getElementById("btnCsv").addEventListener("click", exportCsv);
document.getElementById("pgFirst").addEventListener("click",function(){page=0;renderTable();});
document.getElementById("pgPrev").addEventListener("click",function(){page--;renderTable();});
document.getElementById("pgNext").addEventListener("click",function(){page++;renderTable();});
document.getElementById("pgLast").addEventListener("click",function(){page=1e9;renderTable();});

if(!hasChart){ ["chTiempo","chCierre","chTipo","chUsuCount","chUsuValor","chFuente","chResp"].forEach(noChart); }
renderHeaderBadges();
applyFilters();
renderAll();
</script>
</body>
</html>
'''
