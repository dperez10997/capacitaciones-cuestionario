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
