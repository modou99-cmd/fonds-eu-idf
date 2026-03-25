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

APP_HTML = r"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
body{background:#f7f8fa;color:#1a1a2e;padding:16px}
.topbar{display:flex;align-items:center;justify-content:space-between;background:white;border-radius:12px;padding:16px 20px;margin-bottom:12px;border:1px solid #e8eaf0}
.topbar h1{font-size:17px;font-weight:700;color:#1F4E79}
.topbar p{font-size:12px;color:#888;margin-top:3px}
.badge{background:#1F4E79;color:white;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px}
.kpi{background:white;border-radius:12px;padding:14px 16px;border:1px solid #e8eaf0;border-left:4px solid #1F4E79}
.kpi-lbl{font-size:10px;color:#888;text-transform:uppercase;letter-spacing:.06em;margin-bottom:5px}
.kpi-val{font-size:22px;font-weight:700;color:#1F4E79}
.kpi-sub{font-size:10px;color:#aaa;margin-top:2px}
.nav{display:flex;background:white;border-radius:12px;border:1px solid #e8eaf0;overflow:hidden;margin-bottom:12px}
.nav-btn{flex:1;padding:12px;text-align:center;cursor:pointer;font-size:13px;font-weight:500;color:#888;border:none;background:none;border-bottom:3px solid transparent;transition:all .2s}
.nav-btn.active{color:#1F4E79;border-bottom-color:#1F4E79;background:#f0f5fb}
.nav-btn:hover:not(.active){background:#f7f8fa}
.panel{display:none}.panel.active{display:block}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.card{background:white;border-radius:12px;border:1px solid #e8eaf0;padding:16px}
.card-title{font-size:11px;font-weight:700;color:#888;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px}
.seg{display:inline-flex;background:#f0f2f5;border-radius:8px;padding:3px;margin-bottom:12px}
.seg-btn{font-size:12px;padding:5px 12px;border-radius:6px;border:none;background:none;cursor:pointer;color:#666;font-weight:500;transition:all .15s}
.seg-btn.active{background:white;color:#1F4E79;font-weight:700;box-shadow:0 1px 4px rgba(0,0,0,.1)}
.bar-row{display:flex;align-items:center;gap:8px;margin-bottom:7px}
.bar-lbl{font-size:11px;color:#555;width:115px;text-align:right;flex-shrink:0}
.bar-bg{flex:1;background:#f0f2f5;border-radius:4px;height:16px}
.bar-fill{height:16px;border-radius:4px;transition:width .35s cubic-bezier(.4,0,.2,1)}
.bar-val{font-size:11px;font-weight:700;color:#555;width:56px;text-align:right}
.tt{position:fixed;background:white;border:1px solid #e8eaf0;border-radius:10px;padding:12px 16px;pointer-events:none;display:none;z-index:9999;min-width:165px;box-shadow:0 4px 20px rgba(0,0,0,.12)}
.tt-name{font-size:13px;font-weight:700;color:#1F4E79;margin-bottom:8px}
.tt-row{display:flex;justify-content:space-between;gap:16px;margin-top:4px}
.tt-k{color:#aaa;font-size:11px}.tt-v{color:#1a1a2e;font-size:11px;font-weight:700}
.ops-row{display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid #f5f5f5}
.ops-row:last-child{border:none}
.ops-rank{font-size:11px;color:#ccc;width:16px;flex-shrink:0}
.ops-info{flex:1;min-width:0}
.ops-name{font-size:12px;color:#333;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ops-op{font-size:11px;color:#bbb;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:1px}
.pill{font-size:10px;font-weight:700;padding:3px 8px;border-radius:20px;flex-shrink:0}
.ops-amt{font-size:13px;font-weight:700;color:#1F4E79;width:54px;text-align:right;flex-shrink:0}
.qual-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.qcard{border:1px solid #e8eaf0;border-radius:10px;padding:10px 12px}
.qcol{font-size:10px;color:#aaa;font-weight:700}
.qname{font-size:12px;font-weight:700;color:#1a1a2e;margin-top:1px}
.qpct{font-size:20px;font-weight:700;margin:5px 0 2px}
.qnote{font-size:10px;color:#888}
.anom{border-radius:10px;padding:10px 13px;margin-bottom:8px}
.anom-t{font-size:12px;font-weight:700;margin-bottom:4px}
.anom-d{font-size:11px;line-height:1.6;color:#555}
.rec{background:#f0f5fb;border-radius:10px;padding:12px 14px;border-left:4px solid #1F4E79;margin-top:10px}
.rec-t{font-size:12px;font-weight:700;color:#1F4E79;margin-bottom:3px}
.rec-d{font-size:11px;color:#555;line-height:1.6}
.legend{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px;font-size:11px;color:#666;align-items:center}
.sw{width:10px;height:10px;border-radius:2px;display:inline-block;margin-right:3px;vertical-align:middle}
.sbox{background:#f7f8fa;border-radius:10px;padding:12px;text-align:center;border:1px solid #e8eaf0}
.sn{font-size:20px;font-weight:700}.sl{font-size:10px;color:#888;margin-top:2px}
</style></head>
<body>
<div class="topbar">
  <div><h1>Fonds Européens — Île-de-France</h1>
  <p>1 121 opérations &nbsp;·&nbsp; 1 669 M€ &nbsp;·&nbsp; 2014-2020 &nbsp;·&nbsp; data.gouv.fr</p></div>
  <span class="badge">SGAE · Étude de cas</span>
</div>
<div class="kpis">
  <div class="kpi"><div class="kpi-lbl">Montant total UE</div><div class="kpi-val">1 669 M€</div><div class="kpi-sub">8 départements IDF</div></div>
  <div class="kpi"><div class="kpi-lbl">Opérations</div><div class="kpi-val">1 121</div><div class="kpi-sub">879 mono-département</div></div>
  <div class="kpi"><div class="kpi-lbl">Bénéficiaires</div><div class="kpi-val">558</div><div class="kpi-sub">acteurs uniques</div></div>
  <div class="kpi" style="border-left-color:#C55A11"><div class="kpi-lbl">Cohésion territoriale</div><div class="kpi-val" style="color:#C55A11">r = −0.55</div><div class="kpi-sub">fonds / revenus médians</div></div>
</div>
<div class="nav">
  <button class="nav-btn active" onclick="showPanel('carte',this)">🗺️  Carte territoriale</button>
  <button class="nav-btn" onclick="showPanel('ops',this)">📊  Opérations</button>
  <button class="nav-btn" onclick="showPanel('qual',this)">🔍  Qualité des données</button>
</div>

<div id="panel-carte" class="panel active">
  <div class="two-col">
    <div class="card" style="position:relative">
      <div class="card-title">Répartition par département</div>
      <svg id="idf-map" viewBox="0 0 300 320" style="width:100%;height:290px"></svg>
      <div class="legend" id="map-legend"></div>
    </div>
    <div class="card">
      <div class="card-title">Classement</div>
      <div class="seg">
        <button class="seg-btn active" onclick="setSort('montant',this)">Montant</button>
        <button class="seg-btn" onclick="setSort('ops',this)">Opérations</button>
        <button class="seg-btn" onclick="setSort('moy',this)">Moy/op</button>
      </div>
      <div id="bar-chart"></div>
      <div style="margin-top:14px;padding-top:12px;border-top:1px solid #f5f5f5">
        <div class="card-title">Répartition par fonds</div>
        <div style="position:relative;height:160px"><canvas id="fonds-chart"></canvas></div>
        <div id="fonds-legend" class="legend"></div>
      </div>
    </div>
  </div>
</div>

<div id="panel-ops" class="panel">
  <div class="two-col">
    <div class="card">
      <div class="card-title">Top 10 — financements les plus importants</div>
      <div id="top10"></div>
    </div>
    <div class="card">
      <div class="card-title">Corrélation fonds EU / revenu médian</div>
      <div style="position:relative;height:250px"><canvas id="scatter"></canvas></div>
      <div style="margin-top:10px;background:#fff8ec;border-radius:8px;padding:10px 12px;border-left:3px solid #C55A11;font-size:11px;color:#555;line-height:1.6">
        <strong style="color:#C55A11">r = −0.55.</strong> Les depts pauvres reçoivent plus. <strong>Paris :</strong> anomalie — BpiFrance et R&D domiciliés en 75.
      </div>
    </div>
  </div>
</div>

<div id="panel-qual" class="panel">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px">
    <div class="sbox"><div class="sn" style="color:#375623">5</div><div class="sl">Champs complets</div></div>
    <div class="sbox"><div class="sn" style="color:#C55A11">2</div><div class="sl">À surveiller</div></div>
    <div class="sbox"><div class="sn" style="color:#C00000">2</div><div class="sl">Critiques</div></div>
    <div class="sbox"><div class="sn">896</div><div class="sl">NaN catégorie</div></div>
  </div>
  <div class="two-col">
    <div class="card">
      <div class="card-title">Complétude par champ</div>
      <div class="qual-grid" id="qual-grid"></div>
    </div>
    <div class="card">
      <div class="card-title">Anomalies détectées</div>
      <div id="anom-list"></div>
    </div>
  </div>
</div>

<div class="tt" id="tooltip"></div>

<script>
const D=[
  {code:'93',nom:'Seine-St-Denis',ops:217,montant:182.2,moy:840,revenu:17620},
  {code:'75',nom:'Paris',         ops:189,montant:123.7,moy:654,revenu:30880},
  {code:'94',nom:'Val-de-Marne',  ops:93, montant:71.4, moy:768,revenu:22960},
  {code:'95',nom:"Val-d'Oise",    ops:108,montant:62.7, moy:580,revenu:25620},
  {code:'77',nom:'Seine-et-Marne',ops:75, montant:67.9, moy:905,revenu:24110},
  {code:'78',nom:'Yvelines',      ops:83, montant:57.6, moy:694,revenu:27980},
  {code:'91',nom:'Essonne',       ops:66, montant:59.0, moy:893,revenu:26085},
  {code:'92',nom:'Hauts-de-Seine',ops:48, montant:40.1, moy:836,revenu:29250},
];
const T=[
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
const Q=[
  {col:'A',nom:'Bénéficiaire',    pct:100, niv:'ok',  nan:0,  note:'558 acteurs'},
  {col:'F',nom:'Montant EU',       pct:100, niv:'ok',  nan:0,  note:'1 montant à 0'},
  {col:'M',nom:'Fonds',            pct:100, niv:'ok',  nan:0,  note:'FSE/FEDER/IEJ'},
  {col:'D',nom:'Date début',       pct:100, niv:'ok',  nan:0,  note:'ISO 2014-2022'},
  {col:'G',nom:'Taux cofin.',      pct:100, niv:'ok',  nan:0,  note:'0 à 0.70'},
  {col:'J',nom:'Département',      pct:99.1,niv:'warn',nan:10, note:'10 vides+223 multi'},
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
const maxM=Math.max(...D.map(d=>d.montant));
const cs=d3.scaleSequential([0,maxM],d3.interpolateBlues);
const tt=document.getElementById('tooltip');

function bbox(d){const n=d.match(/-?\d+\.?\d*/g).map(Number),xs=[],ys=[];for(let i=0;i<n.length;i+=2){xs.push(n[i]);ys.push(n[i+1]);}return{cx:(Math.min(...xs)+Math.max(...xs))/2,cy:(Math.min(...ys)+Math.max(...ys))/2};}

function buildMap(){
  const svg=document.getElementById('idf-map');
  D.forEach(dept=>{
    const p=document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d',PATHS[dept.code]);p.setAttribute('fill',cs(dept.montant));
    p.setAttribute('stroke','#fff');p.setAttribute('stroke-width','2');
    p.style.cssText='cursor:pointer;transition:opacity .15s';
    const bb=bbox(PATHS[dept.code]);
    const t=document.createElementNS('http://www.w3.org/2000/svg','text');
    t.setAttribute('x',bb.cx);t.setAttribute('y',bb.cy);
    t.setAttribute('text-anchor','middle');t.setAttribute('dominant-baseline','middle');
    t.setAttribute('font-size','9');t.setAttribute('font-weight','700');
    t.setAttribute('fill','#fff');t.setAttribute('pointer-events','none');
    t.textContent=dept.code;
    p.onmousemove=e=>{
      tt.style.display='block';tt.style.left=(e.clientX+14)+'px';tt.style.top=(e.clientY-10)+'px';
      tt.innerHTML=`<div class="tt-name">${dept.nom} (${dept.code})</div>
        <div class="tt-row"><span class="tt-k">Montant EU</span><span class="tt-v">${dept.montant} M€</span></div>
        <div class="tt-row"><span class="tt-k">Opérations</span><span class="tt-v">${dept.ops}</span></div>
        <div class="tt-row"><span class="tt-k">Moy/opération</span><span class="tt-v">${dept.moy} K€</span></div>
        <div class="tt-row"><span class="tt-k">Revenu médian</span><span class="tt-v">${dept.revenu.toLocaleString('fr')} €</span></div>`;
    };
    p.onmouseleave=()=>{p.style.opacity='1';tt.style.display='none';};
    p.onmouseenter=()=>p.style.opacity='.72';
    svg.appendChild(p);svg.appendChild(t);
  });
  const leg=document.getElementById('map-legend');
  [0,50,100,150].forEach((v,i,a)=>{
    const s=document.createElement('span');
    s.innerHTML=`<span class="sw" style="background:${cs(v+25)}"></span>${v}–${a[i+1]||182} M€`;
    leg.appendChild(s);
  });
}

let sk='montant';
function setSort(k,btn){sk=k;document.querySelectorAll('.seg-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');renderBars();}
function renderBars(){
  const s=[...D].sort((a,b)=>b[sk]-a[sk]);const mv=Math.max(...s.map(d=>d[sk]));
  const cc={montant:'#1F4E79',ops:'#C55A11',moy:'#375623'};
  const fmt=v=>sk==='montant'?v+'M€':sk==='ops'?v+' ops':v+'K€';
  document.getElementById('bar-chart').innerHTML=s.map(d=>{const v=d[sk];
    return`<div class="bar-row"><div class="bar-lbl">${d.nom}</div><div class="bar-bg"><div class="bar-fill" style="width:${Math.round(v/mv*100)}%;background:${cc[sk]}"></div></div><div class="bar-val">${fmt(v)}</div></div>`;
  }).join('');
}

function buildFonds(){
  const fd=[{l:'FEDER',v:55.0,c:'#1F4E79'},{l:'FSE/FSE+',v:43.6,c:'#C55A11'},{l:'IEJ',v:1.4,c:'#375623'}];
  new Chart(document.getElementById('fonds-chart'),{type:'doughnut',data:{labels:fd.map(d=>d.l),datasets:[{data:fd.map(d=>d.v),backgroundColor:fd.map(d=>d.c),borderWidth:3,borderColor:'#fff'}]},options:{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{legend:{display:false}}}});
  document.getElementById('fonds-legend').innerHTML=fd.map(d=>`<span><span class="sw" style="background:${d.c}"></span>${d.l} ${d.v}%</span>`).join('');
}

function buildTop10(){
  document.getElementById('top10').innerHTML=T.map((d,i)=>`<div class="ops-row"><span class="ops-rank">${i+1}</span><div class="ops-info"><div class="ops-name">${d.b}</div><div class="ops-op">${d.op}</div></div><span class="pill" style="background:${FC[d.f]}18;color:${FC[d.f]}">${d.f}</span><span class="ops-amt">${d.m}M€</span></div>`).join('');
}

function buildScatter(){
  const pts=D.map(d=>({x:d.revenu,y:d.montant,label:d.nom,r:Math.sqrt(d.ops)*1.8}));
  new Chart(document.getElementById('scatter'),{type:'bubble',data:{datasets:[{data:pts,backgroundColor:'#1F4E7988',borderColor:'#1F4E79',borderWidth:1}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.raw.label}: ${c.raw.y}M€`}}},scales:{x:{title:{display:true,text:'Revenu médian (€)',font:{size:10}},ticks:{callback:v=>(v/1000).toFixed(0)+'k',font:{size:9}}},y:{title:{display:true,text:'Montant EU (M€)',font:{size:10}},ticks:{font:{size:9}}}}}});
}

function buildQual(){
  const mp={ok:{bg:'#edfaf3',c:'#375623',l:'Très bon'},warn:{bg:'#fff8ec',c:'#C55A11',l:'Moyen'},crit:{bg:'#fff0f0',c:'#C00000',l:'Critique'}};
  document.getElementById('qual-grid').innerHTML=Q.map(d=>{const{bg,c,l}=mp[d.niv];return`<div class="qcard" style="background:${bg};border-color:${c}33"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><div><div class="qcol">Col. ${d.col}</div><div class="qname">${d.nom}</div></div><span style="font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;background:${c}18;color:${c}">${l}</span></div><div class="qpct" style="color:${c}">${d.pct}%</div><div class="qnote">${d.nan>0?d.nan+' vides — ':``}${d.note}</div></div>`;}).join('');
  document.getElementById('anom-list').innerHTML=[
    {bg:'#fff0f0',bc:'#C00000',tc:'#C00000',t:"Catégorie d'intervention — col. L (896 NaN)",d:"Première ligne vide : Excel ligne 4 · Dernière : ligne 1122<br>FSE 611 · FEDER 269 · IEJ 16<br><strong>Cause :</strong> export incomplet depuis SYNERGIE"},
    {bg:'#fff8ec',bc:'#C55A11',tc:'#C55A11',t:'Département — col. J (10 NaN + 223 multi)',d:'Lignes vides : 69, 83, 91, 168, 345, 430, 442, 766, 900, 1053<br>223 ops multi-depts (75,77,78,91,92,93,94,95)'},
    {bg:'#fff8ec',bc:'#C55A11',tc:'#C55A11',t:'Valeurs aberrantes — col. J',d:'Ligne 854 : 3.2153... (décimal impossible)<br>Ligne 968 : code 3 au lieu de 93'},
  ].map(a=>`<div class="anom" style="background:${a.bg};border-left:4px solid ${a.bc}"><div class="anom-t" style="color:${a.tc}">${a.t}</div><div class="anom-d">${a.d}</div></div>`).join('')
  +`<div class="rec"><div class="rec-t">Recommandation principale</div><div class="rec-d">Enrichir via SYNERGIE · Catégorie obligatoire à la saisie · Normaliser bénéficiaires par SIRET/SIREN</div></div>`;
}

function showPanel(id,btn){
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('panel-'+id).classList.add('active');btn.classList.add('active');
}

buildMap();renderBars();buildFonds();buildTop10();buildScatter();buildQual();
</script></body></html>
"""

components.html(APP_HTML, height=1050, scrolling=True)
