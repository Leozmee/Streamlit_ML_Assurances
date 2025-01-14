import streamlit as st
import joblib

page= st.sidebar.selectbox("Naviguation",["Accueil","Calcul des charges"])


if page == "Accueil":
    st.header("Bienvenue sur l'application")
    st.write("Utilisez le menu à gauche pour accéder aux différentes fonctionnalités.")


if page == "Calcul des charges":
   
    st.header("Renseignez vos informations")
    st.write("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁")
    age=st.number_input("Age",min_value=18,max_value=100)
    poids=st.slider("Poids en kg",min_value=20.0,max_value=300.0,step=0.1)
    size=st.number_input("Taille en cm",min_value=15,max_value=250)
    size_convert= size / 100
    bmi = round(poids / (size_convert ** 2), 2)
    st.write(f"Votre IMC est",bmi)
    sexe=st.selectbox("Sexe",options=['Homme','Femme'])
    is_smoker=st.selectbox("Est Fumeur",options=['Oui','Non'])
    sexe_encode = 0 if sexe == "Femme" else 1
    is_smoker_encode= 0 if is_smoker == "0" else 1

    if st.button("Valider") :
     st.write("Le montant des charges à payer est :")


#if st.button ("go") :
#    st.write ("Hello world")
#    st.session_state["key1"]=42
#else: 
#    st.session_state["key1"]=30

#st.write (st.session_state["key1"])

