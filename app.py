import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Diagnòstic FQ amb IA", layout="centered")
st.title("🧬 Diagnòstic de Fibrosi Quística amb Intel·ligència Artificial")
st.write("Introdueix les dades del pacient i la IA estimarà si pot patir Fibrosi Quística.")

df = pd.read_excel("dataset_fq.csv (2).xlsx")

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.fillna(df.median())

X = df.drop(["Diagnostic FQ IA", "ID Pacient"], axis=1)
y = df["Diagnostic FQ IA"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

st.header("📋 Dades del pacient")

edat = st.number_input("Edat", 0, 100, 10)
sexe = st.selectbox("Sexe (0 = Masculí, 1 = Femení)", [0, 1])
clor = st.number_input("Clor en test de la suor (mmol/L)", 0, 150, 30)
mutacio = st.selectbox("Mutació CFTR (0 = No, 1 = Sí)", [0, 1])
fev1 = st.number_input("FEV1 (%)", 0, 150, 100)
pancreas = st.selectbox("Insuficiència pancreàtica", [0, 1])

pseudomonas = st.selectbox("Pseudomonas", [0, 1])
staphylococcus = st.selectbox("Staphylococcus", [0, 1])
haemophilus = st.selectbox("Haemophilus", [0, 1])
burkholderia = st.selectbox("Burkholderia", [0, 1])
stenotrophomonas = st.selectbox("Stenotrophomonas", [0, 1])
aspergillus = st.selectbox("Aspergillus", [0, 1])
cap = st.selectbox("Cap infecció", [0, 1])

st.header("📋 Dades del pacient")

edat = st.number_input("Edat", 0, 100, 10)
sexe = st.selectbox("Sexe (0 = Masculí, 1 = Femení)", [0, 1])
clor = st.number_input("Clor en test de la suor (mmol/L)", 0, 150, 30)
mutacio = st.selectbox("Mutació CFTR (0 = No, 1 = Sí)", [0, 1])
fev1 = st.number_input("FEV1 (%)", 0, 150, 100)
pancreas = st.selectbox("Insuficiència pancreàtica", [0, 1])

pseudomonas = st.selectbox("Pseudomonas", [0, 1])
staphylococcus = st.selectbox("Staphylococcus", [0, 1])
haemophilus = st.selectbox("Haemophilus", [0, 1])
burkholderia = st.selectbox("Burkholderia", [0, 1])
stenotrophomonas = st.selectbox("Stenotrophomonas", [0, 1])
aspergillus = st.selectbox("Aspergillus", [0, 1])
cap = st.selectbox("Cap infecció", [0, 1])
