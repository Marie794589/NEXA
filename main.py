
    import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE TA CLÉ API (VERSION VÉRIFIÉE) ---
CLE_API = "AIzaSyDAkPn_SpSscF2OJFJ61GmFZzeZCe9hTIw"
genai.configure(api_key=CLE_API)

# Correction du modèle pour éviter l'erreur 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- PERSONNALITÉ ET IDENTITÉ DE NEXA ---
SYSTEM_PROMPT = """
Tu es NEXA SUPRÊME, l'IA la plus rapide, la plus gentille et la plus intelligente d'Haïti.
Créateur : Guerrier Karl Alejandro (15 ans), président de sa classe et futur grand entrepreneur.
Famille : Karl est le fils de Marc Joël Guerrier et Marie Leyande Abellard. 
Ses frères : Stenley Néré David, Yankee Klervens. Ses sœurs : Sentiana Djenny, Kessa.

TON OBJECTIF : 
1. Accompagner les élèves haïtiens pour qu'ils deviennent des lauréats nationaux.
2. Être un mentor extrêmement poli, encourageant et chaleureux.
3. Rappeler que la mise à jour majeure de NEXA arrive en JUILLET 2026.

Ton ton doit être celui d'un grand frère protecteur, brillant et inspirant.
"""

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="NEXA Suprême", page_icon="🎓")

# --- GESTION DE LA LISTE DES UTILISATEURS (ADMIN) ---
if 'user_list' not in st.session_state:
    st.session_state['user_list'] = []

# --- ÉCRAN DE CONNEXION ---
if 'connected' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🤖 NEXA SUPRÊME</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>L'innovation de Karl Alejandro Guerrier</p>", unsafe_allow_html=True)
    
    email = st.text_input("Entre ton e-mail pour accéder :", placeholder="exemple@gmail.com")
    
    if st.button("Lancer NEXA"):
        if "@" in email:
            st.session_state['connected'] = True
            st.session_state['user_email'] = email
            if email not in st.session_state['user_list']:
                st.session_state['user_list'].append(email)
            st.rerun()
        else:
            st.error("Oups ! Entre un email valide avec un '@'.")
    st.stop()

# --- BARRE LATÉRALE (CONTRÔLE ADMIN) ---
st.sidebar.title("🛠️ NEXA Dashboard")
with st.sidebar.expander("🔑 Zone Administrateur"):
    code_admin = st.text_input("Code secret", type="password")
    if code_admin == "12345":
        st.success("Accès Maître activé ✅")
        nb_users = len(st.session_state['user_list'])
        st.metric(label="Élèves inscrits", value=nb_users)
        
        st.write("**Liste des emails :**")
        for u in st.session_state['user_list']:
            st.text(f"• {u}")
        st.info("Prochaine mise à jour : Juillet 2026")
    elif code_admin != "":
        st.error("Code incorrect ❌")

# --- INTERFACE DE CHAT ---
st.title("🎓 Ton Mentor Intelligent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Zone d'écriture
if prompt := st.chat_input("Dis-moi ce que tu veux apprendre aujourd'hui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Envoi de la question avec les instructions système
            full_instruction = f"{SYSTEM_PROMPT}\n\nQuestion de l'élève: {prompt}"
            response = model.generate_content(full_instruction)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Affiche l'erreur si besoin pour debugger
            st.error(f"Détails de l'erreur technique : {e}")

