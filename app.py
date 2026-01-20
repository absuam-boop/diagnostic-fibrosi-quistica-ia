import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# CONFIGURACIÓ GENERAL
# -------------------------------
st.set_page_config(
    page_title="Diagnòstic IA de Fibrosi Quística",
    layout="centered"
)

st.markdown("""
<style>
body { background-color: #f2f6ff; }
.big-title {
    text-align:center;
    font-size:40px;
    font-weight:700;
    color:#003366;
}
.sub {
    text-align:center;
    font-size:18px;
    color:#003366aa;
    margin-bottom:30px;
}
.box {
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.15);
    margin-bottom:30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>Diagnòstic IA de Fibrosi Quística</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Model predictiu basat en dades clíniques</div>", unsafe_allow_html=True)

# ---------------------------------
# CARREGAR I PREPARAR DADES
# ---------------------------------
df = pd.read_excel("dataset_fq.xlsx")

df = df.rename(columns={
    "Edat": "edat",
    "Sexe": "sexe",
    "Test Sudor Clor (concentracio de clorur en mmol/L)": "clor",
    "Mutacio CFTR": "mutacio",
    "FEV1 (Volum espiratori forcat en 1 segon, % predit)": "fev1",
    "Insuficiencia Pancreatica": "pancreas",
    "Tos Cronica": "tos_cronica",
    "Pseudomonas": "pseudomonas",
    "Staphylococcus": "staphylococcus",
    "Haemophilus": "haemophilus",
    "Burkholderia": "burkholderia",
    "Stenotrophomonas": "stenotrophomonas",
    "Aspergillus": "aspergillus",
    "Cap": "cap_infeccio",
    "Diagnostic FQ IA": "diagnostic"
})

cols_usades = [
    "edat", "sexe", "clor", "mutacio", "fev1",
    "pancreas", "tos_cronica",
    "pseudomonas", "staphylococcus", "haemophilus",
    "burkholderia", "stenotrophomonas",
    "aspergillus", "cap_infeccio"
]

X = df[cols_usades]
y = df["diagnostic"]

model = RandomForestClassifier(
    n_estimators=500,
    random_state=42
)
model.fit(X, y)

# -------------------------------
# FORMULARI D'ENTRADA
# -------------------------------
st.markdown("<div class='box'>", unsafe_allow_html=True)
st.header("Dades del pacient")

col1, col2 = st.columns(2)

with col1:
    edat = st.number_input("Edat (anys)", 0, 120)
    sexe = st.selectbox("Sexe", ["Home", "Dona"])
    sexe = 1 if sexe == "Home" else 0
    clor = st.number_input("Test de suor (Clor, mmol/L)", 0.0, 200.0)

with col2:
    mutacio = st.selectbox("Mutació CFTR", ["No", "Sí"])
    mutacio = 1 if mutacio == "Sí" else 0
    fev1 = st.number_input("FEV1 (% predit)", 0.0, 150.0)

st.subheader("Símptomes i afectació clínica")

colA, colB = st.columns(2)

with colA:
    pancreas = st.selectbox("Insuficiència pancreàtica", ["No", "Sí"])
    pancreas = 1 if pancreas == "Sí" else 0

with colB:
    tos = st.selectbox("Tos crònica", ["No", "Sí"])
    tos = 1 if tos == "Sí" else 0

st.subheader("Infeccions respiratòries")
colI1, colI2, colI3 = st.columns(3)

with colI1:
    pseudomonas = st.selectbox("Pseudomonas", ["No", "Sí"])
    pseudomonas = 1 if pseudomonas == "Sí" else 0
    staphylococcus = st.selectbox("Staphylococcus", ["No", "Sí"])
    staphylococcus = 1 if staphylococcus == "Sí" else 0

with colI2:
    haemophilus = st.selectbox("Haemophilus", ["No", "Sí"])
    haemophilus = 1 if haemophilus == "Sí" else 0
    burkholderia = st.selectbox("Burkholderia", ["No", "Sí"])
    burkholderia = 1 if burkholderia == "Sí" else 0

with colI3:
    steno = st.selectbox("Stenotrophomonas", ["No", "Sí"])
    steno = 1 if steno == "Sí" else 0
    aspergillus = st.selectbox("Aspergillus", ["No", "Sí"])
    aspergillus = 1 if aspergillus == "Sí" else 0

cap = st.selectbox("Cap infecció detectada", ["No", "Sí"])
cap = 1 if cap == "Sí" else 0

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# PREDICCIÓ
# -------------------------------
if st.button("Obtenir diagnòstic"):
    dades = [[
        edat, sexe, clor, mutacio, fev1,
        pancreas, tos,
        pseudomonas, staphylococcus, haemophilus,
        burkholderia, steno, aspergillus, cap
    ]]

    prob = model.predict_proba(dades)[0][1]
    pred = model.predict(dades)[0]

    st.markdown("<div class='box'>", unsafe_allow_html=True)

    if pred == 1:
        st.success(
            f"🧬 **Resultat compatible amb Fibrosi Quística**\n\n"
            f"Probabilitat estimada: **{prob*100:.1f}%**"
        )
    else:
        st.info(
            f"✅ **Resultat no compatible amb Fibrosi Quística**\n\n"
            f"Probabilitat estimada: **{prob*100:.1f}%**"
        )

    st.markdown("</div>", unsafe_allow_html=True)
