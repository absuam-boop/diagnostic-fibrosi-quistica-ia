import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -----------------------------------------
# CONFIGURACIÓ DE PÀGINA (estètica)
# -----------------------------------------
st.set_page_config(
    page_title="Diagnòstic FQ amb IA",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# ESTILS PERSONALITZATS
# -----------------------------------------
st.markdown("""
<style>
/* Color de fons suau */
body {
    background-color: #f4f6f9;
}

/* Estil de les targetes */
.card {
    padding: 20px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Títols */
h1 {
    color: #2c3e50;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# CARREGAR DADES
# -----------------------------------------
df = pd.read_excel("dataset_fq_definitiu.xlsx")

df = df.drop(columns=["ID Pacient"])
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.fillna(0)

y = df["Diagnostic FQ IA"]
X = df.drop(columns=["Diagnostic FQ IA"])

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -----------------------------------------
# TÍTOL PRINCIPAL
# -----------------------------------------
st.markdown("<h1>🧬 Diagnòstic de Fibrosi Quística amb Intel·ligència Artificial</h1>", unsafe_allow_html=True)
st.write("Aquest sistema utilitza un model de Random Forest per estimar la probabilitat de Fibrosi Quística a partir de dades clíniques del pacient.")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------
# ORGANITZACIÓ DEL FORMULARI EN COLUMNES
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📋 Introdueix les dades del pacient")

col1, col2, col3 = st.columns(3)

with col1:
    edat = st.number_input("Edat", 0, 100, 10)
    sexe = st.number_input("Sexe (0 = M, 1 = F)", 0, 1, 0)
    clor = st.number_input("Clor (mmol/L)", 0, 200, 30)
    mutacio = st.number_input("Mutació CFTR", 0, 1, 0)
    fev1 = st.number_input("FEV1 (%)", 0, 150, 100)
    fvc = st.number_input("FVC (%)", 0, 150, 100)
    imc = st.number_input("IMC", 0.0, 40.0, 18.0)

with col2:
    pancrees = st.number_input("Insuficiència pancreàtica", 0, 1, 0)
    hepatopatia = st.number_input("Hepatopatia", 0, 1, 0)
    exacerbacions = st.number_input("Exacerbacions/any", 0, 20, 0)
    pes = st.number_input("Pes (kg)", 0.0, 150.0, 40.0)
    talla = st.number_input("Talla (cm)", 30, 220, 140)
    saturacio = st.number_input("Saturació O2 (%)", 0, 100, 98)

with col3:
    pseudomonas = st.number_input("Pseudomonas", 0, 1, 0)
    staphylococcus = st.number_input("Staphylococcus", 0, 1, 0)
    haemophilus = st.number_input("Haemophilus", 0, 1, 0)
    burkholderia = st.number_input("Burkholderia", 0, 1, 0)
    stenotrophomonas = st.number_input("Stenotrophomonas", 0, 1, 0)
    aspergillus = st.number_input("Aspergillus", 0, 1, 0)
    cap = st.number_input("Cap infecció", 0, 1, 0)
    polips = st.number_input("Pòlips nasals", 0, 1, 0)
    reflux = st.number_input("Reflux", 0, 1, 0)
    sibilancies = st.number_input("Sibilàncies", 0, 1, 0)
    sinusitis = st.number_input("Sinusitis crònica", 0, 1, 0)
    tos = st.number_input("Tos crònica", 0, 1, 0)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# BOTÓ DE DIAGNÒSTIC
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

if st.button("🔍 Fer diagnòstic"):
    dades_pacient = [[
        edat, sexe, clor, mutacio, fev1, pancrees, pseudomonas,
        staphylococcus, haemophilus, burkholderia, stenotrophomonas,
        aspergillus, cap, fvc, hepatopatia, imc, exacerbacions, pes,
        polips, reflux, saturacio, sibilancies, sinusitis, talla, tos
    ]]

    pred = model.predict(dades_pacient)[0]

    if pred == 1:
        st.error("⚠️ Resultat: **POSSIBLE FIBROSI QUÍSTICA**")
    else:
        st.success("✅ Resultat: **NO compatible amb FQ**")

st.markdown('</div>', unsafe_allow_html=True)
