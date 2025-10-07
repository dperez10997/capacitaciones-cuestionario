# Capacitación - Cuestionario (Streamlit + SQLite)

App de cuestionario con **página pública** y **panel de administración** (PIN) para tu capacitación de *Creación de Presupuestos*.

## 📦 Requisitos
- Python 3.9+
- `pip install -r requirements.txt`

## ▶️ Ejecutar local
```bash
streamlit run quiz_app.py
```
- PIN admin por defecto: `4321` (cámbialo con la variable de entorno `ADMIN_PIN` o editando el archivo).
- La base de datos se guarda como `quiz_results.db` en la carpeta del proyecto (puedes moverla con `QUIZ_DB_PATH`).

## ☁️ Publicar en Streamlit Community Cloud
1. Sube este repo a GitHub.
2. En *Deploy an app*, elige tu repo y `quiz_app.py` como *Main file*.
3. (Opcional) En **Advanced settings → Secrets** agrega:
```
ADMIN_PIN="4321"
```
4. ¡Listo! Te dará una URL pública `https://<tu-app>.streamlit.app`.

## 🧾 Funcionalidades
- 10 preguntas de selección única.
- Calificación automática y estado Aprobado (≥80) / Reprobado.
- Guarda nombre/correo (opcionales), tiempo y respuestas.
- Panel admin con métricas, tabla y **Descargar CSV**.
- Tasa de acierto por pregunta.

## 🗄️ Respaldo
Copia el archivo `quiz_results.db` para conservar resultados antes de actualizar o reinstalar.