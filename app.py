import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Diagnòstic FQ IA", page_icon="🫁", layout="wide")

st.title("🫁 Diagnòstic de Fibrosi Quística amb IA")
st.markdown("Introdueix les dades del pacient per obtenir una predicció automàtica.")

# --- Carregar model ---
model = joblib.load("model_fq.pkl")

# --- Formulari ---
st.header("Dades del pacient")

col1, col2 = st.columns(2)

with col1:
    edat = st.number_input("Edat", 0, 120, 12)
    sexe = st.selectbox("Sexe", ["Home", "Dona"])
    clor = st.number_input("Clor en suor (mmol/L)", 0, 150, 50)
    mutacio = st.selectbox("Mutació genètica detectada", ["Sí", "No"])

with col2:
    fev1 = st.number_input("FEV1 (%)", 0, 200, 80)
    pancreas = st.selectbox("Insuficiència pancreàtica", ["Sí", "No"])
    
    infeccio = st.selectbox("Infecció principal", [
        "Cap", "Pseudomonas", "Staphylococcus", "Haemophilus", 
        "Burkholderia", "Stenotrophomonas", "Aspergillus"
    ])

# Convertir a format compatible
dades = pd.DataFrame([{
    "edat": edat,
    "sexe": 1 if sexe == "Home" else 0,
    "clor": clor,
    "mutacio": 1 if mutacio == "Sí" else 0,
    "fev1": fev1,
    "pancreas": 1 if pancreas == "Sí" else 0,
    "pseudomonas": 1 if infeccio == "Pseudomonas" else 0,
    "staphylococcus": 1 if infeccio == "Staphylococcus" else 0,
    "haemophilus": 1 if infeccio == "Haemophilus" else 0,
    "burkholderia": 1 if infeccio == "Burkholderia" else 0,
    "stenotrophomonas": 1 if infeccio == "Stenotrophomonas" else 0,
    "aspergillus": 1 if infeccio == "Aspergillus" else 0,
    "cap_infeccio": 1 if infeccio == "Cap" else 0
}])

st.subheader("🔍 Resultat del diagnòstic")

if st.button("Obtenir diagnòstic"):
    prediccio = model.predict(dades)[0]
    probabilitat = model.predict_proba(dades)[0][1]

    if prediccio == 1:
        st.error(f"⚠ Possible cas compatible amb Fibrosi Quística. Probabilitat: {probabilitat:.2f}")
    else:
        st.success(f"🟢 No compatible amb FQ. Probabilitat: {probabilitat:.2f}")
