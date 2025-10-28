# pages/pg_finanzas.py — Contactar Finanzas
import streamlit as st
from ui_style import boot_css, render_banner

st.set_page_config(page_title="Contactar Finanzas — Capacitaciones eSP", page_icon="💼", layout="wide")

boot_css()
render_banner("Contactar Finanzas", logo_path="logos/garnier.png")

st.markdown("""
<style>
  .finz-wrap { max-width: 980px; margin: 6px 0 0 0; }
  .finz-card {
    background:#fff; border:1px solid #e6e8ef; border-radius:16px;
    box-shadow:0 8px 20px rgba(16,24,40,.08); padding:18px 20px; margin: 10px 0 16px 0;
  }
  .finz-title { font-weight: 900; font-size: 22px; margin: 6px 0 6px 0; }
  .finz-sub   { color:#475467; margin: 0 0 14px 0; }
  .finz-grid  { display:grid; grid-template-columns: 1fr 1fr; gap:14px; }
  .finz-item  { background:#f8fafc; border:1px solid #eef2f7; border-radius:12px; padding:12px 14px; }
  .finz-item b { display:block; margin-bottom:4px; }
  .finz-mail a { text-decoration:none; font-weight:700; }
  @media (max-width: 900px){ .finz-grid{ grid-template-columns: 1fr; } }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='finz-wrap'>", unsafe_allow_html=True)

st.markdown("<div class='finz-title'>¿Cómo podemos ayudarte?</div>", unsafe_allow_html=True)
st.markdown("<div class='finz-sub'>Canales oficiales del equipo de Finanzas para consultas operativas, presupuestos, OCs y facturación.</div>", unsafe_allow_html=True)

st.markdown("<div class='finz-card'>", unsafe_allow_html=True)
st.markdown("<div class='finz-grid'>", unsafe_allow_html=True)

st.markdown(
    """
    <div class='finz-item finz-mail'>
      <b>Correo del equipo</b>
      <div><a href="mailto:finanzas@empresa.com">finanzas@empresa.com</a></div>
      <small>Respuesta habitual: 24–48 h hábiles</small>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='finz-item'>
      <b>Horario de atención</b>
      <div>Lunes a Viernes, 8:00–17:30 (GMT-6)</div>
      <small>Fuera de horario, tu ticket quedará en cola para el siguiente día hábil.</small>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='finz-item'>
      <b>Responsables</b>
      <div>• Ana Morales — Presupuestos</div>
      <div>• Luis Pérez — Órdenes de Compra</div>
      <div>• Marta Rojas — Facturación</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='finz-item'>
      <b>Escalamientos</b>
      <div><a href="mailto:finanzas-jefatura@empresa.com">finanzas-jefatura@empresa.com</a></div>
      <small>Usar solo si tu caso supera el SLA comprometido.</small>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)  # finz-grid
st.markdown("</div>", unsafe_allow_html=True)  # finz-card

st.markdown("<div class='finz-card'>", unsafe_allow_html=True)
st.markdown("<b>FAQs rápidas</b>", unsafe_allow_html=True)
st.markdown(
    """
    - ¿Cómo solicito una OC? — Revisa el video en **Producción → Órdenes de compra**.
    - ¿Cuándo se actualiza el presupuesto? — Cierre semanal, cada viernes 16:00.
    - ¿A dónde envío facturas? — A **finanzas@empresa.com** con el ID de trabajo.
    """,
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # finz-wrap
