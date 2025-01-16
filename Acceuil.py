import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


model = joblib.load('serialized_model.pkl')
df = pd.read_csv('df_assu.csv')

X = df.drop('charges', axis=1)
y = df['charges']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
    st.markdown("---")
    st.write("Utilisez le menu à gauche pour accéder aux différentes fonctionnalités.")
    if st.button("Remplir le formulaire"):
        st.session_state.page = "Calcul des charges"

elif st.session_state.page == "Calcul des charges":
    st.header("Renseignez vos informations")
    st.markdown("---")

    age = st.number_input("Âge", min_value=18, max_value=100)
    poids = st.slider("Poids en kg", min_value=20.0, max_value=300.0, step=0.1)
    taille = st.number_input("Taille en cm", min_value=50, max_value=250)
    taille_convertie = taille / 100
    bmi = round(poids / (taille_convertie ** 2), 2)
    st.write(f"Votre IMC est : **<span style='color:green'>{bmi}</span>**", unsafe_allow_html=True)

    sexe = st.selectbox("Sexe", options=["male", "female"])
    fumeur = st.selectbox("Êtes-vous fumeur ?", options=["yes", "no"])
    enfants = st.number_input("Nombre d'enfants", min_value=0, max_value=10, step=1)
    region = st.selectbox("Région", options=["southwest", "southeast", "northwest", "northeast"])

    if st.button("Valider"):
        if age and taille and poids and sexe and fumeur and region:
            # Sauvegarde les données du user
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

elif st.session_state.page == "Affichage du résultat":
    st.header("Affichage du résultat")
    st.markdown("---")
    st.write("Voici la prédiction du montant de charges à payer.")

    if "user_data" in st.session_state:
        # Charge les données du user
        user_data = st.session_state.user_data

        # Conversion en df pour le modèle
        model_input_df = pd.DataFrame([user_data])
        try:
            # Prédiction ponctuelle
            charge_predite = model.predict(model_input_df)[0]

            # Estimation de la marge d'erreur basée sur les prédictions du test
            y_pred_test = model.predict(X_test)
            errors = y_pred_test - y_test
            mean_error = np.mean(errors)
            std_error = np.std(errors)

            #La marge d'erreur est définie comme l'écart-type des erreurs de prédiction sur l'ensemble de test.
            marge_erreur = std_error
            borne_inf = charge_predite - marge_erreur
            borne_sup = charge_predite + marge_erreur

            # Affichage du graphique
            fig, ax = plt.subplots(figsize=(10, 4))

            echelle_charges = np.linspace(0, 60000, 2)
            ax.plot(echelle_charges, [1, 1], '-', color='lightgray', linewidth=2)

            # Ajout de l'intervalle de prédiction
            ax.axvspan(borne_inf, borne_sup, ymin=0.4, ymax=0.6, color='lightpink', alpha=0.3)

            # Placement du point (moyenne de l'intervalle)
            ax.scatter(charge_predite, 1, color='red', s=60, zorder=5)
            ax.set_ylim(0.5, 1.5)
            ax.set_xlim(0, 60000)
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            ax.set_xlabel('Montant des charges (€)')
            ax.axvline(charge_predite, color='lightpink', linestyle='--', alpha=0.3)

            if charge_predite < 20000:
                position = "faibles"
            elif charge_predite < 40000:
                position = "moyennes"
            else:
                position = "élevées"

            ax.text(charge_predite, 1.3,
                    f'Vos charges : {charge_predite:.2f}€\n(charges {position})',
                    color='slateblue',
                    horizontalalignment='center',
                    verticalalignment='bottom')

            st.pyplot(fig)

            # Affichage de la fourchette de prédiction
            st.success(f"""Le montant des charges à payer est estimé entre :
                      **{borne_inf:.2f}€** et **{borne_sup:.2f}€**""")

        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")
