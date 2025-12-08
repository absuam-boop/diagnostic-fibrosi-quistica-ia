# pages/3_ℹ️_Informacio_sobre_la_Fibrosi_Quistica.py
import streamlit as st

st.set_page_config(page_title="ℹ️ Informació sobre la FQ", layout="centered")
st.title("ℹ️ Informació bàsica sobre la Fibrosi Quística")

st.markdown("""
**Què és la Fibrosi Quística (FQ)?**

La Fibrosi Quística és una malaltia genètica que afecta principalment els pulmons i el sistema digestiu. Es caracteritza per una producció d’un moc espès que causa infeccions pulmonars recidivants i problemes digestius.

**Diagnòstic:**
- Test de suor (mesurar clorurs en mmol/L). Valors elevats són indicatius.
- Proves genètiques per mutacions en el gen *CFTR*.
- Proves funcionals respiratòries (FEV1, FVC) per valorar afectació pulmonar.

**Important:**
Aquesta aplicació ofereix una predicció automatitzada basada en un model estadístic. No substitueix el diagnòstic clínic. Sempre cal confirmar amb proves mèdiques i un especialista.
""")

st.markdown("### Fonts i recomanacions per a la lectura")
st.markdown("""
- Protocols clínics i guies locals d'unitats de Fibrosi Quística.  
- Revisar proves complementàries: test de suor i estudi genètic.  
""")
