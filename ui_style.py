# ui_style.py — Banner fijo #CC371D; gutter 1 cm; oculta header/toolbar de Streamlit (selector exacto)
import os, base64, re
import streamlit as st

TOKENS = {
    "brand_red": "#CC371D",
    "maxw": "1160px",
    "logo_h": "72px",
    "text": "#111827",
    "muted": "#475467",
    "border": "#e6e8ef",
    "shadow_sm": "0 6px 14px rgba(16,24,40,.08)",
    "title_size": "28px",
}

def _file_to_data_uri(path: str) -> str | None:
    try:
        if not os.path.exists(path):
            return None
        mime = "image/png"
        p = path.lower()
        if p.endswith(".svg"): mime = "image/svg+xml"
        elif p.endswith(".jpg") or p.endswith(".jpeg"): mime = "image/jpeg"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None

def boot_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

      html, body, .stApp { margin:0 !important; padding:0 !important; background:#fff !important; }

      /* ===== OCULTAR headers/toolbar/decoration nativos de Streamlit ===== */
      /* Selector EXACTO que nos pasaste + variantes */
      div.stAppToolbar.st-emotion-cache-14vh5up.e3g0k5y2,
      [data-testid="stToolbar"],
      .stAppToolbar, .stAppHeader,
      div[class^="stAppToolbar"], div[class*=" stAppToolbar"],
      [data-testid="stToolbarActions"], .stToolbarActions,
      [data-testid="stAppDeployButton"], .stAppDeployButton,
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      #MainMenu, .stMainMenu, [data-testid="stMainMenu"],
      header[data-testid="stHeader"], [data-testid="stHeader"],
      /* fallback por si cambian clases/inline styles */
      body > div:has(> div[class*="stAppToolbar"]) {
        display:none !important; visibility:hidden !important;
        height:0 !important; min-height:0 !important; overflow:hidden !important;
        opacity:0 !important; pointer-events:none !important;
        position:absolute !important; top:-9999px !important; left:-9999px !important;
      }

      /* Reset de paddings/márgenes por defecto */
      section[data-testid="stMain"]           { padding:0 !important; margin:0 !important; }
      div[data-testid="stMainBlockContainer"] { padding:0 !important; margin:0 !important; }
      .stAppViewContainer .main               { padding:0 !important; margin:0 !important; }
      .stAppViewContainer .main .block-container {
        padding:0 !important; margin:0 !important;
        max-width:100% !important; width:100% !important; box-sizing:border-box;
      }

      html, body, [class*="css"] {
        font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif !important;
        color:#111827;
      }
    </style>
    """, unsafe_allow_html=True)

def inject_css():
    st.markdown(f"""
    <style>
      :root {{
        --banner-h: 100px;   /* altura efectiva del banner para el spacer */
        --gutter-hero: 24px;
      }}

      /* ===== Banner fijo (encima de todo) ===== */
      .gc-banner-wrap {{
        position: fixed; top: 0; left: 0; right: 0;
        z-index: 1000;
        background: {TOKENS["brand_red"]};
        box-shadow: 0 4px 18px rgba(0,0,0,.15);
        width: 100%;
      }}
      .gc-banner {{
        display:flex; align-items:center; gap:16px;
        padding:20px var(--gutter-hero);
        min-height: 60px;
        box-sizing:border-box;
      }}
      .gc-banner .logo {{ height:{TOKENS["logo_h"]}; }}
      .gc-banner .title {{ color:#fff; font-weight:900; font-size:32px; line-height:1; }}
      .gc-banner-spacer {{ height: var(--banner-h); }}

      /* ===== Gutter global del contenido (1 cm) ===== */
      section[data-testid="stMain"],
      div[data-testid="stMainBlockContainer"],
      .stAppViewContainer .main .block-container {{
        padding-left: 1cm !important;
      }}

      /* ===== Home: filas ===== */
      .option-row {{ max-width:{TOKENS["maxw"]}; margin:8px 0 20px 0; padding:0; box-sizing:border-box; }}
      .opt-thumb {{
        width:100%; max-width:140px; aspect-ratio:16/10; overflow:hidden; border-radius:12px;
        border:1px solid {TOKENS["border"]}; box-shadow:{TOKENS["shadow_sm"]}; background:#fff; margin:0 !important;
      }}
      .opt-thumb img {{ width:100%; height:100%; object-fit:cover; display:block; }}
      .opt-title {{ font-size:20px; font-weight:800; margin:0 0 6px; }}
      .opt-desc  {{ font-size:16px; color:{TOKENS["muted"]}; line-height:1.5; margin:0 0 8px; }}

      @media (max-width: 900px) {{
        section[data-testid="stMain"],
        div[data-testid="stMainBlockContainer"],
        .stAppViewContainer .main .block-container {{
          padding-left: 12px !important;
        }}
      }}
    </style>
    """, unsafe_allow_html=True)

def render_banner(title: str, logo_path: str = "logos/garnier.png"):
    inject_css()
    logo_src = _file_to_data_uri(logo_path) or "https://placehold.co/160x48?text=LOGO"
    st.markdown(
        f"""
        <div class="gc-banner-wrap">
          <div class="gc-banner">
            <img class="logo" src="{logo_src}" alt="logo" />
            <div class="title">{title}</div>
          </div>
        </div>
        <div class="gc-banner-spacer"></div>
        """,
        unsafe_allow_html=True
    )

def render_topbar(title: str, logo_path: str = "logos/garnier.png"):
    inject_css()
    st.markdown(
        f"""
        <div style="max-width:{TOKENS["maxw"]};margin:10px 0 0 0;padding:0;">
          <div style="display:flex;align-items:center;gap:.75rem;">
            <img src="{_file_to_data_uri(logo_path) or 'https://placehold.co/160x48?text=LOGO'}" style="height:{TOKENS["logo_h"]};" />
            <h1 style="font-size:{TOKENS["title_size"]};font-weight:900;margin:0;">{title}</h1>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_topbar_with_button(title: str, button_label: str = "← Volver al inicio", button_key: str = "back_btn", on_click=None, logo_path: str = "logos/garnier.png"):
    inject_css()
    left, right = st.columns([0.78, 0.22])
    with left:
        render_topbar(title, logo_path)
    with right:
        st.markdown("<div style='display:flex;justify-content:flex-end;align-items:center;height:100%;padding-top:6px;'>", unsafe_allow_html=True)
        st.button(button_label, key=button_key, type="secondary", on_click=on_click)
        st.markdown("</div>", unsafe_allow_html=True)

def yt_thumb(url: str) -> str:
    m = re.search(r"(?:youtu\\.be/|youtube\\.com/(?:watch\\?v=|embed/))([A-Za-z0-9_-]{{6,}})", url or "")
    vid = m.group(1) if m else None
    return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else "https://placehold.co/480x270?text=Video"
