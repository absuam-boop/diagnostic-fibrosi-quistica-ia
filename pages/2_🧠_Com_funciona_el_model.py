# pages/2_🧠_Com_funciona_el_model.py
import streamlit as st
import pandas as pd
import unicodedata, re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🧠 Com funciona el model", layout="centered")
st.title("🧠 Com funciona el model i mètriques")

# normalització petita (mateixa lògica que a l'altre fitxer)
def normalize_name(s):
    if not isinstance(s, str): return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s

# carregar dataset
uploaded = st.file_uploader("(Opcional) Pujar dataset per a l'anàlisi", type=["xlsx"])
if uploaded is not None:
    df_raw = pd.read_excel(uploaded)
else:
    try:
        df_raw = pd.read_excel("dataset_fq.xlsx")
    except Exception:
        st.error("No s'ha trobat 'dataset_fq.xlsx'. Puja el fitxer.")
        st.stop()

# renombrament simple per tenir noms curts (si existeixen les columnes originals)
mapeig = {
    "Edat":"edat","Sexe":"sexe","Test Sudor Clor (concentracio de clorur en mmol/L)":"clor",
    "Mutacio CFTR":"mutacio","FEV1 (Volum espiratori forcat en 1 segon, % predit)":"fev1",
    "Insuficiencia Pancreatica":"pancreas","Pseudomonas":"pseudomonas","Staphylococcus":"staphylococcus",
    "Haemophilus":"haemophilus","Burkholderia":"burkholderia","Stenotrophomonas":"stenotrophomonas",
    "Aspergillus":"aspergillus","Cap":"cap_infeccio","Diagnostic FQ IA":"diagnostic"
}
df = df_raw.rename(columns=mapeig)
df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

if "diagnostic" not in df.columns:
    st.error("La columna 'diagnostic' no existeix: no es pot entrenar ni mostrar mètriques.")
    st.stop()

features = [c for c in df.columns if c != "diagnostic" and c != "id_pacient"]
X = df[features]
y = df["diagnostic"]

# train/test per mostrar mètriques
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42, test_size=0.25)

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# mètriques
st.subheader("Mètriques del model (split 75/25)")
acc = accuracy_score(y_test, y_pred)
st.write(f"**Accuracy:** {acc:.3f}")

st.subheader("Report de classificació")
st.text(classification_report(y_test, y_pred, digits=3))

# matriu de confusió
st.subheader("Matriu de confusió")
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(4,3))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
ax.set_xlabel("Predicció")
ax.set_ylabel("Real")
st.pyplot(fig)

# feature importance gràfic
st.subheader("Importància de les característiques")
importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(8,4))
sns.barplot(x=importances.values, y=importances.index, ax=ax2)
st.pyplot(fig2)

st.markdown("---")
st.write("Notas: aquestes mètriques es presenten com a guia. Amb més dades o validació creuada obtindríem mesures més robustes.")
