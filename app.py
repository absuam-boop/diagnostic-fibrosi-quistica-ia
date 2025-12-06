import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# ESTILS PERSONALITZATS
# -------------------------------
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to bottom right, #e3f2fd, #ffffff);
        }
        .title {
            font-size: 40px !important;
            font-weight: 800 !important;
            color: #0d47a1;
            text-align: center;
            padding-bottom: 10px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 25px;
        }
        .result-ok {
            background: #c8e6c9;
            padding: 20px;
            border-radius: 10px;
            font-size: 22px;
            font-weight: 700;
            color: #1b5e20;
        }
        .result-bad {
            background: #ffcdd2;
            padding: 20px;
            border-radius: 10px;
            font-size: 22px;
            font-weight: 700;
            color: #b71c1c;
        }
        .stButton>button {
            background-color: #0d47a1;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #1565c0;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# TÍTOL PRINCIPAL
# -------------------------------
st.markdown('<div class="title">🧬 Diagnòstic de Fibrosi Quística amb IA</div>', unsafe_allow_html=True)
st.write("Introdueix les dades del pacient i el model estimarà la probabilitat de patir Fibrosi Quística.")

# -------------------------------
# CARREGAR DADES I ENTRENAR MODEL
# -------------------------------
df = pd.read_excel("dataset_fq_definitiu.xlsx")

X = df.drop("diagnostic", axis=1)
y = df["diagnostic"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# -------------------------------
# FORMULARI EN TARGETA
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📋 Dades del pacient")

col1, col2 = st.columns(2)

with col1:
    edat = st.number_input("Edat", 0, 100, 10)
    sexe = st.selectbox("Sexe", [0, 1], format_func=lambda x: "Masculí" if x == 0 else "Femení")
    clor = st.number_input("Clor en test de la suor (mmol/L)", 0.0, 200.0, 30.0)
    mutacio = st.selectbox("Mutació CFTR", [0, 1])

with col2:
    fev1 = st.number_input("FEV1 (%)", 0.0, 150.0, 100.0)
    pancreas = st.selectbox("Insuficiència pancreàtica", [0, 1])
    pseudomonas = st.selectbox("Pseudomonas", [0, 1])
    staphylococcus = st.selectbox("Staphylococcus", [0, 1])

# Infeccions addicionals
colA, colB, colC = st.columns(3)

with colA:
    haemophilus = st.selectbox("Haemophilus", [0, 1])
with colB:
    burkholderia = st.selectbox("Burkholderia", [0, 1])
with colC:
    stenotrophomonas = st.selectbox("Stenotrophomonas", [0, 1])

aspergillus = st.selectbox("Aspergillus", [0, 1])
cap_infeccio = st.selectbox("Cap infecció", [0, 1])

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# BOTÓ DE PREDICCIÓ
# -------------------------------
if st.button("🔍 Fer diagnòstic"):
    dades_pacient = [[
        edat, sexe, clor, mutacio, fev1,
        pancreas, pseudomonas, staphylococcus, haemophilus,
        burkholderia, stenotrophomonas, aspergillus, cap_infeccio
    ]]

    prediccio = model.predict(dades_pacient)[0]

    # Mostra el resultat amb estil
    if prediccio == 1:
        st.markdown('<div class="result-bad">⚠️ Possible Fibrosi Quística</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-ok">✅ No compatible amb Fibrosi Quística</div>', unsafe_allow_html=True)
