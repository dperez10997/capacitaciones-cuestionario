# setup_training_bot_structure.py
# Crea la estructura de carpetas para el chatbot de capacitaciones (aislado)
# Ejecuta: python setup_training_bot_structure.py

from pathlib import Path
import textwrap

ROOT = Path(".")  # ajusta si quieres crearlo en otra ruta
BASE = ROOT / "apps" / "capacitaciones"
ASSIST = BASE / "assistant"

DIRS = [
    BASE,
    ASSIST,
    ASSIST / "privacy",
    ASSIST / "storage",
    ASSIST / "rag",
    ASSIST / "providers",
    ASSIST / "assistant",
    ASSIST / "quizzes",
    ASSIST / "analytics",
    ASSIST / "ui",
    BASE / "materials",
    BASE / "indices",
    BASE / "scripts",
]

FILES_WITH_CONTENT = {
    # Paquetes Python
    ASSIST / "__init__.py": "",
    (ASSIST / "privacy" / "__init__.py"): "",
    (ASSIST / "storage" / "__init__.py"): "",
    (ASSIST / "rag" / "__init__.py"): "",
    (ASSIST / "providers" / "__init__.py"): "",
    (ASSIST / "assistant" / "__init__.py"): "",
    (ASSIST / "quizzes" / "__init__.py"): "",
    (ASSIST / "analytics" / "__init__.py"): "",
    (ASSIST / "ui" / "__init__.py"): "",

    # Config plantilla
    ASSIST / "config.py": textwrap.dedent("""\
        from pathlib import Path
        import os

        # Flags
        ENABLE_TRAINING_BOT = os.getenv("ENABLE_TRAINING_BOT", "false").lower() == "true"
        PRIVACY_STRICT = os.getenv("PRIVACY_STRICT", "true").lower() == "true"

        # Proveedor LLM
        LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # gemini por defecto
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

        # Rutas
        BASE = Path(__file__).resolve().parents[2] / "apps" / "capacitaciones"
        MATERIALS_DIR = Path(os.getenv("MATERIALS_DIR", BASE / "materials"))
        INDICES_DIR = Path(os.getenv("INDICES_DIR", BASE / "indices"))
        RAG_DB_PATH = Path(os.getenv("RAG_DB_PATH", BASE / "capacitaciones.db"))

        # Seguridad
        MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "8000"))
        INSTRUCTOR_PIN = os.getenv("INSTRUCTOR_PIN", "0000")
    """),

    # Script de build de índices (stub)
    (BASE / "scripts" / "build_index.py"): textwrap.dedent("""\
        # CLI para ingestar materiales y construir índices (stub)
        # Uso: python apps/capacitaciones/scripts/build_index.py --curso CURSO --leccion LECCION
        if __name__ == "__main__":
            print("Stub: aquí irá la ingesta e indexación de materiales.")
    """),

    # Panel UI (stub mínimo para no romper nada)
    (ASSIST / "ui" / "panel.py"): textwrap.dedent("""\
        import streamlit as st
        from ..config import ENABLE_TRAINING_BOT

        def render_panel(curso_id: str | None = None, leccion_id: str | None = None):
            if not ENABLE_TRAINING_BOT:
                return
            with st.sidebar:
                st.header("Asistente de Capacitaciones")
                st.caption("Chatbot (Gemini + RAG local) — estructura creada.")
                st.write("Curso:", curso_id or "—")
                st.write("Lección:", leccion_id or "—")
                st.info("Este es un stub inicial. Próximo paso: conectar RAG y Gemini.")
    """),

    # .env ejemplo
    (BASE / ".env.example"): textwrap.dedent("""\
        # Activa/desactiva el chatbot (por defecto apagado para no interferir)
        ENABLE_TRAINING_BOT=false

        # Proveedor LLM
        LLM_PROVIDER=gemini
        GEMINI_API_KEY=coloca_tu_api_key_aqui

        # Privacidad
        PRIVACY_STRICT=true
        MAX_CONTEXT_CHARS=8000
        INSTRUCTOR_PIN=1234

        # Paths
        MATERIALS_DIR=apps/capacitaciones/materials
        INDICES_DIR=apps/capacitaciones/indices
        RAG_DB_PATH=apps/capacitaciones/capacitaciones.db
    """),

    # README breve
    (BASE / "README.md"): textwrap.dedent("""\
        # Chatbot de Capacitaciones (Gemini + RAG local)

        Estructura creada. Este módulo es independiente y opcional.
        - Activación por flag: `ENABLE_TRAINING_BOT=true` en `.env`.
        - No interfiere con otras apps; usa su propia DB e índices.

        ## Siguientes pasos
        1) Copia `.env.example` a `.env` y coloca tu `GEMINI_API_KEY`.
        2) (Opcional) Llama a `ui.panel.render_panel()` desde tu `app.py`.
        3) Agregar ingestión de materiales y construcción de índices (scripts/build_index.py).
    """),
}

GITKEEP_TARGETS = [d / ".gitkeep" for d in DIRS]

def mkdirs():
    for d in DIRS:
        d.mkdir(parents=True, exist_ok=True)

def touch_gitkeeps():
    for f in GITKEEP_TARGETS:
        if not f.exists():
            f.write_text("")

def write_files():
    for path, content in FILES_WITH_CONTENT.items():
        if path.exists():
            # No sobrescribir si ya existe
            continue
        path.write_text(content, encoding="utf-8")

def main():
    mkdirs()
    touch_gitkeeps()
    write_files()
    print("✅ Estructura creada en 'apps/capacitaciones' (sin sobrescribir archivos existentes).")
    print("   - Activa el bot poniendo ENABLE_TRAINING_BOT=true en apps/capacitaciones/.env")
    print("   - Integra el panel con: from apps.capacitaciones.assistant.ui.panel import render_panel")

if __name__ == "__main__":
    main()

