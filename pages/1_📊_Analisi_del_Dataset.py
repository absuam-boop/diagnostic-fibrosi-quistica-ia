import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 Anàlisi del Dataset")

# Carregar dataset
df = pd.read_excel("dataset_fq.xlsx")

st.subheader("Vista general del dataset")
st.dataframe(df.head())

# --- Gràfic de correlació ---
st.subheader("🔗 Matriu de correlació")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df.corr(), ax=ax, annot=True, fmt=".2f")
st.pyplot(fig)

# --- Distribució del clor ---
st.subheader("💧 Distribució dels nivells de clor en pacients FQ vs no FQ")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=df["diagnostic"], y=df["clor"], ax=ax)
ax.set_xlabel("Diagnòstic (0 = No FQ, 1 = FQ)")
ax.set_ylabel("Clor (mmol/L)")
st.pyplot(fig)

# --- FEV1 ---
st.subheader("🫁 FEV1 segons diagnòstic")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x=df["diagnostic"], y=df["fev1"], ax=ax)
ax.set_xlabel("Diagnòstic")
ax.set_ylabel("FEV1 (%)")
st.pyplot(fig)

# --- Comptatge ---
st.subheader("🧪 Distribució del diagnòstic")

fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(x=df["diagnostic"], ax=ax)
st.pyplot(fig)
