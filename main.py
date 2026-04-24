import streamlit as st
from groq import Groq

# --- CONFIGURATION GROQ (TA NOUVELLE CLÉ) ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- PERSONNALITÉ ET IDENTITÉ DE NEXA ---
SYSTEM_PROMPT = """
Tu es NEXA SUPRÊME, l'intelligence artificielle la plus rapide et la plus gentille d'Haïti.
Créateur : Guerrier Karl Alejandro (15 ans), président de sa classe à l'Institution Guillaume Jovin.
Famille : Karl est le fils de Marc Joël Guerrier et Marie Leyande Abellard. 
Ses frères : Stenley Néré David, Yankee Klervens. Ses sœurs : Sentiana Djenny, Kessa.

MISSION : 
1. Accompagner les élèves haïtiens pour qu'ils deviennent des lauréats nationaux (Objectif 10/10).
2. Être un mentor extrêmement poli, encourageant et chaleureux.
3. Rappeler que la mise à jour majeure de NEXA arrive en JUILLET 2026.

TON : Toujours bienveillant. Utilise des phrases comme "C'est une excellente question !" ou "Tu as le potentiel d'un lauréat !".
"""

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="NEXA Suprême", page_icon="🎓")

# --- GESTION DES UTILISATEURS ---
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

# --- BARRE LATÉRALE (PANNEAU ADMIN) ---
st.sidebar.title("🛠️ NEXA Dashboard")
with st.sidebar.expander("🔑 Zone Administrateur"):
    code_admin = st.text_input("Code secret", type="password")
    if code_admin == "12345":
        st.success("Accès Maître activé ✅")
        st.metric(label="Élèves inscrits", value=len(st.session_state['user_list']))
        for u in st.session_state['user_list']:
            st.text(f"• {u}")
        st.info("Mise à jour majeure : Juillet 2026")

# --- ZONE DE CHAT ---
st.title("🎓 Ton Mentor Intelligent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Dis-moi ce que tu veux apprendre aujourd'hui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Utilisation de Llama 3 8B (ultra-rapide)
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Erreur technique : {e}")
