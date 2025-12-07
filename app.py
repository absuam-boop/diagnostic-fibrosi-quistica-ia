import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Diagnòstic Fibrosi Quística", layout="centered")

# -------------------------------
# ESTILS CSS
# -------------------------------
st.markdown("""
<style>
.box {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #d0d4da;
    margin-bottom: 20px;
}
h1 {
    text-align: center;
    color: #004080;
}
.result-ok {
    background-color: #d4f8d4;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #89c789;
    color: #006600;
    font-size: 18px;
}
.result-bad {
    background-color: #ffd6d6;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #cc7a7a;
    color: #990000;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧬 Diagnòstic de Fibrosi Quística amb IA")

st.markdown("Aquesta aplicació permet predir si un pacient té possible **Fibrosi Quística (FQ)** basant-se en paràmetres clínics.")


# ---------------------------------------
# CARREGA I NETEJA AUTOMÀTICA DEL DATASET
# ---------------------------------------
@st.cache_data
def carregar_dataset(path):
    df = pd.read_excel(path)

    mapeig = {
        "ID Pacient": "id_pacient",
        "Edat": "edat",
        "Sexe": "sexe",
        "Test Sudor Clor (concentracio de clorur en mmol/L)": "clor",
        "Mutacio CFTR": "mutacio",
        "FEV1 (Volum espiratori forcat en 1 segon, % predit)": "fev1",
        "Insuficiencia Pancreatica": "pancreas",
        "Pseudomonas": "pseudomonas",
        "Staphylococcus": "staphylococcus",
        "Haemophilus": "haemophilus",
        "Burkholderia": "burkholderia",
        "Stenotrophomonas": "stenotrophomonas",
        "Aspergillus": "aspergillus",
        "Cap": "cap_infeccio",
        "FVC": "fvc",
        "Hepatopatia": "hepatopatia",
        "IMC": "imc",
        "Nº Exarcebacions Any": "exacerbacions",
        "Pes": "pes",
        "Polips nasals": "polips",
        "Reflux Gastroesofagic": "reflux",
        "Saturacio O2": "saturacio",
        "Sibilancies": "sibilancies",
        "Sinusitis Cronica": "sinusitis",
        "Diagnostic FQ IA": "diagnostic",
        "Talla": "talla",
        "Tos cronica": "tos"
    }

    df = df.rename(columns=mapeig)

    # Convertim a numèrics
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    return df


df = carregar_dataset("dataset_fq.xlsx")

# Model
X = df.drop(columns=["diagnostic"])
y = df["diagnostic"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# -------------------------------
# FORMULARI DE PREDICCIÓ
# -------------------------------
st.subheader("🔎 Introdueix les dades del pacient")

with st.form("predictor"):
    col1, col2 = st.columns(2)

    with col1:
        edat = st.number_input("Edat", 0, 100, 10)
        sexe = st.selectbox("Sexe (0 = Dona, 1 = Home)", [0, 1])
        clor = st.number_input("Clor (mmol/L)", 0, 200, 30)
        mutacio = st.selectbox("Mutació CFTR (0 = No, 1 = Sí)", [0, 1])
        fev1 = st.number_input("FEV1 (% predit)", 0, 150, 80)
        pancreas = st.selectbox("Insuficiència Pancreàtica", [0, 1])
        fvc = st.number_input("FVC", 0, 200, 100)

    with col2:
        exacerb = st.number_input("Exacerbacions/Any", 0, 20, 0)
        pes = st.number_input("Pes (kg)", 1, 150, 40)
        imc = st.number_input("IMC", 10.0, 40.0, 18.0)
        hepatopatia = st.selectbox("Hepatopatia", [0, 1])
        saturacio = st.number_input("Saturació O2 (%)", 50, 100, 97)
        talla = st.number_input("Talla (cm)", 30, 220, 150)

    st.write("### Infeccions bacterianes")
    col3, col4, col5 = st.columns(3)
    with col3:
        pseudomonas = st.selectbox("Pseudomonas", [0, 1])
        aspergillus = st.selectbox("Aspergillus", [0, 1])
        haemophilus = st.selectbox("Haemophilus", [0, 1])
    with col4:
        staphylococcus = st.selectbox("Staphylococcus", [0, 1])
        burkholderia = st.selectbox("Burkholderia", [0, 1])
        stenotrophomonas = st.selectbox("Stenotrophomonas", [0, 1])
    with col5:
        polips = st.selectbox("Pòlips Nasals", [0, 1])
        reflux = st.selectbox("Reflux", [0, 1])
        sinusitis = st.selectbox("Sinusitis", [0, 1])

    tos = st.selectbox("Tos Crònica", [0, 1])
    cap_infeccio = st.selectbox("Cap infecció", [0, 1])

    submit = st.form_submit_button("🔍 Predir Diagnòstic")


# -------------------------------
# RESULTAT
# -------------------------------
if submit:
    entrada = pd.DataFrame([[
        0, edat, sexe, clor, mutacio, fev1, pancreas, pseudomonas,
        staphylococcus, haemophilus, burkholderia, stenotrophomonas,
        aspergillus, cap_infeccio, fvc, hepatopatia, imc, exacerb,
        pes, polips, reflux, saturacio, sibilancies, sinusitis,
        0, talla, tos
    ]], columns=X.columns)

    pred = model.predict(entrada)[0]

    st.markdown("---")
    if pred == 1:
        st.markdown("<div class='result-bad'>⚠️ Possible diagnòstic de Fibrosi Quística</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-ok'>✅ No compatible amb Fibrosi Quística</div>", unsafe_allow_html=True)
