import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Fonds Européens — Île-de-France",
    page_icon="🇪🇺",
    layout="wide",
)

st.markdown("""
<style>
.block-container{padding:1.2rem 2rem}
.metric-card{background:#EEF4FB;border-radius:10px;padding:14px 18px;border-left:4px solid #1F4E79}
.metric-val{font-size:26px;font-weight:600;color:#1F4E79;margin:0}
.metric-lbl{font-size:11px;color:#666;margin:0;text-transform:uppercase;letter-spacing:.05em}
.metric-sub{font-size:11px;color:#999;margin:0;margin-top:2px}
.anom{background:#FFF2CC;border-left:4px solid #C55A11;border-radius:6px;padding:10px 14px;margin-bottom:8px}
.anom-crit{background:#FFE5E5;border-left-color:#C00000}
.anom-title{font-weight:600;font-size:13px;margin-bottom:4px}
.anom-detail{font-size:12px;color:#555;line-height:1.6}
.footer{text-align:center;color:#aaa;font-size:11px;margin-top:2rem;padding-top:1rem;border-top:1px solid #eee}
</style>
""", unsafe_allow_html=True)

# ── DONNÉES ──
DEPTS = pd.DataFrame([
    {"code":"93","nom":"Seine-St-Denis","ops":217,"montant":182.2,"moy":840,"revenu":17620},
    {"code":"75","nom":"Paris",          "ops":189,"montant":123.7,"moy":654,"revenu":30880},
    {"code":"94","nom":"Val-de-Marne",   "ops":93, "montant":71.4, "moy":768,"revenu":22960},
    {"code":"95","nom":"Val-d'Oise",     "ops":108,"montant":62.7, "moy":580,"revenu":25620},
    {"code":"77","nom":"Seine-et-Marne", "ops":75, "montant":67.9, "moy":905,"revenu":24110},
    {"code":"78","nom":"Yvelines",       "ops":83, "montant":57.6, "moy":694,"revenu":27980},
    {"code":"91","nom":"Essonne",        "ops":66, "montant":59.0, "moy":893,"revenu":26085},
    {"code":"92","nom":"Hauts-de-Seine", "ops":48, "montant":40.1, "moy":836,"revenu":29250},
])
TOP10 = pd.DataFrame([
    {"benef":"BpiFrance Financement","op":"Prêts rebond FEDER IDF","montant":132.5,"fonds":"FEDER"},
    {"benef":"Région IDF","op":"REACT-EU équipements lycées","montant":105.0,"fonds":"FEDER"},
    {"benef":"Région IDF","op":"Équipements numériques lycées","montant":61.0,"fonds":"FEDER"},
    {"benef":"Conseil Régional IDF","op":"PRFE 1ère reconduction 2019","montant":51.8,"fonds":"FSE"},
    {"benef":"Conseil Régional IDF","op":"PRC 3 — 2ème reconduction","montant":50.5,"fonds":"FSE"},
    {"benef":"Conseil Régional IDF","op":"PRFE 2018 initial","montant":49.1,"fonds":"FSE"},
    {"benef":"Conseil Régional IDF","op":"PRC 4 — 1ère reconduction","montant":45.6,"fonds":"FSE"},
    {"benef":"Conseil Régional IDF","op":"Avenir Jeunes 2ème reconduction","montant":43.5,"fonds":"FSE"},
    {"benef":"BpiFrance","op":"FEDER REACT EU prêts rebond","montant":33.1,"fonds":"FEDER"},
    {"benef":"Conseil Régional IDF","op":"Paris Region Venture Fund","montant":32.8,"fonds":"FEDER"},
])
QUALITE = pd.DataFrame([
    {"col":"A","nom":"Bénéficiaire",     "pct":100.0,"niveau":"Très bon","nan":0,  "note":"558 acteurs"},
    {"col":"F","nom":"Montant EU",        "pct":100.0,"niveau":"Très bon","nan":0,  "note":"1 montant à 0"},
    {"col":"M","nom":"Fonds",             "pct":100.0,"niveau":"Très bon","nan":0,  "note":"FSE/FEDER/IEJ"},
    {"col":"D","nom":"Date début",        "pct":100.0,"niveau":"Très bon","nan":0,  "note":"ISO 2014-2022"},
    {"col":"G","nom":"Taux cofin.",       "pct":100.0,"niveau":"Très bon","nan":0,  "note":"0 à 0.70"},
    {"col":"J","nom":"Département",       "pct":99.1, "niveau":"Moyen",   "nan":10, "note":"10 vides+223 multi"},
    {"col":"H","nom":"Emplacement",       "pct":94.0, "niveau":"Moyen",   "nan":67, "note":"Parfois vide"},
    {"col":"I","nom":"ITI",               "pct":30.0, "niveau":"Faible",  "nan":784,"note":"70% vide"},
    {"col":"L","nom":"Catégorie interv.", "pct":20.1, "niveau":"Critique","nan":896,"note":"Lignes 4 à 1122"},
])
COLORS = {"FEDER":"#1F4E79","FSE":"#C55A11","IEJ":"#375623"}
NIVEAUX_COL = {"Très bon":"#375623","Moyen":"#C55A11","Faible":"#C55A11","Critique":"#C00000"}

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 🇪🇺 Fonds EU — IDF")
    st.markdown("**Période :** 2014-2020  \n**Source :** data.gouv.fr")
    st.divider()
    st.markdown("### Filtres")
    fonds_sel = st.multiselect("Fonds européen", ["FEDER","FSE","IEJ"], default=["FEDER","FSE","IEJ"])
    critere = st.radio("Classement", ["Montant (M€)","Nb opérations","Moy/op (K€)"])
    st.divider()
    st.markdown("**WADE Modou**  \nMaster 2 TNI — Paris-Saclay  \nÉtude de cas SGAE S-2026-204678")

crit_map = {"Montant (M€)":"montant","Nb opérations":"ops","Moy/op (K€)":"moy"}
crit_key = crit_map[critere]

# ── HEADER ──
c1, c2 = st.columns([4,1])
with c1:
    st.title("Fonds Européens — Île-de-France")
    st.caption("1 121 opérations · 1 669 M€ · 2014-2020 · Source data.gouv.fr")
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='background:#1F4E79;color:white;padding:7px 12px;border-radius:8px;text-align:center;font-size:12px'>SGAE · Étude de cas</div>", unsafe_allow_html=True)

st.divider()

# ── KPIs ──
k1,k2,k3,k4 = st.columns(4)
for col, lbl, val, sub in [
    (k1,"Montant total UE","1 669 M€","8 départements IDF"),
    (k2,"Opérations","1 121","879 mono-département"),
    (k3,"Bénéficiaires","558","acteurs uniques"),
    (k4,"Cohésion territoriale","r = −0.55","fonds / revenus"),
]:
    col.markdown(f"""<div class='metric-card'>
        <p class='metric-lbl'>{lbl}</p>
        <p class='metric-val'>{val}</p>
        <p class='metric-sub'>{sub}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ONGLETS ──
tab1, tab2, tab3 = st.tabs(["🗺️  Carte territoriale","📊  Opérations","🔍  Qualité des données"])

# ── TAB 1 ──
with tab1:
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("#### Classement des départements")
        data_s = DEPTS.sort_values(crit_key, ascending=True)
        vals = data_s[crit_key].values
        norm = plt.Normalize(vals.min(), vals.max())
        bar_cols = [plt.cm.Blues(norm(v)) for v in vals]

        fig, ax = plt.subplots(figsize=(6,4))
        fig.patch.set_facecolor("#F8F9FA"); ax.set_facecolor("#F8F9FA")
        bars = ax.barh(data_s["nom"], vals, color=bar_cols, edgecolor='white', height=0.65)
        for bar, v in zip(bars, vals):
            lbl = f"{v:.0f}M€" if crit_key=="montant" else f"{int(v)} ops" if crit_key=="ops" else f"{int(v)}K€"
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, lbl, va='center', fontsize=8, fontweight='bold', color='#333')
        ax.spines[['top','right','bottom']].set_visible(False)
        ax.set_xlabel(critere, fontsize=9); ax.tick_params(labelsize=9)
        ax.set_title(f"Par {critere}", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with c_right:
        st.markdown("#### Répartition par fonds")
        fd = {k:v for k,v in {"FEDER":55.0,"FSE":43.6,"IEJ":1.4}.items() if k in fonds_sel}
        if fd:
            fig2, ax2 = plt.subplots(figsize=(5,3.5))
            fig2.patch.set_facecolor("#F8F9FA")
            wcs = [COLORS[k] for k in fd]
            wedges, texts, autos = ax2.pie(list(fd.values()), labels=list(fd.keys()),
                autopct='%1.1f%%', colors=wcs, startangle=90,
                wedgeprops=dict(edgecolor='white', linewidth=2))
            for t in autos: t.set_fontsize(10); t.set_fontweight('bold'); t.set_color('white')
            ax2.set_title("Montants par fonds", fontsize=10, fontweight='bold', color='#1F4E79')
            plt.tight_layout(); st.pyplot(fig2); plt.close()
        else:
            st.info("Sélectionnez un fonds dans le menu.")

        st.markdown("#### Données")
        df_show = DEPTS[["nom","code","ops","montant","moy"]].copy()
        df_show.columns = ["Département","Code","Nb ops","Montant M€","Moy K€"]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

# ── TAB 2 ──
with tab2:
    c_top, c_scat = st.columns(2)

    with c_top:
        st.markdown("#### Top 10 financements")
        t10 = TOP10[TOP10["fonds"].isin(fonds_sel)] if fonds_sel else TOP10
        fig3, ax3 = plt.subplots(figsize=(6,4.5))
        fig3.patch.set_facecolor("#F8F9FA"); ax3.set_facecolor("#F8F9FA")
        bcs = [COLORS.get(f,"#888") for f in t10["fonds"]]
        lbls = [b[:20]+"…" if len(b)>20 else b for b in t10["benef"]]
        bars3 = ax3.barh(range(len(t10)), t10["montant"], color=bcs, edgecolor='white', height=0.65)
        ax3.set_yticks(range(len(t10))); ax3.set_yticklabels(lbls, fontsize=8); ax3.invert_yaxis()
        for bar, v in zip(bars3, t10["montant"]):
            ax3.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, f"{v}M€", va='center', fontsize=8, fontweight='bold', color='#333')
        ax3.spines[['top','right','bottom']].set_visible(False)
        leg = [mpatches.Patch(color=COLORS[f], label=f) for f in COLORS if f in fonds_sel]
        ax3.legend(handles=leg, fontsize=8)
        ax3.set_title("Top 10 par montant UE", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig3); plt.close()
        st.info("Top 10 = 607 M€ = 36% du budget total. BpiFrance et Conseil Régional IDF dominent.")

    with c_scat:
        st.markdown("#### Corrélation fonds / revenus")
        fig4, ax4 = plt.subplots(figsize=(6,4.5))
        fig4.patch.set_facecolor("#F8F9FA"); ax4.set_facecolor("#F8F9FA")
        ax4.scatter(DEPTS["revenu"], DEPTS["montant"], s=DEPTS["ops"]/1.5, color='#1F4E79', alpha=0.75, edgecolors='white', linewidth=0.8)
        for _, r in DEPTS.iterrows():
            ox = 200 if r["nom"]!="Paris" else -3800
            oy = 2 if r["nom"] not in ["Paris","Val-de-Marne"] else -7
            ax4.annotate(r["nom"], (r["revenu"],r["montant"]), xytext=(r["revenu"]+ox,r["montant"]+oy), fontsize=8, color='#333')
        z = np.polyfit(DEPTS["revenu"], DEPTS["montant"], 1)
        xl = np.linspace(DEPTS["revenu"].min()-500, DEPTS["revenu"].max()+500, 100)
        ax4.plot(xl, np.poly1d(z)(xl), "--", color="#C55A11", alpha=0.7, lw=1.5, label="Tendance (r=−0.55)")
        ax4.spines[['top','right']].set_visible(False)
        ax4.set_xlabel("Revenu médian (€)", fontsize=9)
        ax4.set_ylabel("Montant EU (M€)", fontsize=9)
        ax4.legend(fontsize=9); ax4.tick_params(labelsize=9)
        ax4.set_title("Fonds EU vs revenu médian", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig4); plt.close()
        st.warning("Paris est une anomalie : revenu élevé mais fonds importants — BpiFrance et acteurs R&D y sont domiciliés.")

# ── TAB 3 ──
with tab3:
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Champs complets","6 / 9"); m2.metric("À risque","2 / 9")
    m3.metric("Critiques","1 / 9"); m4.metric("NaN catégorie","896 / 1121")
    st.markdown("<br>", unsafe_allow_html=True)

    cq, ca = st.columns(2)
    with cq:
        st.markdown("#### Complétude par colonne")
        fig5, ax5 = plt.subplots(figsize=(6,4))
        fig5.patch.set_facecolor("#F8F9FA"); ax5.set_facecolor("#F8F9FA")
        bcs5 = [NIVEAUX_COL.get(n,"#888") for n in QUALITE["niveau"]]
        bars5 = ax5.barh(QUALITE["nom"], QUALITE["pct"], color=bcs5, edgecolor='white', height=0.65)
        ax5.axvline(100, color='#ccc', linestyle='--', lw=0.8)
        for bar, v in zip(bars5, QUALITE["pct"]):
            ax5.text(min(v+0.5,95), bar.get_y()+bar.get_height()/2, f"{v}%", va='center', fontsize=8, fontweight='bold', color='#333')
        ax5.set_xlim(0,112); ax5.invert_yaxis()
        ax5.spines[['top','right','bottom']].set_visible(False)
        ax5.set_xlabel("Complétude (%)", fontsize=9); ax5.tick_params(labelsize=9)
        from matplotlib.patches import Patch
        ax5.legend(handles=[Patch(color=v,label=k) for k,v in NIVEAUX_COL.items()], fontsize=8, loc='lower right')
        ax5.set_title("Qualité par champ", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig5); plt.close()

    with ca:
        st.markdown("#### Anomalies détectées")
        st.markdown("""
        <div class='anom anom-crit'>
        <div class='anom-title' style='color:#C00000'>Catégorie d'intervention — col. L (896 NaN)</div>
        <div class='anom-detail'>Première ligne vide : Excel ligne 4 · Dernière : ligne 1122<br>
        FSE 611 · FEDER 269 · IEJ 16<br>
        Cause : export incomplet depuis SYNERGIE</div>
        </div>
        <div class='anom'>
        <div class='anom-title' style='color:#C55A11'>Département — col. J (10 NaN + 223 multi)</div>
        <div class='anom-detail'>Lignes vides : 69, 83, 91, 168, 345, 430, 442, 766, 900, 1053<br>
        223 ops multi-depts (ex : 75,77,78,91,92,93,94,95)</div>
        </div>
        <div class='anom'>
        <div class='anom-title' style='color:#C55A11'>Valeurs aberrantes — col. J</div>
        <div class='anom-detail'>Ligne 854 : 3.2153... (décimal impossible)<br>
        Ligne 968 : code 3 au lieu de 93 (Seine-Saint-Denis)</div>
        </div>
        <div style='background:#EEF4FB;border-radius:8px;padding:10px 14px;border-left:4px solid #1F4E79;font-size:12px;margin-top:8px'>
        <strong style='color:#1F4E79'>Recommandation</strong><br>
        Enrichir via data warehouse SYNERGIE · Catégorie obligatoire à la saisie · Normaliser bénéficiaires par SIRET/SIREN
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='footer'>WADE Modou · Master 2 TNI Paris-Saclay · SGAE S-2026-204678 · 2026</div>", unsafe_allow_html=True)
