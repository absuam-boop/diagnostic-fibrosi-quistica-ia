import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Diagnòstic Fibrosi Quística IA", page_icon="🫁", layout="centered")

# ---------------------- ESTILS ----------------------
st.markdown("""
<style>
body {
    font-family: 'Arial', sans-serif;
}
.big-title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    margin-bottom: -10px;
}
.subtitle {
    font-size: 18px;
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}
.box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.10);
    margin-bottom: 25px;
}
.result-ok {
    padding: 22px;
    background-color: #d4f8d4;
    border-left: 8px solid #2e8b57;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 600;
}
.result-bad {
    padding: 22px;
    background-color: #ffd6d6;
    border-left: 8px solid #c0392b;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- TÍTOL ----------------------
st.markdown("<div class='big-title'>🫁 Diagnòstic de Fibrosi Quística amb IA</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Model predictiu basat en dades clíniques</div>", unsafe_allow_html=True)

# ---------------------- CARREGA MODEL ----------------------
model = joblib.load("model_fq.pkl")

# ---------------------- FORMULARI ----------------------
st.markdown("<div class='box'>", unsafe_allow_html=True)
st.subheader("Dades clíniques del pacient")

edat = st.number_input("Edat", min_value=0, max_value=120, value=10)
sexe = st.selectbox("Sexe", ["Home", "Dona"])
clor = st.number_input("Test de suor (clorur en mmol/L)", min_value=0.0, max_value=200.0)
mutacio = st.selectbox("Mutació CFTR", ["0 = Cap", "1 = Present"])
fev1 = st.number_input("FEV1 (% predit)", min_value=0.0, max_value=150.0)
pancreas = st.selectbox("Insuficiència pancreàtica", ["0 = No", "1 = Sí"])

pseudomonas = st.selectbox("Pseudomonas", ["0 = No", "1 = Sí"])
staphylococcus = st.selectbox("Staphylococcus", ["0 = No", "1 = Sí"])
haemophilus = st.selectbox("Haemophilus", ["0 = No", "1 = Sí"])
burkholderia = st.selectbox("Burkholderia", ["0 = No", "1 = Sí"])
steno = st.selectbox("Stenotrophomonas", ["0 = No", "1 = Sí"])
aspergillus = st.selectbox("Aspergillus", ["0 = No", "1 = Sí"])
cap = st.selectbox("Cap infecció", ["0 = No", "1 = Sí"])

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- PREDICCIÓ ----------------------
if st.button("🔍 Fer diagnòstic"):
    dades = pd.DataFrame([{
        "edat": edat,
        "sexe": 1 if sexe == "Home" else 0,
        "clor": clor,
        "mutacio": int(mutacio[0]),
        "fev1": fev1,
        "pancreas": int(pancreas[0]),
        "pseudomonas": int(pseudomonas[0]),
        "staphylococcus": int(staphylococcus[0]),
        "haemophilus": int(haemophilus[0]),
        "burkholderia": int(burkholderia[0]),
        "stenotrophomonas": int(steno[0]),
        "aspergillus": int(aspergillus[0]),
        "cap_infeccio": int(cap[0])
    }])

    pred = model.predict(dades)[0]
    prob = model.predict_proba(dades)[0][1] * 100

    if pred == 1:
        st.markdown(f"<div class='result-bad'>⚠ Possibilitat alta de Fibrosi Quística<br><br>Probabilitat: {prob:.2f}%</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='result-ok'>🟢 No sembla compatible amb Fibrosi Quística<br><br>Probabilitat: {prob:.2f}%</div>", unsafe_allow_html=True)
