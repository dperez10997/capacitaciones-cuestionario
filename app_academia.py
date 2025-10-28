# app_academia.py — Home con banner, menú "Recursos", tarjetas y dock de chatbot
import os, base64, mimetypes
import streamlit as st
from ui_style import boot_css, inject_css, render_banner

st.set_page_config(
    page_title="Capacitaciones eSP",
    page_icon="🎓",
    layout="wide"
)

boot_css()
inject_css()
render_banner("Capacitaciones eSP", logo_path="logos/garnier.png")

# ===== util: convertir imagen local a data-URI (para <img> HTML controlado) =====
def _img_data_uri(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        mime = "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# ===================== MENÚ + Recursos (alineado a la derecha con margen) =====================
st.markdown(
    """<style>
:root{ --menu-right-offset: 120px; }

/* Contenedor del menú */
.gc-banner-menu{
  position:fixed;
  top:calc(var(--banner-h)/2 - 22px);
  right:calc(var(--gutter-hero) + var(--menu-right-offset));
  z-index:1001; font-family:inherit;
}

/* Botón ROJO del banner */
.gc-banner-menu .gc-menu-btn{
  background:#CC371D !important;
  color:#fff !important;
  font-weight:700;
  padding:10px 12px;
  border-radius:10px;
  border:1px solid rgba(0,0,0,.08) !important;
  cursor:pointer; user-select:none;
  box-shadow:0 4px 10px rgba(0,0,0,.08);
}
.gc-banner-menu .gc-menu-btn:hover{ background:#B63019 !important; }

/* Dropdown */
.gc-dd{
  display:none; position:absolute; right:0; top:calc(100% + 8px);
  min-width:260px; background:#fff; color:#111827; border:1px solid #e6e8ef; border-radius:12px;
  box-shadow:0 16px 40px rgba(16,24,40,.16),0 3px 8px rgba(16,24,40,.06); overflow:hidden
}
.gc-dd a,.gc-dd button{
  display:flex; align-items:center; gap:10px; width:100%; text-align:left; padding:12px 14px;
  color:#111827; text-decoration:none; background:#fff; border:0; font-size:14px; cursor:pointer
}
.gc-dd a:hover,.gc-dd button:hover{ background:#f5f6f8 }
.gc-menu-wrap:hover .gc-dd{ display:block }
.gc-menu-toggle{ display:none }
.gc-menu-toggle:checked + label + .gc-dd{ display:block }
.gc-menu-label{ display:inline-block }

@media (max-width: 900px){
  :root{ --menu-right-offset: 0px; }
  .gc-banner-menu{ right:var(--gutter-hero); }
}
</style>
<div class="gc-banner-menu">
  <div class="gc-menu-wrap">
    <input id="gc-menu-toggle" type="checkbox" class="gc-menu-toggle" />
    <label for="gc-menu-toggle" class="gc-menu-label"><span class="gc-menu-btn">+ Recursos</span></label>
    <div class="gc-dd">
      <a href="/pg_finanzas">📇 Contactar Finanzas</a>
      <a href="https://example.com/faq" target="_blank" rel="noopener">❓ Preguntas frecuentes</a>
      <a href="mailto:soporte@empresa.com?subject=Reporte%20Capacitaciones%20eSP&body=Describe%20el%20problema%20(a%C3%B1ade%20capturas%20si%20puedes).">🛠️ Reportar un problema</a>
      <a href="https://status.cloud.google.com" target="_blank" rel="noopener">🟢 Estado de plataformas</a>
      <a href="https://calendar.google.com" target="_blank" rel="noopener">🗓️ Calendario de capacitaciones</a>
    </div>
  </div>
</div>""",
    unsafe_allow_html=True,
)

# ===================== HERO =====================
st.markdown(
    """
    <div class="home-hero">
      <div class="hero-copy">
        <h2>Bienvenido</h2>
        <p>
          En esta página encontrarás videos explicativos sobre el uso de <strong>eSilent Partner</strong> y los flujos de trabajo.
          El contenido se actualiza periódicamente para mantener su utilidad y relevancia.
        </p>
        <p class="muted">Selecciona un área para comenzar:</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ===================== Enlace robusto (mantengo historial navegador) =====================
def safe_page_link(page_path: str, label: str, key: str):
    if not os.path.exists(page_path):
        st.info(f"⚠️ No pude abrir la página: '{os.path.basename(page_path)}'. Verifica que exista en /pages y reinicia la app.")
        return
    try:
        st.page_link(page_path, label=label)
        return
    except Exception:
        pass
    if st.button(label, key=key):
        try:
            st.switch_page(page_path)
        except Exception:
            st.warning("No pude abrir la página. Verifica que exista en /pages y reinicia la app.")

# ===================== Helper para filas (IMAGEN HTML dentro del marco) =====================
def option_row(img_path: str, title: str, desc: str, page_path: str, link_key: str):
    st.markdown('<div class="option-row">', unsafe_allow_html=True)
    c1, c2 = st.columns([0.12, 0.88], vertical_alignment="center")
    with c1:
        data_uri = _img_data_uri(img_path) if img_path else None
        if data_uri:
            # control total del tamaño dentro de .opt-thumb
            st.markdown(f'<div class="opt-thumb"><img src="{data_uri}" alt="{title}" /></div>', unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="opt-thumb opt-thumb--ph">
                  <div class="ph"></div>
                </div>
                """,
                unsafe_allow_html=True
            )
    with c2:
        st.markdown(f"<div class='opt-title'>{title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='opt-desc'>{desc}</div>", unsafe_allow_html=True)
        # Usa navegación nativa para mantener back/forward del navegador
        safe_page_link(page_path, label="▶ Ver videos", key=f"go_{link_key}")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== Tarjetas =====================
st.markdown('<div class="cards-wrap">', unsafe_allow_html=True)

option_row(
    img_path="logos/opt_prod.jpg",
    title="Producción",
    desc="Flujo de trabajo, estimación, ODC, ejecución y cierre. Videos para comprender el proceso end-to-end y mejores prácticas.",
    page_path="pages/pg_produccion.py",
    link_key="prod",
)

option_row(
    img_path="logos/opt_digital.jpg",
    title="Medios Pauta Digital",
    desc="Planeación de campañas, flujos de aprobación y recomendaciones para optimización y medición en plataformas digitales.",
    page_path="pages/pg_medios_pauta_digital.py",
    link_key="digital",
)

option_row(
    img_path="logos/opt_atl.jpg",
    title="Medios ATL",
    desc="Conceptos base de planificación ATL, formatos, pautas y roles del equipo para campañas en TV, radio y exteriores.",
    page_path="pages/pg_medios_atl.py",
    link_key="atl",
)

st.markdown('</div>', unsafe_allow_html=True)

# ===================== Dock del chatbot (si tienes CHATBOT_URL definido, se muestra) =====================
def _get_chatbot_url() -> str:
    url = os.environ.get("CHATBOT_URL", "")
    try:
        if "CHATBOT_URL" in st.secrets:  # type: ignore[attr-defined]
            url = st.secrets["CHATBOT_URL"] or url  # type: ignore[index]
    except Exception:
        pass
    return url.strip()

CHATBOT_URL = _get_chatbot_url()

if CHATBOT_URL:
    st.markdown(
        f"""
        <style>
          .chatdock {{
            position: fixed;
            top: calc(var(--banner-h) + 16px);
            right: var(--gutter-hero);
            width: clamp(360px, 34vw, 520px);
            height: calc(100vh - var(--banner-h) - 32px);
            background: #ffffff;
            border: 1px solid #e6e8ef; border-radius: 14px;
            box-shadow: 0 12px 32px rgba(16,24,40,.12);
            overflow: hidden; z-index: 60;
          }}
          .chatdock iframe {{ width: 100%; height: 100%; border: 0; display: block; }}
          @media (max-width: 1200px) {{ .chatdock {{ display: none; }} }}
        </style>
        <div class="chatdock">
          <iframe src="{CHATBOT_URL}" allow="clipboard-write; microphone *; camera *; geolocation *"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )

# ===================== Footer =====================
st.markdown(
    """
    <div style="height:40px"></div>
    <div style="font-size:12px;color:#98A2B3;padding-left:var(--gc-gutter-cards);padding-bottom:24px;">
      Capacitaciones internas · Grupo Garnier
    </div>
    """,
    unsafe_allow_html=True
)
