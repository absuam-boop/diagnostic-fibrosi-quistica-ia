import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Diagnòstic FQ IA", page_icon="🧬", layout="centered")

st.markdown("<h1 style='text-align:center;'>🧬 Diagnòstic de Fibrosi Quística amb IA</h1>", unsafe_allow_html=True)
st.write("Introdueix les dades del pacient i la IA estimarà si pot patir Fibrosi Quística.")

# -------------------------------------------------------------------
# 1. LLEGIR DATASET
# -------------------------------------------------------------------
df = pd.read_excel("dataset_fq.xlsx")

# Separar X i y
y = df["Diagnostic FQ IA"]
X = df.drop(columns=["Diagnostic FQ IA"])

# -------------------------------------------------------------------
# 2. ENTRENAR MODEL
# -------------------------------------------------------------------
model = RandomForestClassifier(
    n_estimators=400,
    random_state=42,
    class_weight="balanced"
)
model.fit(X, y)

# -------------------------------------------------------------------
# 3. FORMULARI PACIENT
# -------------------------------------------------------------------
st.subheader("📋 Dades del pacient")

inputs = {}

for col in X.columns:
    if col == "edat":
        inputs[col] = st.number_input("Edat", 0, 120, 10)
    elif col == "sexe":
        inputs[col] = st.selectbox("Sexe", [0, 1], format_func=lambda x: "Home" if x == 0 else "Dona")
    elif col == "clor_suor":
        inputs[col] = st.number_input("Clor en test de la suor (mmol/L)", 0, 200, 30)
    elif col == "mutacio_cftr":
        inputs[col] = st.selectbox("Mutació CFTR", [0, 1])
    else:
        # totes les infeccions i altres variables binary 0/1
        inputs[col] = st.selectbox(col.replace("_", " ").capitalize(), [0, 1])

# Convertir a DataFrame d'UNA sola fila amb columnes EXACTES
dades_pacient = pd.DataFrame([inputs])[X.columns]

# -------------------------------------------------------------------
# 4. BOTÓ PREDECCIÓ
# -------------------------------------------------------------------
if st.button("🔍 Fer diagnòstic"):
    pred = model.predict(dades_pacient)[0]
    prob = model.predict_proba(dades_pacient)[0][1] * 100

    if pred == 1:
        st.success(f"🧪 **Possible Fibrosi Quística** ({prob:.1f}% de probabilitat)")
    else:
        st.info(f"✅ **No compatible amb Fibrosi Quística** ({prob:.1f}% de probabilitat)")
