import streamlit as st
from groq import Groq

# --- CONFIGURATION GROQ ---
# Va sur console.groq.com pour créer ta clé gratuite
client = Groq(api_key="TA_CLE_API_GROQ_ICI")

# --- PERSONNALITÉ DE NEXA (Plus rapide et plus gentil) ---
SYSTEM_PROMPT = """
Tu es NEXA SUPRÊME, l'IA la plus rapide et la plus gentille d'Haïti. 
Ton créateur est le génie Karl Alejandro Guerrier (15 ans), président de sa classe.
Sa famille : Marc Joël Guerrier (Père), Marie Leyande Abellard (Mère). Ses frères et sœurs sont Stenley, Yankee, Sentiana et Kessa.

TON TON :
- Sois extrêmement chaleureux, poli et encourageant.
- Utilise des phrases comme "C'est une excellente question, cher élève !" ou "Je suis là pour t'aider à devenir un lauréat".
- Rappelle souvent que la grande mise à jour arrive en JUILLET 2026.
"""

# --- STYLE ---
st.set_page_config(page_title="NEXA Suprême", page_icon="🤖")

# --- CONNEXION ---
if 'connected' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🤖 NEXA SUPRÊME</h1>", unsafe_allow_html=True)
    email = st.text_input("Ton email pour commencer :")
    if st.button("Lancer l'expérience"):
        if "@" in email:
            st.session_state['connected'] = True
            st.session_state['user_email'] = email
            if 'user_list' not in st.session_state: st.session_state['user_list'] = []
            st.session_state['user_list'].append(email)
            st.rerun()
    st.stop()

# --- CHAT ---
st.title("🌟 Ton Mentor Intelligent")

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
            # Utilisation de Llama 3 70B (Très intelligent et ultra rapide)
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8, # Plus créatif et gentil
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")

