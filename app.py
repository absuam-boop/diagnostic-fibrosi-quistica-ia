st.header("📋 Dades del pacient")

edat = st.number_input("Edat", 0, 100, 10, key="edat")
sexe = st.selectbox("Sexe (0 = Masculí, 1 = Femení)", [0, 1], key="sexe")
clor = st.number_input("Clor en test de la suor (mmol/L)", 0, 150, 30, key="clor")
mutacio = st.selectbox("Mutació CFTR (0 = No, 1 = Sí)", [0, 1], key="mutacio")
fev1 = st.number_input("FEV1 (%)", 0, 150, 100, key="fev1")

insuf_pancreatica = st.selectbox("Insuficiència pancreàtica", [0, 1], key="pancreas")
pseudomonas = st.selectbox("Pseudomonas", [0, 1], key="pseudomonas")
staphylococcus = st.selectbox("Staphylococcus", [0, 1], key="staph")
haemophilus = st.selectbox("Haemophilus", [0, 1], key="haemo")
burkholderia = st.selectbox("Burkholderia", [0, 1], key="burk")
stenotrophomonas = st.selectbox("Stenotrophomonas", [0, 1], key="steno")
aspergillus = st.selectbox("Aspergillus", [0, 1], key="aspergillus")
cap = st.selectbox("Cap infecció", [0, 1], key="cap")

if st.button("🧪 Fer diagnòstic amb IA"):

    dades_pacient = [[
        edat, sexe, clor, mutacio, fev1,
        insuf_pancreatica, pseudomonas, staphylococcus,
        haemophilus, burkholderia, stenotrophomonas,
        aspergillus, cap
    ]]

    prediccio = model.predict(dades_pacient)[0]

    if prediccio == 1:
        st.error("⚠️ POSSIBLE FIBROSI QUÍSTICA DETECTADA")
    else:
        st.success("✅ NO sembla Fibrosi Quística")
