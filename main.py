import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE L'API GEMINI ---
# Ta clé API est maintenant intégrée
genai.configure(api_key="AIzaSyCR1bWEDmXFtD8Z6_xRF7CNlbmlsgzwQVA")
model = genai.GenerativeModel('gemini-1.5-flash')

# Instruction système : Définit l'identité et l'objectif de NEXA
NEXA_PROMPT = (
    "Tu es NEXA, une IA éducative créée par le développeur Karl Alejandro. "
    "Ton objectif principal est d'aider les élèves haïtiens à préparer "
    "leurs examens de 9ème année. Tu dois être pédagogique, précis sur le "
    "programme scolaire haïtien et toujours encourager les élèves."
)

# Configuration de la page
st.set_page_config(page_title="NEXA Suprême", page_icon="🎓", layout="centered")

# --- SYSTÈME DE CONNEXION ---
if 'connected' not in st.session_state:
    st.title("🤖 NEXA SUPRÊME")
    st.write("### L'IA au service de l'éducation en Haïti")
    
    email = st.text_input("Entre ton e-mail pour accéder aux révisions :")
    if st.button("Se connecter"):
        if "@" in email:
            st.session_state['connected'] = True
            st.session_state['user_email'] = email
            st.rerun()
        else:
            st.error("Oups ! Entre un e-mail valide pour continuer.")
else:
    # --- BARRE LATÉRALE (ADMIN & PARAMÈTRES) ---
    st.sidebar.title("Tableau de bord NEXA")
    st.sidebar.write(f"Connecté : {st.session_state['user_email']}")
    
    with st.sidebar.expander("⚙️ Paramètres Admin"):
        code = st.text_input("Code secret", type="password")
        if code == "12345":
            st.success("Accès Administrateur ✅")
            st.info("Statistiques : 100 utilisateurs actifs")
            st.write("Statut serveur : Opérationnel")
        elif code != "":
            st.error("Code incorrect")

    # --- ZONE DE CHAT PRINCIPALE ---
    st.title("🎓 Espace de Révision")
    st.write("Pose tes questions de mathématiques, physique, histoire ou français !")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Affichage de l'historique des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée de l'utilisateur
    if prompt := st.chat_input("Ex: Explique-moi la règle de trois"):
        # Ajouter le message de l'utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Générer la réponse avec Gemini
        with st.chat_message("assistant"):
            # On envoie l'instruction système + la question pour que l'IA reste dans son rôle
            full_prompt = f"{NEXA_PROMPT}\n\nQuestion de l'élève: {prompt}"
            try:
                response = model.generate_content(full_prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Désolé, j'ai un petit problème technique. Réessaie dans un instant !")

