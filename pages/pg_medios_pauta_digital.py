# pages/pg_medios_pauta_digital.py — Pauta Digital (iframe YouTube dentro de caja 16:9, 12cm de ancho)
import re
import streamlit as st
from ui_style import boot_css, render_banner

st.set_page_config(page_title="Medios Pauta Digital — Capacitaciones eSP", page_icon="🎓", layout="wide")
boot_css()
render_banner("Medios Pauta Digital")

st.markdown("""
<style>
  :root { --video-w: 12cm; }

  .video-wrap { margin: 14px 0 22px 0; display:flex; flex-direction:column; align-items:center; }
  .video-title { font-weight: 800; margin: 0 0 6px 0; align-self:flex-start; }

  .video-box{ width: var(--video-w); aspect-ratio: 16 / 9;
    border: 1px solid #e6e8ef; border-radius: 12px; box-shadow: 0 4px 10px rgba(16,24,40,.06);
    overflow: hidden; background: #f5f6f8; }
  .video-box iframe{ width:100%; height:100%; border:0; display:block; }
</style>
""", unsafe_allow_html=True)

def yt_embed(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{6,})", url or "")
    vid = m.group(1) if m else None
    if not vid:
        return ""
    start = 0
    m2 = re.search(r"[?&]t=(\d+)", url)
    if m2:
        try: start = int(m2.group(1))
        except: start = 0
    start_q = f"?start={start}" if start > 0 else ""
    return f"https://www.youtube.com/embed/{vid}{start_q}"

def video_block(title: str, url: str | None = None):
    st.markdown(f"<div class='video-wrap'><div class='video-title'>{title}</div>", unsafe_allow_html=True)
    if url:
        embed = yt_embed(url)
        if embed:
            st.markdown(
                f"<div class='video-box'><iframe src='{embed}' title='YouTube video' "
                "allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' allowfullscreen></iframe></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown("<div class='video-box' style='display:grid;place-items:center;color:#98A2B3;font-weight:700;'>URL inválida</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='video-box' style='display:grid;place-items:center;color:#98A2B3;font-weight:700;'>PRÓXIMAMENTE</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("### Qué verás aquí")
st.caption("Planeación, compra, optimización y medición en plataformas digitales. Próximamente.")
# Agregamos videos cuando los tengas.
