# pages/1_📊_Dataset_i_Grafics.py
import streamlit as st
import pandas as pd
import unicodedata
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="📊 Anàlisi del Dataset", layout="wide")
st.title("📊 Anàlisi del dataset i gràfics")

# ---------------- utilitats per normalitzar columnes ----------------
def normalize_name(s):
    if not isinstance(s, str):
        return ""
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s

keyword_map = {
    "edat": "edat", "sexe": "sexe", "clor": "clor", "suor": "clor",
    "mutacio": "mutacio", "cftr": "mutacio", "fev1": "fev1",
    "pancrea": "pancreas", "pancreas": "pancreas",
    "pseudomon": "pseudomonas", "staphyl": "staphylococcus",
    "haemophil": "haemophilus", "burk": "burkholderia",
    "stenotrophomonas": "stenotrophomonas", "asperg": "aspergillus",
    "cap": "cap_infeccio", "fvc": "fvc", "imc": "imc",
    "exarce": "exacerbacions", "exacer": "exacerbacions",
    "pes": "pes", "polip": "polips", "reflux": "reflux",
    "satur": "saturacio", "sibil": "sibilancies",
    "sinus": "sinusitis", "diagnostic": "diagnostic",
    "diagnosticfq": "diagnostic", "talla": "talla", "tos": "tos"
}

# ---------------- carregar dataset (des del repositori o pujat) ----------------
uploaded = st.file_uploader("(Opcional) Pujar dataset (Excel) — si no, s'usa dataset_fq.xlsx del repositori", type=["xlsx"])
if uploaded is not None:
    df_raw = pd.read_excel(uploaded)
else:
    try:
        df_raw = pd.read_excel("dataset_fq.xlsx")
    except Exception as e:
        st.error("No s'ha trobat 'dataset_fq.xlsx'. Puja el fitxer o comprova el repositori.")
        st.stop()

st.subheader("Visió general")
st.write("Columnes originals detectades:")
st.write(list(df_raw.columns))

# normalitzar noms i mapar a canònics
norm_map = {orig: normalize_name(orig) for orig in df_raw.columns}
final_map = {}
used = set()
for orig, norm in norm_map.items():
    chosen = None
    for key, canon in keyword_map.items():
        if key in norm and canon not in used:
            chosen = canon
            break
    if chosen is None:
        chosen = norm
    final_map[orig] = chosen
    used.add(chosen)

df = df_raw.rename(columns=final_map)
df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

st.write("Columnes normalitzades i usades:")
st.write(list(df.columns))

# ---------------- gràfics ----------------
st.markdown("---")
st.subheader("Distribucions i comparacions")

# Comptatge diagnòstic
if "diagnostic" in df.columns:
    fig1, ax1 = plt.subplots(figsize=(4,3))
    sns.countplot(x=df["diagnostic"], ax=ax1)
    ax1.set_xlabel("Diagnòstic (0 = No, 1 = Sí)")
    ax1.set_title("Distribució del diagnòstic")
    st.pyplot(fig1)
else:
    st.info("La columna 'diagnostic' no existeix; no es poden generar certes comparacions.")

# Boxplots per clor i FEV1 si existeixen
cols_to_plot = []
if "clor" in df.columns: cols_to_plot.append("clor")
if "fev1" in df.columns: cols_to_plot.append("fev1")
if len(cols_to_plot):
    st.subheader("Boxplots per diagnòstic")
    for c in cols_to_plot:
        fig, ax = plt.subplots(figsize=(6,3))
        if "diagnostic" in df.columns:
            sns.boxplot(x=df["diagnostic"], y=df[c], ax=ax)
            ax.set_title(f"{c} segons diagnòstic")
        else:
            sns.boxplot(y=df[c], ax=ax)
            ax.set_title(f"Distribució de {c}")
        st.pyplot(fig)

# Heatmap correlació (només variables numèriques)
st.subheader("Matriu de correlació")
corr = df.corr()
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Feature importance: entrenar model ràpidament si hi ha diagnostic
if "diagnostic" in df.columns:
    st.subheader("Importància de característiques (RandomForest)")
    features = [c for c in df.columns if c != "diagnostic" and c != "id_pacient"]
    if len(features) >= 2:
        X = df[features]
        y = df["diagnostic"]
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X, y)
        importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
        st.bar_chart(importances.head(15))
        st.write("Top 10 característiques més importants:")
        st.table(importances.head(10).reset_index().rename(columns={"index":"Característica",0:"Importància"}))
    else:
        st.info("No hi ha prou característiques per calcular importància.")
else:
    st.info("Necessites la columna 'diagnostic' per calcular importància i comparar grups.")

st.markdown("---")
st.write("Si vols altres gràfics (histogrames, comparacions concretes), digues-me quins i els afegeixo.")
