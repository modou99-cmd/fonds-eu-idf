import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Fonds Européens — IDF",
    page_icon="🇪🇺",
    layout="wide",
)

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
    {"Bénéficiaire":"BpiFrance Financement","Opération":"Prêts rebond FEDER IDF","Montant (M€)":132.5,"Fonds":"FEDER"},
    {"Bénéficiaire":"Région IDF","Opération":"REACT-EU équipements lycées","Montant (M€)":105.0,"Fonds":"FEDER"},
    {"Bénéficiaire":"Région IDF","Opération":"Équipements numériques lycées","Montant (M€)":61.0,"Fonds":"FEDER"},
    {"Bénéficiaire":"Conseil Régional IDF","Opération":"PRFE 1ère reconduction 2019","Montant (M€)":51.8,"Fonds":"FSE"},
    {"Bénéficiaire":"Conseil Régional IDF","Opération":"PRC 3 — 2ème reconduction","Montant (M€)":50.5,"Fonds":"FSE"},
    {"Bénéficiaire":"Conseil Régional IDF","Opération":"PRFE 2018 initial","Montant (M€)":49.1,"Fonds":"FSE"},
    {"Bénéficiaire":"Conseil Régional IDF","Opération":"PRC 4 — 1ère reconduction","Montant (M€)":45.6,"Fonds":"FSE"},
    {"Bénéficiaire":"Conseil Régional IDF","Opération":"Avenir Jeunes 2ème reconduction","Montant (M€)":43.5,"Fonds":"FSE"},
    {"Bénéficiaire":"BpiFrance","Opération":"FEDER REACT EU prêts rebond","Montant (M€)":33.1,"Fonds":"FEDER"},
    {"Bénéficiaire":"Conseil Régional IDF","Opération":"Paris Region Venture Fund","Montant (M€)":32.8,"Fonds":"FEDER"},
])

QUALITE = pd.DataFrame([
    {"Colonne":"A","Champ":"Bénéficiaire",     "Complétude (%)":100.0,"Niveau":"✅ Très bon","NaN":0,   "Note":"558 acteurs distincts"},
    {"Colonne":"F","Champ":"Montant EU",        "Complétude (%)":100.0,"Niveau":"✅ Très bon","NaN":0,   "Note":"1 montant à 0 EUR"},
    {"Colonne":"M","Champ":"Fonds",             "Complétude (%)":100.0,"Niveau":"✅ Très bon","NaN":0,   "Note":"FSE / FEDER / IEJ"},
    {"Colonne":"D","Champ":"Date début",        "Complétude (%)":100.0,"Niveau":"✅ Très bon","NaN":0,   "Note":"Format ISO 2014-2022"},
    {"Colonne":"G","Champ":"Taux cofin.",       "Complétude (%)":100.0,"Niveau":"✅ Très bon","NaN":0,   "Note":"0 à 0.70"},
    {"Colonne":"J","Champ":"Département",       "Complétude (%)":99.1, "Niveau":"⚠️ Moyen",  "NaN":10,  "Note":"10 vides + 223 multi-depts"},
    {"Colonne":"H","Champ":"Emplacement",       "Complétude (%)":94.0, "Niveau":"⚠️ Moyen",  "NaN":67,  "Note":"Parfois non renseigné"},
    {"Colonne":"I","Champ":"ITI",               "Complétude (%)":30.0, "Niveau":"🔶 Faible", "NaN":784, "Note":"70% vide"},
    {"Colonne":"L","Champ":"Catégorie interv.", "Complétude (%)":20.1, "Niveau":"❌ Critique","NaN":896, "Note":"Lignes Excel 4 à 1122"},
])

COLORS = {"FEDER":"#1F4E79","FSE":"#C55A11","IEJ":"#375623"}

# ── SIDEBAR ──
with st.sidebar:
    st.title("🇪🇺 Fonds EU — IDF")
    st.caption("Période 2014-2020 · Source data.gouv.fr")
    st.divider()
    st.subheader("Filtres")
    fonds_sel = st.multiselect(
        "Fonds européen",
        ["FEDER", "FSE", "IEJ"],
        default=["FEDER", "FSE", "IEJ"]
    )
    critere = st.radio(
        "Critère de classement",
        ["Montant total (M€)", "Nb opérations", "Montant moyen (K€)"]
    )
    st.divider()
    st.caption("**WADE Modou**  \nMaster 2 TNI — Paris-Saclay  \nÉtude de cas SGAE S-2026-204678")

crit_map = {"Montant total (M€)":"montant","Nb opérations":"ops","Montant moyen (K€)":"moy"}
crit_key = crit_map[critere]

# ── HEADER ──
st.title("🇪🇺 Fonds Européens — Île-de-France")
st.caption("1 121 opérations · 1 669 M€ · Période 2014-2020 · Source : data.gouv.fr")
st.divider()

# ── KPIs natifs Streamlit ──
k1, k2, k3, k4 = st.columns(4)
k1.metric("💶 Montant total UE",    "1 669 M€",  "8 départements IDF")
k2.metric("📁 Opérations",          "1 121",      "879 mono-département")
k3.metric("👤 Bénéficiaires",       "558",        "acteurs uniques")
k4.metric("📊 Corrélation INSEE",   "r = −0.55",  "fonds / revenus médians")

st.divider()

# ── ONGLETS ──
tab1, tab2, tab3 = st.tabs([
    "🗺️  Carte territoriale",
    "📊  Opérations & financements",
    "🔍  Qualité des données"
])

# ════════════════════════════════════
# ONGLET 1 — CARTE TERRITORIALE
# ════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Classement des départements")
        data_s = DEPTS.sort_values(crit_key, ascending=True)
        vals = data_s[crit_key].values
        norm = plt.Normalize(vals.min(), vals.max())
        bar_cols = [plt.cm.Blues(norm(v)) for v in vals]

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor("#F8F9FA"); ax.set_facecolor("#F8F9FA")
        bars = ax.barh(data_s["nom"], vals, color=bar_cols, edgecolor='white', height=0.65)
        for bar, v in zip(bars, vals):
            lbl = f"{v:.0f}M€" if crit_key=="montant" else f"{int(v)} ops" if crit_key=="ops" else f"{int(v)}K€"
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                    lbl, va='center', fontsize=8, fontweight='bold', color='#333')
        ax.spines[['top','right','bottom']].set_visible(False)
        ax.set_xlabel(critere, fontsize=9); ax.tick_params(labelsize=9)
        ax.set_title(f"Par {critere}", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with c2:
        st.subheader("Répartition par fonds")
        fd = {k:v for k,v in {"FEDER":55.0,"FSE":43.6,"IEJ":1.4}.items() if k in fonds_sel}
        if fd:
            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            fig2.patch.set_facecolor("#F8F9FA")
            wcs = [COLORS[k] for k in fd]
            wedges, texts, autos = ax2.pie(
                list(fd.values()), labels=list(fd.keys()),
                autopct='%1.1f%%', colors=wcs, startangle=90,
                wedgeprops=dict(edgecolor='white', linewidth=2))
            for t in autos:
                t.set_fontsize(10); t.set_fontweight('bold'); t.set_color('white')
            ax2.set_title("Montants par fonds", fontsize=10, fontweight='bold', color='#1F4E79')
            plt.tight_layout(); st.pyplot(fig2); plt.close()
        else:
            st.info("Sélectionnez au moins un fonds.")

        st.subheader("Tableau récapitulatif")
        df_show = DEPTS[["nom","code","ops","montant","moy"]].copy()
        df_show.columns = ["Département","Code","Nb ops","Montant M€","Moy K€"]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

# ════════════════════════════════════
# ONGLET 2 — OPÉRATIONS
# ════════════════════════════════════
with tab2:
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Top 10 — Financements les plus importants")
        t10 = TOP10[TOP10["Fonds"].isin(fonds_sel)] if fonds_sel else TOP10

        fig3, ax3 = plt.subplots(figsize=(6, 4.5))
        fig3.patch.set_facecolor("#F8F9FA"); ax3.set_facecolor("#F8F9FA")
        bcs = [COLORS.get(f,"#888") for f in t10["Fonds"]]
        lbls = [b[:20]+"…" if len(b)>20 else b for b in t10["Bénéficiaire"]]
        bars3 = ax3.barh(range(len(t10)), t10["Montant (M€)"], color=bcs, edgecolor='white', height=0.65)
        ax3.set_yticks(range(len(t10))); ax3.set_yticklabels(lbls, fontsize=8)
        ax3.invert_yaxis()
        for bar, v in zip(bars3, t10["Montant (M€)"]):
            ax3.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                     f"{v}M€", va='center', fontsize=8, fontweight='bold', color='#333')
        ax3.spines[['top','right','bottom']].set_visible(False)
        leg = [mpatches.Patch(color=COLORS[f], label=f) for f in COLORS if f in fonds_sel]
        ax3.legend(handles=leg, fontsize=8)
        ax3.set_title("Top 10 par montant UE", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig3); plt.close()

        st.info("📌 Top 10 = 607 M€ = 36% du budget total.")

    with c4:
        st.subheader("Corrélation fonds EU / revenu médian")
        fig4, ax4 = plt.subplots(figsize=(6, 4.5))
        fig4.patch.set_facecolor("#F8F9FA"); ax4.set_facecolor("#F8F9FA")
        ax4.scatter(DEPTS["revenu"], DEPTS["montant"],
                    s=DEPTS["ops"]/1.5, color='#1F4E79',
                    alpha=0.75, edgecolors='white', linewidth=0.8)
        for _, r in DEPTS.iterrows():
            ox = 200 if r["nom"]!="Paris" else -3800
            oy = 2 if r["nom"] not in ["Paris","Val-de-Marne"] else -7
            ax4.annotate(r["nom"], (r["revenu"], r["montant"]),
                         xytext=(r["revenu"]+ox, r["montant"]+oy), fontsize=8, color='#333')
        z = np.polyfit(DEPTS["revenu"], DEPTS["montant"], 1)
        xl = np.linspace(DEPTS["revenu"].min()-500, DEPTS["revenu"].max()+500, 100)
        ax4.plot(xl, np.poly1d(z)(xl), "--", color="#C55A11",
                 alpha=0.7, lw=1.5, label="Tendance (r = −0.55)")
        ax4.spines[['top','right']].set_visible(False)
        ax4.set_xlabel("Revenu médian (€)", fontsize=9)
        ax4.set_ylabel("Montant EU (M€)", fontsize=9)
        ax4.legend(fontsize=9); ax4.tick_params(labelsize=9)
        ax4.set_title("Fonds EU vs revenu médian", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig4); plt.close()

        st.warning("⚠️ Paris : anomalie — revenu élevé mais fonds importants (BpiFrance domicilié à Paris).")

# ════════════════════════════════════
# ONGLET 3 — QUALITÉ
# ════════════════════════════════════
with tab3:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("✅ Champs complets", "5 / 9")
    m2.metric("⚠️ À surveiller",    "2 / 9")
    m3.metric("❌ Critiques",        "1 / 9")
    m4.metric("🔴 NaN catégorie",   "896 / 1121")

    st.divider()
    c5, c6 = st.columns(2)

    with c5:
        st.subheader("Complétude par colonne")
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        fig5.patch.set_facecolor("#F8F9FA"); ax5.set_facecolor("#F8F9FA")
        col_colors = {"✅ Très bon":"#375623","⚠️ Moyen":"#C55A11","🔶 Faible":"#E8A020","❌ Critique":"#C00000"}
        bcs5 = [col_colors.get(n,"#888") for n in QUALITE["Niveau"]]
        bars5 = ax5.barh(QUALITE["Champ"], QUALITE["Complétude (%)"],
                         color=bcs5, edgecolor='white', height=0.65)
        ax5.axvline(100, color='#ccc', linestyle='--', lw=0.8)
        for bar, v in zip(bars5, QUALITE["Complétude (%)"]):
            ax5.text(min(v+0.5, 95), bar.get_y()+bar.get_height()/2,
                     f"{v}%", va='center', fontsize=8, fontweight='bold', color='#333')
        ax5.set_xlim(0, 112); ax5.invert_yaxis()
        ax5.spines[['top','right','bottom']].set_visible(False)
        ax5.set_xlabel("Complétude (%)", fontsize=9); ax5.tick_params(labelsize=9)
        from matplotlib.patches import Patch
        ax5.legend(handles=[Patch(color=v, label=k) for k,v in col_colors.items()],
                   fontsize=8, loc='lower right')
        ax5.set_title("Qualité par champ", fontsize=10, fontweight='bold', color='#1F4E79')
        plt.tight_layout(); st.pyplot(fig5); plt.close()

        st.subheader("Tableau qualité complet")
        st.dataframe(QUALITE[["Colonne","Champ","Complétude (%)","Niveau","NaN","Note"]],
                     use_container_width=True, hide_index=True)

    with c6:
        st.subheader("Anomalies détectées")

        st.error("""
**❌ Catégorie d'intervention — col. L (896 NaN)**

Première ligne vide : Excel ligne 4 · Dernière : ligne 1122

FSE 611 vides · FEDER 269 · IEJ 16

Cause : export incomplet depuis SYNERGIE — données présentes dans le SI mais non exportées.
        """)

        st.warning("""
**⚠️ Département — col. J (10 NaN + 223 multi-depts)**

Lignes vides : 69, 83, 91, 168, 345, 430, 442, 766, 900, 1053

223 opérations couvrant plusieurs départements (ex : 75,77,78,91,92,93,94,95)

Empêche toute agrégation territoriale fiable.
        """)

        st.warning("""
**⚠️ Valeurs aberrantes — col. J**

Ligne 854 : département = 3.2153… (nombre décimal impossible)

Ligne 968 : code 3 au lieu de 93 (Seine-Saint-Denis)

7 autres codes hors IDF légitimes (projets bassin versant Seine).
        """)

        st.info("""
**💡 Recommandation principale**

Enrichir l'export via le data warehouse SYNERGIE pour récupérer les codes de catégorie d'intervention.
Mettre le champ obligatoire à la saisie. Normaliser les bénéficiaires par SIRET/SIREN.
Implémenter une liste blanche INSEE pour les codes département.
        """)

st.divider()
st.caption("WADE Modou · Master 2 TNI Paris-Saclay · SGAE S-2026-204678 · 2026")
