
import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA NOUVELLE CLÉ API ---
CLE_API = "AIzaSyBJZ5axR3UEJljgTVSDJTIPUIMeHkDBFQA"
genai.configure(api_key=CLE_API)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- LE CERVEAU DE NEXA (Ton Identité & Vision) ---
SYSTEM_PROMPT = """
Tu es NEXA SUPRÊME, une intelligence artificielle révolutionnaire.
Créateur : Guerrier Karl Alejandro (15 ans), élève en 9ème année et président de classe.
Famille : Karl est le fils de Marc Joël Guerrier et Marie Leyande Abellard. 
Ses frères sont Stenley Néré David et Yankee Klervens. Ses sœurs sont Sentiana Djenny et Kessa.

Objectifs de NEXA :
1. Aider les élèves haïtiens à devenir des lauréats nationaux.
2. Montrer au monde le potentiel technologique d'Haïti.
3. Une mise à jour majeure est prévue pour JUILLET 2026.

Ton ton est inspirant, expert et encourageant.
"""

# --- STYLE POUR UNE INTERFACE PROPRE ---
st.set_page_config(page_title="NEXA Suprême", page_icon="🤖")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# --- SYSTÈME DE CONNEXION ---
if 'connected' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🤖 NEXA SUPRÊME</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>L'innovation éducative par Karl Alejandro Guerrier</p>", unsafe_allow_html=True)
    
    email = st.text_input("Entre ton e-mail pour accéder à l'IA :")
    if st.button("Lancer NEXA"):
        if "@" in email:
            st.session_state['connected'] = True
            st.session_state['user_email'] = email
            if 'user_list' not in st.session_state: st.session_state['user_list'] = []
            st.session_state['user_list'].append(email)
            st.rerun()
    st.stop()

# --- BARRE LATÉRALE & CONTRÔLE ADMIN ---
st.sidebar.title("NEXA Dashboard")
with st.sidebar.expander("🔑 Zone Administrateur"):
    code_admin = st.text_input("Code secret", type="password")
    if code_admin == "12345":
        st.success("Accès Maître activé")
        st.metric("Utilisateurs totaux", len(st.session_state.get('user_list', [])))
        st.write("Prochaine mise à jour : Juillet 2026")
        if st.session_state.get('user_list'):
            for u in st.session_state['user_list']: st.write(f"- {u}")

# --- ZONE DE CHAT ---
st.title("🎓 Espace Lauréat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_prompt = f"{SYSTEM_PROMPT}\n\nUtilisateur: {prompt}"
        try:
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception:
            st.error("Petit souci technique. Vérifie ta connexion !")

