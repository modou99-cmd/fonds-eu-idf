import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Fonds Européens — Île-de-France",
    page_icon="🇪🇺",
    layout="wide",
)

st.markdown("""
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
header{visibility:hidden}
.block-container{padding:0 !important;max-width:100% !important}
</style>
""", unsafe_allow_html=True)

APP_HTML = """
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
:root{
  --bg:#f0f2f5;--bg2:#ffffff;--bg3:#f7f8fa;--bg4:#eef4fb;
  --txt:#1a1a2e;--txt2:#555;--txt3:#888;--txt4:#aaa;
  --border:#e2e6ea;--border2:#d0d7de;
  --blue:#1F4E79;--blue2:#2E75B6;--blue3:#5ba3e8;--blue-pale:#eef4fb;
  --orange:#C55A11;--orange-pale:#fff8ec;
  --green:#375623;--green-pale:#edfaf3;
  --red:#C00000;--red-pale:#fff0f0;
  --warn-bg:#fff8ec;--warn-fg:#C55A11;
  --ok-bg:#edfaf3;--ok-fg:#375623;
  --crit-bg:#fff0f0;--crit-fg:#C00000;
  --info-bg:#eef4fb;--info-fg:#1F4E79;
}
@media(prefers-color-scheme:dark){
  :root{
    --bg:#12141a;--bg2:#1e2030;--bg3:#181a24;--bg4:#1a2540;
    --txt:#e8eaf0;--txt2:#b0b8c8;--txt3:#7a8299;--txt4:#4a5270;
    --border:#2a2d3e;--border2:#333650;
    --blue:#5ba3e8;--blue2:#7ab8ee;--blue3:#9ecdf5;--blue-pale:#1a2540;
    --orange:#e89050;--orange-pale:#2a1e10;
    --green:#68b368;--green-pale:#1a2a1a;
    --red:#e85050;--red-pale:#2a1010;
    --warn-bg:#2a1e10;--warn-fg:#e89050;
    --ok-bg:#1a2a1a;--ok-fg:#68b368;
    --crit-bg:#2a1010;--crit-fg:#e85050;
    --info-bg:#1a2540;--info-fg:#5ba3e8;
  }
}
body{background:var(--bg);color:var(--txt)}
.app{max-width:1120px;margin:0 auto;padding:14px}
.topbar{display:flex;align-items:center;justify-content:space-between;background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:12px 18px;margin-bottom:10px}
.topbar h1{font-size:17px;font-weight:600;color:var(--blue)}
.topbar p{font-size:11px;color:var(--txt3);margin-top:3px}
.badge{font-size:11px;padding:4px 12px;border-radius:20px;background:var(--blue-pale);color:var(--blue);font-weight:600;border:1px solid var(--border)}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-bottom:10px}
.kpi{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:12px 14px;border-left:3px solid var(--blue)}
.kpi-lbl{font-size:10px;color:var(--txt3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.kpi-val{font-size:21px;font-weight:700;color:var(--blue)}
.kpi-sub{font-size:10px;color:var(--txt4);margin-top:2px}
.layout{display:grid;grid-template-columns:190px 1fr;gap:10px;align-items:start}
.sidebar{display:flex;flex-direction:column;gap:8px}
.sidenav{background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden}
.nav-item{display:flex;align-items:center;gap:10px;padding:11px 14px;cursor:pointer;font-size:13px;color:var(--txt2);border-left:3px solid transparent;transition:all .15s;background:none;border-top:none;border-right:none;border-bottom:1px solid var(--border);width:100%;text-align:left;font-family:inherit}
.nav-item:last-child{border-bottom:none}
.nav-item.active{color:var(--blue);border-left-color:var(--blue);background:var(--blue-pale);font-weight:600}
.nav-item:hover:not(.active){background:var(--bg3)}
.nav-icon{font-size:15px;width:20px;text-align:center;flex-shrink:0}
.fcard{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:12px 14px}
.ftitle{font-size:10px;font-weight:600;color:var(--txt3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}
.seg{display:flex;flex-direction:column;gap:3px;margin-bottom:2px}
.seg-btn{font-size:12px;padding:6px 10px;border-radius:7px;border:1px solid var(--border);background:none;cursor:pointer;color:var(--txt2);text-align:left;font-family:inherit;transition:all .12s}
.seg-btn.active{background:var(--blue-pale);color:var(--blue);border-color:var(--blue2);font-weight:600}
.seg-btn:hover:not(.active){background:var(--bg3)}
.cb-row{display:flex;align-items:center;gap:8px;margin-top:7px;cursor:pointer}
.cb{width:15px;height:15px;border-radius:4px;border:1.5px solid var(--border2);display:flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0;transition:all .12s;color:white}
.cb.on{border-color:var(--blue2)}
.cb-lbl{font-size:12px;color:var(--txt2)}
.main{min-width:0;display:flex;flex-direction:column;gap:10px}
.panel{display:none}.panel.active{display:flex;flex-direction:column;gap:10px}
.row2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}
.row4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
.ctitle{font-size:11px;font-weight:600;color:var(--txt3);text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px}
.bar-row{display:flex;align-items:center;gap:8px;margin-bottom:6px}
.blbl{font-size:11px;color:var(--txt2);width:110px;text-align:right;flex-shrink:0}
.bbg{flex:1;background:var(--bg3);border-radius:3px;height:14px}
.bfill{height:14px;border-radius:3px;transition:width .35s ease}
.bval{font-size:11px;font-weight:600;color:var(--txt2);width:52px;text-align:right}
.tt{position:absolute;background:var(--bg2);border:1px solid var(--border2);border-radius:10px;padding:10px 14px;pointer-events:none;display:none;z-index:99;min-width:160px}
.tt-name{font-size:13px;font-weight:700;color:var(--blue);margin-bottom:7px}
.tt-row{display:flex;justify-content:space-between;gap:12px;margin-top:3px}
.tt-k{font-size:11px;color:var(--txt3)}.tt-v{font-size:11px;font-weight:600;color:var(--txt)}
.leg{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;font-size:11px;color:var(--txt3);align-items:center}
.sw{width:9px;height:9px;border-radius:2px;display:inline-block;margin-right:3px;vertical-align:middle}
.ops-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--border)}
.ops-row:last-child{border:none}
.ops-n{font-size:11px;color:var(--txt4);width:16px;flex-shrink:0}
.ops-info{flex:1;min-width:0}
.ops-name{font-size:12px;font-weight:600;color:var(--txt);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ops-op{font-size:10px;color:var(--txt3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:1px}
.pill{font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;flex-shrink:0}
.ops-amt{font-size:12px;font-weight:700;color:var(--blue);width:50px;text-align:right;flex-shrink:0}
.qgrid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.qcard{border:1px solid var(--border);border-radius:10px;padding:10px 12px;background:var(--bg3)}
.qcol{font-size:10px;color:var(--txt4);font-weight:600;margin-bottom:1px}
.qname{font-size:12px;font-weight:600;color:var(--txt)}
.qpct{font-size:18px;font-weight:700;margin:4px 0 2px}
.qnote{font-size:10px;color:var(--txt3)}
.qbadge{font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px}
.anom{border-left:3px solid;padding:10px 12px;margin-bottom:7px;border-radius:0 7px 7px 0;background:var(--bg3)}
.anom-t{font-size:12px;font-weight:700;margin-bottom:3px}
.anom-d{font-size:11px;color:var(--txt2);line-height:1.65}
.banner{border-radius:8px;padding:9px 12px;font-size:11px;line-height:1.55;margin-top:8px;border-left:3px solid}
</style>

<div class="app">
  <div class="topbar">
    <div>
      <h1>Fonds Européens — Île-de-France</h1>
      <p>1 121 opérations &nbsp;·&nbsp; 1 669 M€ &nbsp;·&nbsp; 2014-2020 &nbsp;·&nbsp; data.gouv.fr</p>
    </div>
    <span class="badge">SGAE · Étude de cas</span>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="kpi-lbl">Montant total UE</div><div class="kpi-val">1 669 M€</div><div class="kpi-sub">8 départements IDF</div></div>
    <div class="kpi"><div class="kpi-lbl">Opérations</div><div class="kpi-val">1 121</div><div class="kpi-sub">879 mono-département</div></div>
    <div class="kpi"><div class="kpi-lbl">Bénéficiaires</div><div class="kpi-val">558</div><div class="kpi-sub">acteurs uniques</div></div>
    <div class="kpi" style="border-left-color:var(--orange)"><div class="kpi-lbl">Corrélation INSEE</div><div class="kpi-val" style="color:var(--orange)">r = −0.55</div><div class="kpi-sub">cohésion territoriale</div></div>
  </div>

  <div class="layout">
    <div class="sidebar">
      <nav class="sidenav">
        <button class="nav-item active" onclick="showPanel('carte',this)"><span class="nav-icon">▦</span>Carte territoriale</button>
        <button class="nav-item" onclick="showPanel('ops',this)"><span class="nav-icon">▤</span>Opérations</button>
        <button class="nav-item" onclick="showPanel('qual',this)"><span class="nav-icon">◎</span>Qualité des données</button>
      </nav>

      <div class="fcard">
        <div class="ftitle">Classement</div>
        <div class="seg" id="sort-seg">
          <button class="seg-btn active" onclick="setSort('montant',this)">Montant total</button>
          <button class="seg-btn" onclick="setSort('ops',this)">Nb opérations</button>
          <button class="seg-btn" onclick="setSort('moy',this)">Moy / opération</button>
        </div>
        <div class="ftitle" style="margin-top:12px">Fonds</div>
        <div class="cb-row" onclick="toggleFonds('FEDER')">
          <div class="cb on" id="cb-FEDER" style="background:var(--blue)">✓</div>
          <span class="cb-lbl" style="color:var(--blue)">FEDER</span>
        </div>
        <div class="cb-row" onclick="toggleFonds('FSE')">
          <div class="cb on" id="cb-FSE" style="background:var(--orange)">✓</div>
          <span class="cb-lbl" style="color:var(--orange)">FSE / FSE+</span>
        </div>
        <div class="cb-row" onclick="toggleFonds('IEJ')">
          <div class="cb on" id="cb-IEJ" style="background:var(--green)">✓</div>
          <span class="cb-lbl" style="color:var(--green)">IEJ</span>
        </div>
      </div>
    </div>

    <div class="main">
      <!-- CARTE -->
      <div id="panel-carte" class="panel active">
        <div class="row2">
          <div class="card" style="position:relative">
            <div class="ctitle">Répartition par département</div>
            <svg id="idf-map" viewBox="0 0 300 320" style="width:100%;height:280px"></svg>
            <div class="leg" id="map-legend"></div>
            <div class="tt" id="tooltip"></div>
          </div>
          <div class="card">
            <div class="ctitle">Classement</div>
            <div id="bar-chart"></div>
            <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--border)">
              <div class="ctitle">Répartition par fonds</div>
              <div style="position:relative;height:150px"><canvas id="fonds-chart"></canvas></div>
              <div id="fonds-legend" class="leg"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- OPÉRATIONS -->
      <div id="panel-ops" class="panel">
        <div class="row2">
          <div class="card">
            <div class="ctitle">Top 10 — financements les plus importants</div>
            <div id="top10"></div>
          </div>
          <div class="card">
            <div class="ctitle">Corrélation fonds EU / revenu médian</div>
            <div style="position:relative;height:250px"><canvas id="scatter"></canvas></div>
            <div class="banner" style="background:var(--warn-bg);color:var(--warn-fg);border-color:var(--orange);margin-top:10px">
              <strong>r = −0.55</strong> — corrélation négative modérée. Les depts plus pauvres reçoivent proportionnellement plus.
              <strong>Paris :</strong> anomalie — BpiFrance et acteurs R&D domiciliés en 75.
            </div>
          </div>
        </div>
      </div>

      <!-- QUALITÉ -->
      <div id="panel-qual" class="panel">
        <div class="row4">
          <div class="kpi" style="border-left-color:var(--green)"><div class="kpi-lbl">Complets</div><div class="kpi-val" style="color:var(--green)">5</div><div class="kpi-sub">sur 9 champs</div></div>
          <div class="kpi" style="border-left-color:var(--orange)"><div class="kpi-lbl">À surveiller</div><div class="kpi-val" style="color:var(--orange)">2</div><div class="kpi-sub">sur 9 champs</div></div>
          <div class="kpi" style="border-left-color:var(--red)"><div class="kpi-lbl">Critiques</div><div class="kpi-val" style="color:var(--red)">2</div><div class="kpi-sub">sur 9 champs</div></div>
          <div class="kpi"><div class="kpi-lbl">NaN catégorie</div><div class="kpi-val">896</div><div class="kpi-sub">sur 1 121 lignes</div></div>
        </div>
        <div class="row2">
          <div class="card">
            <div class="ctitle">Complétude par champ</div>
            <div class="qgrid" id="qual-grid"></div>
          </div>
          <div class="card">
            <div class="ctitle">Anomalies détectées</div>
            <div id="anom-list"></div>
            <div class="banner" style="background:var(--info-bg);color:var(--info-fg);border-color:var(--blue);margin-top:10px">
              <strong>Recommandation :</strong> Enrichir via SYNERGIE · Catégorie obligatoire à la saisie · Normaliser bénéficiaires par SIRET/SIREN
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const DEPTS=[
  {code:'93',nom:'Seine-St-Denis',ops:217,montant:182.2,moy:840,revenu:17620},
  {code:'75',nom:'Paris',         ops:189,montant:123.7,moy:654,revenu:30880},
  {code:'94',nom:'Val-de-Marne',  ops:93, montant:71.4, moy:768,revenu:22960},
  {code:'95',nom:"Val-d'Oise",    ops:108,montant:62.7, moy:580,revenu:25620},
  {code:'77',nom:'Seine-et-Marne',ops:75, montant:67.9, moy:905,revenu:24110},
  {code:'78',nom:'Yvelines',      ops:83, montant:57.6, moy:694,revenu:27980},
  {code:'91',nom:'Essonne',       ops:66, montant:59.0, moy:893,revenu:26085},
  {code:'92',nom:'Hauts-de-Seine',ops:48, montant:40.1, moy:836,revenu:29250},
];
const TOP10=[
  {b:'BpiFrance Financement',op:'Prêts rebond FEDER IDF',m:132.5,f:'FEDER'},
  {b:'Région IDF',op:'REACT-EU équipements lycées',m:105.0,f:'FEDER'},
  {b:'Région IDF',op:'Équipements numériques lycées',m:61.0,f:'FEDER'},
  {b:'Conseil Régional IDF',op:'PRFE 1ère reconduction 2019',m:51.8,f:'FSE'},
  {b:'Conseil Régional IDF',op:'PRC 3 — 2ème reconduction',m:50.5,f:'FSE'},
  {b:'Conseil Régional IDF',op:'PRFE 2018 initial',m:49.1,f:'FSE'},
  {b:'Conseil Régional IDF',op:'PRC 4 — 1ère reconduction',m:45.6,f:'FSE'},
  {b:'Conseil Régional IDF',op:'Avenir Jeunes 2ème reconduction',m:43.5,f:'FSE'},
  {b:'BpiFrance',op:'FEDER REACT EU prêts rebond',m:33.1,f:'FEDER'},
  {b:'Conseil Régional IDF',op:'Paris Region Venture Fund',m:32.8,f:'FEDER'},
];
const QUAL=[
  {col:'A',nom:'Bénéficiaire',    pct:100, niv:'ok',  nan:0,  note:'558 acteurs distincts'},
  {col:'F',nom:'Montant EU',       pct:100, niv:'ok',  nan:0,  note:'1 montant à 0 EUR'},
  {col:'M',nom:'Fonds',            pct:100, niv:'ok',  nan:0,  note:'FSE / FEDER / IEJ'},
  {col:'D',nom:'Date début',       pct:100, niv:'ok',  nan:0,  note:'Format ISO 2014-2022'},
  {col:'G',nom:'Taux cofin.',      pct:100, niv:'ok',  nan:0,  note:'0 à 0.70'},
  {col:'J',nom:'Département',      pct:99.1,niv:'warn',nan:10, note:'10 vides + 223 multi'},
  {col:'H',nom:'Emplacement',      pct:94,  niv:'warn',nan:67, note:'Parfois vide'},
  {col:'I',nom:'ITI',              pct:30,  niv:'crit',nan:784,note:'70% vide'},
  {col:'L',nom:'Catégorie interv.',pct:20.1,niv:'crit',nan:896,note:'Lignes 4 à 1122'},
];
const FC={FEDER:'#1F4E79',FSE:'#C55A11',IEJ:'#375623'};
const PATHS={
  '77':'M148,180 L190,170 L210,185 L205,220 L180,235 L155,225 L140,205 Z',
  '78':'M80,130 L115,118 L130,135 L125,160 L100,165 L78,152 Z',
  '91':'M120,185 L148,178 L155,205 L140,225 L115,220 L105,200 Z',
  '92':'M108,148 L128,144 L132,160 L118,168 L105,162 Z',
  '93':'M138,128 L165,122 L175,140 L168,158 L148,160 L132,148 Z',
  '94':'M132,160 L156,155 L160,175 L148,185 L130,180 Z',
  '95':'M90,105 L130,95 L140,115 L132,132 L108,138 L86,125 Z',
  '75':'M120,148 L138,142 L145,155 L138,165 L120,168 L112,158 Z',
};

const isDark=matchMedia('(prefers-color-scheme:dark)').matches;
const maxM=Math.max(...DEPTS.map(d=>d.montant));
const cs=isDark
  ? d3.scaleSequential([0,maxM],d3.interpolate('#0a2a4a','#5ba3e8'))
  : d3.scaleSequential([0,maxM],d3.interpolateBlues);
const tt=document.getElementById('tooltip');
const gridColor=isDark?'rgba(255,255,255,.07)':'rgba(0,0,0,.07)';
let activeFonds=new Set(['FEDER','FSE','IEJ']);
let sk='montant';
let fondsChart=null;

function bbox(d){
  const n=d.match(/-?\d+\.?\d*/g).map(Number),xs=[],ys=[];
  for(let i=0;i<n.length;i+=2){xs.push(n[i]);ys.push(n[i+1]);}
  return{cx:(Math.min(...xs)+Math.max(...xs))/2,cy:(Math.min(...ys)+Math.max(...ys))/2};
}

function buildMap(){
  const svg=document.getElementById('idf-map');
  DEPTS.forEach(dept=>{
    const p=document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d',PATHS[dept.code]);
    p.setAttribute('fill',cs(dept.montant));
    p.setAttribute('stroke',isDark?'rgba(0,0,0,.4)':'#fff');
    p.setAttribute('stroke-width','1.5');
    p.style.cssText='cursor:pointer;transition:opacity .12s';
    const bb=bbox(PATHS[dept.code]);
    const t=document.createElementNS('http://www.w3.org/2000/svg','text');
    t.setAttribute('x',bb.cx);t.setAttribute('y',bb.cy);
    t.setAttribute('text-anchor','middle');t.setAttribute('dominant-baseline','middle');
    t.setAttribute('font-size','9');t.setAttribute('font-weight','700');
    t.setAttribute('fill',isDark?'rgba(0,0,0,.85)':'rgba(255,255,255,.95)');
    t.setAttribute('pointer-events','none');
    t.textContent=dept.code;
    p.onmouseenter=()=>p.style.opacity='.72';
    p.onmousemove=e=>{
      const r=svg.closest('.card').getBoundingClientRect();
      const lx=e.clientX-r.left;
      tt.style.display='block';
      tt.style.left=(lx>r.width/2?lx-175:lx+12)+'px';
      tt.style.top=Math.max(0,e.clientY-r.top-20)+'px';
      tt.innerHTML=`<div class="tt-name">${dept.nom} (${dept.code})</div>
        <div class="tt-row"><span class="tt-k">Montant EU</span><span class="tt-v">${dept.montant} M€</span></div>
        <div class="tt-row"><span class="tt-k">Opérations</span><span class="tt-v">${dept.ops}</span></div>
        <div class="tt-row"><span class="tt-k">Moy / opération</span><span class="tt-v">${dept.moy} K€</span></div>
        <div class="tt-row"><span class="tt-k">Revenu médian</span><span class="tt-v">${dept.revenu.toLocaleString('fr')} €</span></div>`;
    };
    p.onmouseleave=()=>{p.style.opacity='1';tt.style.display='none';};
    svg.appendChild(p);svg.appendChild(t);
  });
  const leg=document.getElementById('map-legend');
  [0,50,100,150].forEach((v,i,a)=>{
    const s=document.createElement('span');
    s.innerHTML=`<span class="sw" style="background:${cs(v+25)}"></span>${v}–${a[i+1]||182} M€`;
    leg.appendChild(s);
  });
}

function setSort(k,btn){
  sk=k;
  document.querySelectorAll('#sort-seg .seg-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderBars();
}

function renderBars(){
  const s=[...DEPTS].sort((a,b)=>b[sk]-a[sk]);
  const mv=Math.max(...s.map(d=>d[sk]));
  const cc={montant:'#1F4E79',ops:'#C55A11',moy:'#375623'};
  const fmt=v=>sk==='montant'?v+'M€':sk==='ops'?v+' ops':v+'K€';
  document.getElementById('bar-chart').innerHTML=s.map(d=>{
    const v=d[sk];
    return`<div class="bar-row">
      <div class="blbl">${d.nom}</div>
      <div class="bbg"><div class="bfill" style="width:${Math.round(v/mv*100)}%;background:${cc[sk]}"></div></div>
      <div class="bval">${fmt(v)}</div>
    </div>`;
  }).join('');
}

function toggleFonds(f){
  if(activeFonds.has(f))activeFonds.delete(f);
  else activeFonds.add(f);
  const cb=document.getElementById('cb-'+f);
  cb.classList.toggle('on',activeFonds.has(f));
  cb.textContent=activeFonds.has(f)?'✓':'';
  if(!activeFonds.has(f))cb.style.background='none';
  else cb.style.background=FC[f];
  renderFonds();
  renderTop10();
}

function renderFonds(){
  const all=[{l:'FEDER',v:55.0,c:'#1F4E79'},{l:'FSE/FSE+',v:43.6,c:'#C55A11'},{l:'IEJ',v:1.4,c:'#375623'}];
  const fd=all.filter(d=>activeFonds.has(d.l.split('/')[0]));
  if(fondsChart)fondsChart.destroy();
  if(!fd.length)return;
  fondsChart=new Chart(document.getElementById('fonds-chart'),{
    type:'doughnut',
    data:{labels:fd.map(d=>d.l),datasets:[{data:fd.map(d=>d.v),backgroundColor:fd.map(d=>d.c),borderWidth:2,borderColor:isDark?'#1e2030':'#fff'}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.label}: ${c.parsed}%`}}}}
  });
  document.getElementById('fonds-legend').innerHTML=fd.map(d=>`<span><span class="sw" style="background:${d.c}"></span>${d.l} ${d.v}%</span>`).join('');
}

function renderTop10(){
  const fil=TOP10.filter(d=>activeFonds.has(d.f));
  document.getElementById('top10').innerHTML=fil.map((d,i)=>`
    <div class="ops-row">
      <span class="ops-n">${i+1}</span>
      <div class="ops-info">
        <div class="ops-name">${d.b}</div>
        <div class="ops-op">${d.op}</div>
      </div>
      <span class="pill" style="background:${FC[d.f]}22;color:${FC[d.f]}">${d.f}</span>
      <span class="ops-amt">${d.m}M€</span>
    </div>`).join('');
}

function buildScatter(){
  const pts=DEPTS.map(d=>({x:d.revenu,y:d.montant,label:d.nom,r:Math.sqrt(d.ops)*1.7}));
  new Chart(document.getElementById('scatter'),{
    type:'bubble',
    data:{datasets:[{data:pts,backgroundColor:isDark?'rgba(91,163,232,.45)':'rgba(31,78,121,.5)',borderColor:isDark?'#5ba3e8':'#1F4E79',borderWidth:1}]},
    options:{responsive:true,maintainAspectRatio:false,layout:{padding:16},
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.raw.label}: ${c.raw.y}M€ (${(c.raw.x/1000).toFixed(1)}k€)`}}},
      scales:{
        x:{title:{display:true,text:'Revenu médian (€)',color:isDark?'#7a8299':'#888',font:{size:10}},
           ticks:{callback:v=>(v/1000).toFixed(0)+'k',color:isDark?'#7a8299':'#888',font:{size:9}},
           grid:{color:gridColor}},
        y:{title:{display:true,text:'Montant EU (M€)',color:isDark?'#7a8299':'#888',font:{size:10}},
           ticks:{color:isDark?'#7a8299':'#888',font:{size:9}},
           grid:{color:gridColor}}
      }
    }
  });
}

function buildQual(){
  const mp={
    ok:{bg:'var(--ok-bg)',c:'var(--ok-fg)',l:'Très bon'},
    warn:{bg:'var(--warn-bg)',c:'var(--warn-fg)',l:'Moyen'},
    crit:{bg:'var(--crit-bg)',c:'var(--crit-fg)',l:'Critique'}
  };
  document.getElementById('qual-grid').innerHTML=QUAL.map(d=>{
    const{bg,c,l}=mp[d.niv];
    return`<div class="qcard">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">
        <div><div class="qcol">Col. ${d.col}</div><div class="qname">${d.nom}</div></div>
        <span class="qbadge" style="background:${bg};color:${c}">${l}</span>
      </div>
      <div class="qpct" style="color:${c}">${d.pct}%</div>
      <div class="qnote">${d.nan>0?d.nan+' vides — ':``}${d.note}</div>
    </div>`;
  }).join('');

  document.getElementById('anom-list').innerHTML=[
    {bc:'var(--red)',tc:'var(--crit-fg)',
     t:"Catégorie d'intervention — col. L (896 NaN)",
     d:'Première ligne vide : Excel ligne 4 · Dernière : ligne 1122<br>FSE 611 · FEDER 269 · IEJ 16 — Export incomplet depuis SYNERGIE'},
    {bc:'var(--orange)',tc:'var(--warn-fg)',
     t:'Département — col. J (10 NaN + 223 multi-depts)',
     d:'Lignes vides : 69, 83, 91, 168, 345, 430, 442, 766, 900, 1053<br>223 ops couvrant plusieurs depts (75,77,78,91,92,93,94,95)'},
    {bc:'var(--orange)',tc:'var(--warn-fg)',
     t:'Valeurs aberrantes — col. J',
     d:'Ligne 854 : 3.2153... (décimal impossible)<br>Ligne 968 : code 3 au lieu de 93 (Seine-Saint-Denis)'},
  ].map(a=>`<div class="anom" style="border-color:${a.bc}">
    <div class="anom-t" style="color:${a.tc}">${a.t}</div>
    <div class="anom-d">${a.d}</div>
  </div>`).join('');
}

function showPanel(id,btn){
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(b=>b.classList.remove('active'));
  document.getElementById('panel-'+id).classList.add('active');
  btn.classList.add('active');
}

buildMap();renderBars();renderFonds();renderTop10();buildScatter();buildQual();
</script>
"""

components.html(APP_HTML, height=1050, scrolling=True)
