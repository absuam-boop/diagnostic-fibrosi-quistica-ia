import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# TÍTOL DE L’APP
st.title("🧬 Diagnòstic de Fibrosi Quística amb Intel·ligència Artificial")
st.write("Introdueix les dades del pacient i la IA estimarà si pot patir Fibrosi Quística.")

# CARREGAR LA BASE DE DADES
df = pd.read_excel("dataset_fq.csv (2).xlsx")

# ELIMINAR COLUMNES QUE NO SÓN NUMÈRIQUES
df = df.select_dtypes(include=["number"])

# SEPARAR VARIABLES I RESULTAT
columna_resultat = df.columns[-1]   # agafa l’última columna automàticament
X = df.drop(columna_resultat, axis=1)
y = df[columna_resultat]

# ENTRENAR EL MODEL
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# FORMULARI DEL PACIENT
st.header("📋 Dades del pacient")

edat = st.number_input("Edat del pacient", 0, 120, 10)
sexe = st.number_input("Sexe (0 = Masculí, 1 = Femení)", 0, 1, 0)
clor = st.number_input("Clor en test de la suor (mmol/L)", 0, 200, 30)
mutacio = st.number_input("Mutació CFTR (0 = No, 1 = Sí)", 0, 1, 0)
fev1 = st.number_input("FEV1 (%)", 0, 150, 100)

pancrees = st.number_input("Insuficiència pancreàtica (0 = No, 1 = Sí)", 0, 1, 0)
pseudomonas = st.number_input("Pseudomonas (0 = No, 1 = Sí)", 0, 1, 0)
staphylococcus = st.number_input("Staphylococcus (0 = No, 1 = Sí)", 0, 1, 0)
haemophilus = st.number_input("Haemophilus (0 = No, 1 = Sí)", 0, 1, 0)
burkholderia = st.number_input("Burkholderia (0 = No, 1 = Sí)", 0, 1, 0)
stenotrophomonas = st.number_input("Stenotrophomonas (0 = No, 1 = Sí)", 0, 1, 0)
aspergillus = st.number_input("Aspergillus (0 = No, 1 = Sí)", 0, 1, 0)
cap_infeccio = st.number_input("Sense infecció (0 = No, 1 = Sí)", 0, 1, 0)

# BOTÓ DE DIAGNÒSTIC
if st.button("🔍 Fer diagnòstic"):
    dades = [[
        edat, sexe, clor, mutacio, fev1,
        pancreas, pseudomonas, staphylococcus,
        haemophilus, burkholderia,
        stenotrophomonas, aspergillus, cap_infeccio
    ]]

    resultat = model.predict(dades)

    if resultat[0] == 1:
        st.error("⚠️ Resultat: POSSIBLE Fibrosi Quística")
    else:
        st.success("✅ Resultat: NO compatible amb Fibrosi Quística")
