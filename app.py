import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# CARREGAR BASE DE DADES
# -----------------------------
df = pd.read_excel("dataset_fq.csv (2).xlsx")

# Variable objectiu
y = df["Diagnostic FQ IA"]

# Variables d'entrada
X = df.drop(columns=["ID Pacient", "Diagnostic FQ IA"])

# -----------------------------
# ENTRENAR EL MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -----------------------------
# INTERFÍCIE STREAMLIT
# -----------------------------
st.title("🧬 Diagnòstic de Fibrosi Quística amb IA")
st.write("Introdueix les dades del pacient:")

# -----------------------------
# FORMULARI
# -----------------------------
edat = st.number_input("Edat", 0, 100, 10)
sexe = st.number_input("Sexe (0 = Masculí, 1 = Femení)", 0, 1, 0)
clor = st.number_input("Clor test suor (mmol/L)", 0, 200, 30)
mutacio = st.number_input("Mutació CFTR (0 = No, 1 = Sí)", 0, 1, 0)
fev1 = st.number_input("FEV1 (%)", 0, 150, 100)
pancrees = st.number_input("Insuficiència pancreàtica", 0, 1, 0)

pseudomonas = st.number_input("Pseudomonas", 0, 1, 0)
staphylococcus = st.number_input("Staphylococcus", 0, 1, 0)
haemophilus = st.number_input("Haemophilus", 0, 1, 0)
burkholderia = st.number_input("Burkholderia", 0, 1, 0)
stenotrophomonas = st.number_input("Stenotrophomonas", 0, 1, 0)
aspergillus = st.number_input("Aspergillus", 0, 1, 0)
cap = st.number_input("Cap infecció", 0, 1, 0)

fvc = st.number_input("FVC", 0, 150, 100)
hepatopatia = st.number_input("Hepatopatia", 0, 1, 0)
imc = st.number_input("IMC", 0.0, 40.0, 18.0)
exacerbacions = st.number_input("Nº Exacerbacions Any", 0, 20, 0)
pes = st.number_input("Pes (kg)", 0.0, 150.0, 40.0)
polips = st.number_input("Pòlips nasals", 0, 1, 0)
reflux = st.number_input("Reflux gastroesofàgic", 0, 1, 0)
saturacio = st.number_input("Saturació O2 (%)", 0, 100, 98)
sibilancies = st.number_input("Sibilàncies", 0, 1, 0)
sinusitis = st.number_input("Sinusitis crònica", 0, 1, 0)
talla = st.number_input("Talla (cm)", 30, 220, 140)
tos = st.number_input("Tos crònica", 0, 1, 0)

# -----------------------------
# BOTÓ DIAGNÒSTIC
# -----------------------------
if st.button("🔍 Fer diagnòstic"):
    dades_pacient = [[
        edat, sexe, clor, mutacio, fev1, pancrees,
        pseudomonas, staphylococcus, haemophilus,
        burkholderia, stenotrophomonas, aspergillus, cap,
        fvc, hepatopatia, imc, exacerbacions, pes,
        polips, reflux, saturacio, sibilancies,
        sinusitis, talla, tos
    ]]

    prediccio = model.predict(dades_pacient)[0]

    if prediccio == 1:
        st.error("⚠️ Resultat: POSSIBLE FIBROSI QUÍSTICA")
    else:
        st.success("✅ Resultat: NO compatible amb FQ")
