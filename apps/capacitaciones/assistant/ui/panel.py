import streamlit as st

# ============================
# Panel integrado en la página
# ============================
def render_panel():
    st.subheader("Asistente Virtual de Capacitaciones (Integrado)")
    st.write("Este es el asistente en versión integrada en la pantalla.")


# ========================================
# Chatbot flotante de demostración: Ferchito
# ========================================
def render_floating_demo():
    # Inicializar historial de conversación
    if "ferchito_chat" not in st.session_state:
        st.session_state.ferchito_chat = [
            {
                "role": "assistant",
                "text": "👋 Hola, soy **Ferchito**. Pregúntame lo que quieras sobre capacitaciones."
            }
        ]

    # CSS del contenedor flotante
    st.markdown(
        """
        <style>
        .chat-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 340px;
            height: 480px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            background: white;
            font-family: Arial, sans-serif;
            z-index: 9999;
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            background:#2c7be5; 
            color:white; 
            padding:10px; 
            font-weight:bold;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        }
        .chat-body {
            flex:1; 
            padding:10px; 
            overflow-y:auto; 
            font-size:14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Abrir contenedor
    st.markdown(
        '<div class="chat-container"><div class="chat-header">🤖 Ferchito – Chat Demo</div>',
        unsafe_allow_html=True
    )

    # Historial de mensajes
    st.markdown('<div class="chat-body">', unsafe_allow_html=True)
    for msg in st.session_state.ferchito_chat:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align:right; margin:6px 0;'><b>Tú:</b> {msg['text']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='margin:6px 0; background:#e9f2ff; padding:6px; "
                f"border-radius:6px;'><b>Ferchito:</b> {msg['text']}</div>",
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # Entrada de usuario con chat_input (real)
    user_msg = st.chat_input("Escribe aquí...")
    if user_msg:
        st.session_state.ferchito_chat.append({"role": "user", "text": user_msg})
        st.session_state.ferchito_chat.append({
            "role": "assistant",
            "text": "Todavía no te puedo dar información, estoy aprendiendo para contestar 🤖"
        })

    # Cerrar el div flotante
    st.markdown('</div>', unsafe_allow_html=True)
