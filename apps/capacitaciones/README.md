# Chatbot de Capacitaciones (Gemini + RAG local)

Estructura creada. Este módulo es independiente y opcional.
- Activación por flag: `ENABLE_TRAINING_BOT=true` en `.env`.
- No interfiere con otras apps; usa su propia DB e índices.

## Siguientes pasos
1) Copia `.env.example` a `.env` y coloca tu `GEMINI_API_KEY`.
2) (Opcional) Llama a `ui.panel.render_panel()` desde tu `app.py`.
3) Agregar ingestión de materiales y construcción de índices (scripts/build_index.py).
