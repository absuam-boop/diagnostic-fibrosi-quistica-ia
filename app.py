import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ------------------------------------
# ⭐ Estil CSS modern
# ------------------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .title {
            color: #2c3e50;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #34495e;
            text-align: center;
            font-size: 20px;
            margin-bottom: 30px;
        }
        .box {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 0px 12px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------
# ⭐ Títol principal
# ------------------------------------
st.markdown('<div class="title">🧬 Diagnòstic de Fibrosi Quística amb IA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Introdueix les dades del pacient i la IA farà una predicció.</div>', unsafe_allow_html=True)

# ------------------------------------
# ⭐ Carregar dataset
# ------------------------------------
df = pd.read_excel("dataset_fq.xlsx")

# 🔧 Solució a l'error: convertir totes les columnes a numèric
df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

# Comprovar columnes correctes
required_cols = [
    'edat','sexe','clor','mutacio','fev1','pancreas',
    'pseudomonas','staphylococcus','haemophilus',
    'burkholderia','stenotrophomonas','aspergillus',
    'cap_infeccio','diagnostic'
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"❌ Falten columnes al dataset: {missing}")
    st.stop()

# ------------------------------------
# ⭐ Entrenar model
# ------------------------------------
X = df.drop("diagnostic", axis=1)
y = df["diagnostic"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# ------------------------------------
# ⭐ Formulari de dades del pacient
# ------------------------------------
st.markdown('<div class="box">', unsafe_allow_html=True)

st.subheader("📋 Dades del pacient")

edat = st.number_input("Edat", 0, 120, 10)
sexe = st.selectbox("Sexe", ["Masculí (0)", "Femení (1)"])
sexe = 0 if sexe == "Masculí (0)" else 1

clor = st.number_input("Clor en test de la suor (mmol/L)", 0, 200, 30)
mutacio = st.selectbox("Mutació CFTR", ["No (0)", "Sí (1)"])
mutacio = 1 if mutacio == "Sí (1)" else 0

fev1 = st.number_input("FEV1 (%)", 0, 150, 100)

pancreas = st.selectbox("Insuficiència pancreàtica", ["No (0)", "Sí (1)"])
pancreas = 1 if pancreas == "Sí (1)" else 0

pseudomonas = st.selectbox("Pseudomonas", ["No (0)", "Sí (1)"])
pseudomonas = 1 if pseudomonas == "Sí (1)" else 0

staphylococcus = st.selectbox("Staphylococcus", ["No (0)", "Sí (1)"])
staphylococcus = 1 if staphylococcus == "Sí (1)" else 0

haemophilus = st.selectbox("Haemophilus", ["No (0)", "Sí (1)"])
haemophilus = 1 if haemophilus == "Sí (1)" else 0

burkholderia = st.selectbox("Burkholderia", ["No (0)", "Sí (1)"])
burkholderia = 1 if burkholderia == "Sí (1)" else 0

steno = st.selectbox("Stenotrophomonas", ["No (0)", "Sí (1)"])
steno = 1 if steno == "Sí (1)" else 0

asper = st.selectbox("Aspergillus", ["No (0)", "Sí (1)"])
asper = 1 if asper == "Sí (1)" else 0

cap_inf = st.selectbox("Cap infecció", ["No (0)", "Sí (1)"])
cap_inf = 1 if cap_inf == "Sí (1)" else 0

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------
# ⭐ Predicció
# ------------------------------------
if st.button("🔍 Fer diagnòstic", use_container_width=True):
    dades_pacient = pd.DataFrame([[
        edat, sexe, clor, mutacio, fev1, pancreas,
        pseudomonas, staphylococcus, haemophilus,
        burkholderia, steno, asper, cap_inf
    ]], columns=X.columns)

    pred = model.predict(dades_pacient)[0]
    prob = model.predict_proba(dades_pacient)[0][1]

    if pred == 1:
        st.success(f"🟢 **Possible Fibrosi Quística** (probabilitat: {prob*100:.1f}%)")
    else:
        st.error(f"🔴 **No compatible amb Fibrosi Quística** (probabilitat: {prob*100:.1f}%)")
