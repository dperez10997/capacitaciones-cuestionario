# Capacitación - Cuestionario (Rotación + Tiempo + Feedback + Intentos)

- **Nombre y correo obligatorios**.
- **1 minuto por pregunta** (flujo una-a-una).
- **Feedback inmediato** en cada selección (verde correcto, rojo incorrecto).
- **Rotación de preguntas** y **barajado de opciones**.
- **Intentos**: Solo 1 intento válido por usuario si ya aprobó (≥70). Quien obtenga <70 debe **repetir** hasta aprobar.
- **Panel de administración** con PIN, métricas, resumen por usuario y exportaciones CSV.

## Requisitos
- Python 3.9+
- `pip install -r requirements.txt`

## Ejecutar
```bash
streamlit run quiz_app.py
```
Variables (opcionales):
- `ADMIN_PIN="4321"`
- `NUM_QUESTIONS="10"`  # preguntas por intento
- `QUIZ_DB_PATH="quiz_results.db"`

## Publicar (Streamlit Community Cloud)
- Main file: `quiz_app.py`
- Secrets (opcional):
```
ADMIN_PIN="4321"
NUM_QUESTIONS="10"
```