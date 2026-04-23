import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE TA NOUVELLE CLÉ API ---
CLE_API = "AIzaSyBDj61VVdhC-9-gvWWorEjcHIKVrqU_0g"
genai.configure(api_key=CLE_API)
# Utilisation de Flash pour la vitesse maximale
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PERSONNALITÉ ET IDENTITÉ DE NEXA ---
SYSTEM_PROMPT = """
Tu es NEXA SUPRÊME, l'IA la plus rapide, la plus gentille et la plus intelligente d'Haïti.
Créateur : Guerrier Karl Alejandro (15 ans), président de sa classe.
Famille : Karl est le fils de Marc Joël Guerrier et Marie Leyande Abellard. 
Ses frères : Stenley Néré David, Yankee Klervens. Ses sœurs : Sentiana Djenny, Kessa.

TON OBJECTIF : 
1. Accompagner les élèves haïtiens pour qu'ils deviennent des lauréats nationaux.
2. Être un mentor extrêmement poli, encourageant et chaleureux.
3. Rappeler que la mise à jour majeure de NEXA arrive en JUILLET 2026.

Ton ton doit être celui d'un grand frère protecteur et brillant.
"""

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="NEXA Suprême", page_icon="🤖")

# --- GESTION DE LA LISTE DES UTILISATEURS ---
if 'user_list' not in st.session_state:
    st.session_state['user_list'] = []

# --- ÉCRAN DE CONNEXION ---
if 'connected' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🤖 NEXA SUPRÊME</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>L'innovation de Karl Alejandro Guerrier</p>", unsafe_allow_html=True)
    
    email = st.text_input("Entre ton e-mail pour accéder :")
    
    if st.button("Lancer NEXA"):
        if "@" in email:
            st.session_state['connected'] = True
            st.session_state['user_email'] = email
            if email not in st.session_state['user_list']:
                st.session_state['user_list'].append(email)
            st.rerun()
        else:
            st.error("Email invalide.")
    st.stop()

# --- BARRE LATÉRALE (CONTRÔLE ADMIN) ---
st.sidebar.title("🛠️ NEXA Dashboard")
with st.sidebar.expander("🔑 Zone Administrateur"):
    code_admin = st.text_input("Code secret", type="password")
    if code_admin == "12345":
        st.success("Accès Maître activé")
        nb_users = len(st.session_state['user_list'])
        st.metric(label="Élèves inscrits", value=nb_users)
        
        st.write("**Emails des utilisateurs :**")
        for u in st.session_state['user_list']:
            st.text(f"• {u}")
    elif code_admin != "":
        st.error("Code incorrect")

# --- ZONE DE CHAT ---
st.title("🎓 Ton Mentor Intelligent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Pose ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # On combine le système et la question pour plus de gentillesse
            full_instruction = f"{SYSTEM_PROMPT}\n\nQuestion de l'élève: {prompt}"
            response = model.generate_content(full_instruction)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Petit souci technique. Vérifie ta batterie ou ta connexion !")
