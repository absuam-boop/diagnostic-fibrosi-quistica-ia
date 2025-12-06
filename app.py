import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import altair as alt

# --------------------------
# CARREGA DE DADES I MODEL
# --------------------------
df = pd.read_excel("dataset_fq_definitiu.xlsx")

X = df.drop("diagnostic", axis=1)
y = df["diagnostic"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

# --------------------------
# ESTILS VISUALS
# --------------------------
st.set_page_config(
    page_title="Diagnòstic Fibrosi Quística IA",
    page_icon="🧬",
    layout="centered"
)

st.markdown("""
<style>
    .big-title {
        font-size: 32px !important;
        font-weight: 700;
        text-align: center;
        color: #3A7CA5;
    }
    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #F0F8FF;
        border: 2px solid #A3C4D9;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# TÍTOL
# --------------------------
st.markdown('<p class="big-title">🧬 Diagnòstic de Fibrosi Quística amb IA</p>', unsafe_allow_html=True)
st.write("Introdueix les dades del pacient i la IA estimarà el risc de Fibrosi Quística.")

# --------------------------
# FORMULARI
# --------------------------
st.header("📋 Dades del pacient")

edat = st.number_input("Edat", 0, 100, 10)
sexe = st.selectbox("Sexe", [0,1], format_func=lambda x: "Masculí" if x==0 else "Femení")
clor = st.number_input("Clor en test de la suor (mmol/L)", 0, 200, 30)
mutacio = st.selectbox("Mutació CFTR", [0,1])
fev1 = st.number_input("FEV1 (%)", 0, 150, 100)
pancrees = st.selectbox("Insuficiència pancreàtica", [0,1])
pseudomonas = st.selectbox("Pseudomonas", [0,1])
staphylococcus = st.selectbox("Staphylococcus", [0,1])
haemophilus = st.selectbox("Haemophilus", [0,1])
burkholderia = st.selectbox("Burkholderia", [0,1])
steno = st.selectbox("Stenotrophomonas", [0,1])
aspergillus = st.selectbox("Aspergillus", [0,1])
cap_infeccio = st.selectbox("Cap infecció", [0,1])

# -------------------------------
# PREDICCIÓ
# -------------------------------
if st.button("🔍 Fer diagnòstic"):
    
    dades_pacient = [[
        edat, sexe, clor, mutacio, fev1,
        pancrees, pseudomonas, staphylococcus, haemophilus,
        burkholderia, steno, aspergillus, cap_infeccio
    ]]
    
    # Probabilitat
    prob = model.predict_proba(dades_pacient)[0][1]
    prediccio = 1 if prob >= 0.5 else 0

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    st.subheader("🧠 Resultat del diagnòstic")

    st.write(f"**Probabilitat estimada de FQ:** `{prob*100:.1f}%`")

    if prediccio == 1:
        st.error("**Risc ALT:** El model detecta una probabilitat elevada compatible amb Fibrosi Quística.")
    else:
        st.success("**Risc BAIX:** El model no detecta indicis compatibles amb Fibrosi Quística.")

    # -------------------------
    # GRÀFIC DE RISC
    # -------------------------
    chart_data = pd.DataFrame({
        "Categoria": ["Risc de FQ"],
        "Probabilitat": [prob * 100]
    })

    chart = alt.Chart(chart_data).mark_bar().encode(
        x="Categoria",
        y="Probabilitat"
    ).properties(
        width=300,
        height=300
    )

    st.altair_chart(chart)

    # -------------------------
    # INFORME EXPLICATIU
    # -------------------------
    st.subheader("📄 Informe interpretatiu")

    if prob < 0.33:
        st.write("""
        El model indica un **risc baix**.  
        Aquest resultat és habitual en pacients sense valors anormals al test de suor 
        i sense mutacions CFTR ni infeccions greus recurrents.  
        **Tot i així, qualsevol sospita clínica ha de ser contrastada amb proves mèdiques oficials.**
        """)
    elif prob < 0.66:
        st.write("""
        El model indica un **risc moderat**.  
        Algunes variables poden estar fora de rang o ser indicatives de disfunció pulmonar o digestiva.  
        **Es recomana realitzar proves diagnòstiques complementàries com el test de suor o estudis genètics.**
        """)
    else:
        st.write("""
        El model indica un **risc alt**.  
        Aquesta estimació pot correspondre’s amb alteracions clíniques rellevants,
        com valors elevats de clor en suor, FEV1 reduït o presència d'infeccions típiques.  
        **Cal valoració mèdica especialitzada urgent.**
        """)

    st.markdown('</div>', unsafe_allow_html=True)
