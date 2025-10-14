# Capacitación - Cuestionario (PLAIN)

Versión sin formato/tema personalizado (estilo por defecto de Streamlit). Mantiene toda la lógica:
- Nombre y correo obligatorios
- Tiempo por pregunta: 1 minuto
- Feedback inmediato (correcto/incorrecto)
- Rotación de preguntas y barajado de opciones
- 1 intento válido por usuario si ya aprobó (≥70); si <70 debe repetir
- Panel de administración con PIN

## Requisitos
- Python 3.9+
- `pip install -r requirements.txt`

## Ejecutar
```bash
streamlit run quiz_app.py
```
Variables (opcionales):
- `ADMIN_PIN="4321"`
- `NUM_QUESTIONS="10"`
- `QUIZ_DB_PATH="quiz_results.db"`