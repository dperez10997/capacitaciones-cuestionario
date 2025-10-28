# pages/pg_produccion.py — Producción (iframe YouTube dentro de caja 16:9, 12cm de ancho)
import re
import streamlit as st
from ui_style import boot_css, render_banner

st.set_page_config(page_title="Producción — Capacitaciones eSP", page_icon="🎓", layout="wide")
boot_css()
render_banner("Producción")

# ===== Estilos: caja 16:9, ancho controlado =====
st.markdown("""
<style>
  :root { --video-w: 12cm; } /* ⇦ ajusta el ancho si lo quieres distinto */

  .video-wrap { margin: 14px 0 22px 0; display:flex; flex-direction:column; align-items:center; }
  .video-title { font-weight: 800; margin: 0 0 6px 0; align-self:flex-start; }

  .video-box{
    width: var(--video-w);
    aspect-ratio: 16 / 9;              /* altura se calcula sola */
    border: 1px solid #e6e8ef; border-radius: 12px;
    box-shadow: 0 4px 10px rgba(16,24,40,.06);
    overflow: hidden; background: #f5f6f8;
  }
  .video-box iframe{
    width: 100%; height: 100%; border:0; display:block;
  }
</style>
""", unsafe_allow_html=True)

def yt_embed(url: str) -> str:
    """Convierte URLs de YouTube a formato embed, conservando ?t= como ?start="""
    if not url:
        return ""
    # extraer id de video
    m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{6,})", url)
    vid = m.group(1) if m else None
    if not vid:
        return ""
    # segundos de inicio
    start = 0
    m2 = re.search(r"[?&]t=(\d+)", url)  # soporta ...&t=34s o &t=34
    if m2:
        try:
            start = int(m2.group(1))
        except:  # noqa: E722
            start = 0
    start_q = f"?start={start}" if start > 0 else ""
    return f"https://www.youtube.com/embed/{vid}{start_q}"

def video_block(title: str, url: str | None = None):
    st.markdown(f"<div class='video-wrap'><div class='video-title'>{title}</div>", unsafe_allow_html=True)
    if url:
        embed = yt_embed(url)
        if embed:
            st.markdown(
                f"<div class='video-box'><iframe src='{embed}' "
                "title='YouTube video' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share' allowfullscreen></iframe></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown("<div class='video-box' style='display:grid;place-items:center;color:#98A2B3;font-weight:700;'>URL inválida</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='video-box' style='display:grid;place-items:center;color:#98A2B3;font-weight:700;'>VIDEO PENDIENTE</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.write("### Qué verás aquí")
st.caption("Videos cortos para comprender el flujo de Producción: creación de trabajos, presupuestos, OCs, búsqueda e ítems.")

# Orden 01 → 06 (05 pendiente)
video_block("01 — Creación de Trabajos", "https://www.youtube.com/watch?v=J1kXpEanBFg&t=12s")
video_block("02 — Creación de Presupuestos", "https://www.youtube.com/watch?v=8JTWUaRDYqI&t=13s")
video_block("03 — Órdenes de compra", "https://www.youtube.com/watch?v=v7zgMEE_880&t=1s")
video_block("04 — Búsqueda de Trabajos", "https://www.youtube.com/watch?v=YgnH36vwk_s")
video_block("05 — (pendiente)")
video_block("06 — Ítems", "https://www.youtube.com/watch?v=IH_EO4-dcMU&t=4s")
video_block("07 — (Campañas y Productos)", "https://www.youtube.com/watch?v=sDm6pZFp4Gk")