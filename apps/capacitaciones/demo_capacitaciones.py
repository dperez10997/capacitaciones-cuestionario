# demo_capacitaciones.py — Demo independiente con chat embebido a la derecha
import streamlit as st

st.set_page_config(page_title="Demo Capacitaciones", layout="wide")

# ====== Layout: contenido izquierda + chat derecha ======
st.markdown("""
<style>
.chatbox {
  height: 76vh;                 /* alto visible */
  border: 1px solid #e6e8ef;    /* borde suave */
  border-radius: 14px;
  padding: 8px 10px;
  background: #ffffff;
  overflow-y: auto;             /* scroll interno */
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.chatbox h3 { margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

col_izq, col_der = st.columns([3, 2], gap="large")

with col_izq:
    st.title("Capacitaciones eSP — Demo")
    st.write("Aquí va tu contenido (listas, cards, videos, etc.).")

with col_der:
    st.markdown("<div class='chatbox'>", unsafe_allow_html=True)
    st.markdown("### Asistente de Capacitaciones")
    st.caption("Chat embebido (demo sin IA, no flotante)")

    # Historial aislado para esta pantalla
    if "cap_chat_hist" not in st.session_state:
        st.session_state.cap_chat_hist = []

    # Pintar historial
    for msg in st.session_state.cap_chat_hist:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada de mensaje
    prompt = st.chat_input("Escribe tu pregunta aquí…")
    if prompt:
        st.session_state.cap_chat_hist.append({"role": "user", "content": prompt})

        # Respuesta temporal (cuando tengamos API key, aquí conectamos Gemini + RAG)
        respuesta = (
            "Estoy listo para ayudarte. (Demo sin IA)\n\n"
            f"Me preguntaste: **{prompt}**\n\n"
            "Cuando activemos Gemini, responderé con citas a tu material."
        )
        with st.chat_message("assistant"):
            st.markdown(respuesta)

        st.session_state.cap_chat_hist.append({"role": "assistant", "content": respuesta})

    st.markdown("</div>", unsafe_allow_html=True)
