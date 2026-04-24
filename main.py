import streamlit as st
from groq import Groq

# --- CONFIGURATION GROQ ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# --- IDENTITÉ DE NEXA ---
SYSTEM_PROMPT = """
Tu es NEXA SUPRÊME, l'IA la plus rapide d'Haïti.
Créateur : Guerrier Karl Alejandro (15 ans), président de classe à l'IGJ.
Famille : Karl est le fils de Marc Joël Guerrier et Marie Leyande Abellard. 
Ses frères : Stenley Néré David, Yankee Klervens. Ses sœurs : Sentiana Djenny, Kessa.
Mise à jour majeure : JUILLET 2026.
Ton ton est poli, encourageant et très gentil.
"""

st.set_page_config(page_title="NEXA Suprême", page_icon="🎓")

if 'user_list' not in st.session_state: st.session_state['user_list'] = []

if 'connected' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🤖 NEXA SUPRÊME</h1>", unsafe_allow_html=True)
    email = st.text_input("Ton email :")
    if st.button("Lancer"):
        if "@" in email:
            st.session_state['connected'] = True
            st.session_state['user_email'] = email
            if email not in st.session_state['user_list']: st.session_state['user_list'].append(email)
            st.rerun()
    st.stop()

# Barre latérale Admin
with st.sidebar.expander("🔑 Admin (Code: 12345)"):
    if st.text_input("Code", type="password") == "12345":
        st.metric("Élèves", len(st.session_state['user_list']))
        for u in st.session_state['user_list']: st.text(u)

st.title("🎓 Mentor Intelligent")

if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Dis-moi ce que tu veux apprendre..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ICI LE CHANGEMENT : llama-3.1-8b-instant
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                temperature=0.8,
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Erreur technique : {e}")
