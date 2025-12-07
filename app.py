import streamlit as st
import pandas as pd
import unicodedata
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Diagnòstic FQ (robust)", layout="centered")

# -------------------------
# Funció per normalitzar noms
# -------------------------
def normalize_name(s):
    if not isinstance(s, str):
        return ""
    s = s.strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    # substituir tot el que no sigui lletra o número per underscore
    import re
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s

# -------------------------
# Mapatge per paraules clau a noms canònics
# -------------------------
keyword_map = {
    "edat": "edat",
    "sexe": "sexe",
    "clor": "clor",
    "suor": "clor",
    "sudor": "clor",
    "mutacio": "mutacio",
    "cftr": "mutacio",
    "fev1": "fev1",
    "insuficiencia_pancreatica": "pancreas",
    "pancrea": "pancreas",
    "pancreas": "pancreas",
    "pseudomon": "pseudomonas",
    "staphyl": "staphylococcus",
    "staphylococcus": "staphylococcus",
    "haemophil": "haemophilus",
    "haemophilus": "haemophilus",
    "burk": "burkholderia",
    "stenotrophomonas": "stenotrophomonas",
    "asperg": "aspergillus",
    "cap": "cap_infeccio",
    "fvc": "fvc",
    "hepat": "hepatopatia",
    "imc": "imc",
    "exacer": "exacerbacions",
    "exarce": "exacerbacions",
    "pes": "pes",
    "polip": "polips",
    "reflux": "reflux",
    "satur": "saturacio",
    "sibil": "sibilancies",
    "sinus": "sinusitis",
    "diagnostic": "diagnostic",
    "diagnosticfq": "diagnostic",
    "diagnosticfqia": "diagnostic",
    "talla": "talla",
    "tos": "tos"
}

# -------------------------
# Carrega del dataset (intent automàtic)
# -------------------------
st.title("🧬 Diagnòstic FQ — càrrega i normalització automàtiques")

uploaded = st.file_uploader("Puja el fitxer dataset_fq.xlsx (o fes servir el del repositori)", type=["xlsx"])
if uploaded is None:
    # intentem llegir directament pel nom (per a Streamlit Cloud si ja està pujat)
    try:
        df_raw = pd.read_excel("dataset_fq.xlsx")
    except Exception:
        st.warning("Puja l'arxiu 'dataset_fq.xlsx' o assegura't que està al repositori.")
        st.stop()
else:
    df_raw = pd.read_excel(uploaded)

st.write("Columnes originals detectades:")
st.write(list(df_raw.columns))

# Normalitzem els noms
norm_cols = [normalize_name(c) for c in df_raw.columns]
mapping = dict(zip(df_raw.columns, norm_cols))
st.write("Columnes normalitzades (temporals):")
st.write(mapping)

# Mapatge intel·ligent a noms canònics
final_cols = {}
used = set()
for orig, norm in mapping.items():
    chosen = None
    # busquem paraules clau dins del nom normalitzat
    for key, canon in keyword_map.items():
        if key in norm and canon not in used:
            chosen = canon
            break
    # si no trobem cap coincidència, fem servir el nom normalitzat tal qual (si no xoca)
    if chosen is None:
        chosen = norm
    final_cols[orig] = chosen
    used.add(chosen)

st.write("Mapeig final (original -> canònic):")
st.write(final_cols)

# Apliquem el renombrament
df = df_raw.rename(columns=final_cols)

# Convertim a numèric i omplim NaN
df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

st.write("Columnes després del renombrament i neteja:")
st.write(list(df.columns))

# Comprovació de columnes obligatòries
required = ["edat","sexe","clor","mutacio","fev1","pancreas",
            "pseudomonas","staphylococcus","haemophilus","burkholderia",
            "stenotrophomonas","aspergillus","cap_infeccio","diagnostic"]

missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"❌ Falten columnes desprès de la normalització: {missing}")
    st.stop()

# Tot correcte: entrenem model
X = df.drop(columns=["diagnostic"])
y = df["diagnostic"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

st.success("✅ Dataset validat i model entrenat correctament")

# -------------------------
# Formulari per predicció (ordenem amb les columnes de X)
# -------------------------
st.subheader("🔎 Introdueix dades del pacient")

# creem inputs segons l'ordre de X.columns
inputs = {}
for col in X.columns:
    label = col.replace("_", " ").capitalize()
    # si és binari 0/1 fem selectbox, si és continu fem number_input
    if col in ["sex", "sexe","mutacio","pancreas","pseudomonas","staphylococcus","haemophilus",
               "burkholderia","stenotrophomonas","aspergillus","cap_infeccio","polips","reflux","sibilancies","sinusitis","tos"]:
        inputs[col] = st.selectbox(label, [0,1], index=1)
    else:
        # límits generals; l'usuari pot adaptar-ho
        inputs[col] = st.number_input(label, value=0.0)

# Build DataFrame d'entrada amb l'ordre correcte
entrada = pd.DataFrame([[inputs[c] for c in X.columns]], columns=X.columns)

if st.button("🔍 Fer diagnòstic"):
    pred = model.predict(entrada)[0]
    prob = model.predict_proba(entrada)[0][1]
    if pred == 1:
        st.error(f"⚠️ Possible Fibrosi Quística — probabilitat {prob*100:.1f}%")
    else:
        st.success(f"✅ No compatible amb Fibrosi Quística — probabilitat {prob*100:.1f}%")
