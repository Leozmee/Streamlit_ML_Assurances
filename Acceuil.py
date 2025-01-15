import streamlit as st
import joblib
import pandas as pd

model = joblib.load('serialized_model.pkl')

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# Synchroniser le session state avec la sidebar
def navigate():
    st.session_state.page = st.session_state["menu"]

page = st.sidebar.selectbox(
    "Navigation",
    ["Accueil", "Calcul des charges", "Affichage du résultat"],
    key="menu",
    on_change=navigate
    
)

if st.session_state.page == "Accueil":
    st.header("Bienvenue sur l'application")
    st.write("Utilisez le menu à gauche pour accéder aux différentes fonctionnalités.")
    if st.button ("Remplir le formiulaire") :
        st.session_state.page = "Calcul des charges"

elif st.session_state.page == "Calcul des charges":
    st.header("Renseignez vos informations")
    st.write("  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁")
    

    age = st.number_input("Âge", min_value=18, max_value=100)
    poids = st.slider("Poids en kg", min_value=20.0, max_value=300.0, step=0.1)
    taille = st.number_input("Taille en cm", min_value=50, max_value=250)
    taille_convertie = taille / 100
    bmi = round(poids / (taille_convertie ** 2), 2)
    st.write(f"Votre IMC est : **<span style='color:green'>{bmi}</span>**",unsafe_allow_html=True)
    
    sexe = st.selectbox("Sexe", options=["Homme", "Femme"])
    fumeur = st.selectbox("Êtes-vous fumeur ?", options=["oui", "non"])
    enfants = st.number_input("Nombre d'enfants", min_value=0, max_value=10, step=1)
    region = st.selectbox("Région", options=["Sud-Ouest", "Sud-Est", "Nord-Ouest", "Nord-Est"])


    if st.button("Valider"):
        if age and taille and poids and sexe and fumeur and region:
            # Sauvegarde les données utilisateur
            st.session_state.user_data = {
                "age": age,
                "bmi": bmi,
                "sex": sexe,
                "children": enfants,
                "smoker": fumeur,
                "region": region,
            }
            st.session_state.page = "Affichage du résultat"
        else:
            st.error("Veuillez renseigner tous les champs.")
    st.write("  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁")

elif st.session_state.page == "Affichage du résultat":
    st.header("Affichage du résultat")
    st.write("Voici la prédiction du montant de charges à payer.")
    if "user_data" in st.session_state:
        # Charge les données du user
        user_data = st.session_state.user_data

        # Convertion en df pour le modèle
        model_input_df = pd.DataFrame([user_data])
        try:
            charge_predite = model.predict(model_input_df)[0]
            st.success(f"Le montant des charges à payer est de : **{charge_predite:.2f} €**")
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")

