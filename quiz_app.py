
# quiz_app.py
# -*- coding: utf-8 -*-
"""
Quiz de Capacitación - Creación de Presupuestos
MVP con página pública y panel de administración.
Estilo con cabecera morada en gradiente y tarjetas blancas.

Cómo ejecutar:
1) pip install -r requirements.txt
2) streamlit run quiz_app.py
"""
import os, json, time, sqlite3
from contextlib import closing
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cuestionario: Creación de Presupuestos", page_icon="📊", layout="centered")

ADMIN_PIN = os.environ.get("ADMIN_PIN", "4321")
DB_PATH = os.environ.get("QUIZ_DB_PATH", "quiz_results.db")

BRAND = {
    "title": "Cuestionario",
    "subtitle": "Creación de Presupuestos - Evaluación de Conocimientos",
    "emoji": "📊",
    "accent": "#7c3aed",
}

QUESTIONS: List[Dict[str, Any]] = [
    {"text": "¿Desde qué pestaña se gestionan todas las solicitudes relacionadas con presupuestos?",
     "options": ["Finanzas", "Clientes", "Trabajo", "Reportes"], "answer": 2},
    {"text": "¿Por qué es fundamental completar correctamente el encabezado del presupuesto?",
     "options": ["Para facilitar la búsqueda del presupuesto más adelante.",
                 "Porque la información se utilizará en el cuerpo de la factura.",
                 "Para que el cliente vea un formato más profesional.",
                 "Para cumplir con los requisitos del área de Tráfico."],
     "answer": 1},
    {"text": "En la columna Unidades, ¿qué opción se debe seleccionar?",
     "options": ["Paquetes", "Horas", "Cantidad", "Monto fijo"], "answer": 2},
    {"text": "El Costo de cada ítem debe ingresarse como:",
     "options": ["Monto bruto con impuesto y comisión", "Impuesto únicamente", "Comisión únicamente", "Monto neto (sin impuesto ni comisión)"], "answer": 3},
    {"text": "Si la comisión se calcula automáticamente, ¿dónde y cómo se configura?",
     "options": ["En “Costo”, sumando 13%",
                 "En el título, escribiendo el porcentaje",
                 "No se puede calcular automáticamente",
                 "En el campo “MB”, indicando el % de utilidad; el sistema calcula el monto"], "answer": 3},
    {"text": "Si la comisión va en línea aparte, ¿qué corresponde hacer?",
     "options": ["Agregar cualquier ítem y escribir “comisión”",
                 "Sumarla a los impuestos",
                 "Omitirla y avisar por correo",
                 "Seleccionar el ítem de comisión ligado a la venta principal y colocar el monto según el plan aprobado"], "answer": 3},
    {"text": "¿Qué tipo de impuesto corresponde habitualmente?",
     "options": ["TE0 (0%)", "TE1 (13%)", "TE2 (Exento)", "TE4 (reducido)"], "answer": 1},
    {"text": "¿Cuándo se utiliza el tipo de impuesto TE4?",
     "options": ["Siempre en servicios digitales",
                 "Solo en casos específicos con clientes que tienen una tasa menor al 13%",
                 "Cuando hay comisión separada",
                 "Cuando hay descuentos"], "answer": 1},
    {"text": "Para enviar el presupuesto al cliente en PDF, en “Imprimir para” se debe seleccionar:",
     "options": ["Borrador", "Vista preliminar", "Versión", "Plantilla"], "answer": 2},
    {"text": "Tras completar, revisar y guardar, ¿a qué estatus se debe cambiar el presupuesto?",
     "options": ["En proceso", "Aprobado internamente", "Pendiente de Aprobación", "Facturado"], "answer": 2},
]
TOTAL_QUESTIONS = len(QUESTIONS)

def inject_css():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, #8b5cf6 0%, #7c3aed 22%, #eef2ff 22%, #f8fafc 100%);
    }}
    .main .block-container {{
        max-width: 920px;
        padding-top: 0 !important;
    }}
    .hero {{
        background: linear-gradient(135deg, #6d28d9, #8b5cf6);
        color: white;
        padding: 28px 32px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(107, 33, 168, .25);
        text-align: center;
        margin: 28px 0 18px 0;
    }}
    .hero .title {{
        font-weight: 800;
        font-size: 2.1rem;
        margin: 0;
        letter-spacing: 0.2px;
    }}
    .hero .subtitle {{ opacity: .95; margin-top: 6px; }}
    .paper {{
        background: #ffffff;
        border: 1px solid #e6e8ef;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(16,24,40,.06);
        padding: 16px 18px;
    }}
    .question-card {{
        border: 1px solid #e6e8ef; border-radius: 14px; padding: 1rem 1rem; margin-bottom: 1rem; background: #fff;
    }}
    .question-title {{ font-weight: 700; margin-bottom: .5rem; }}
    .stRadio > div[role="radiogroup"] {{ gap: .75rem; }}
    .stRadio > div[role="radiogroup"] > label {{
        background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px 14px; display:block; box-shadow: 0 1px 0 rgba(16,24,40,.02);
    }}
    .stRadio > div[role="radiogroup"] > label:hover {{
        border-color: {BRAND["accent"]}; box-shadow: 0 0 0 4px rgba(124,58,237,.15);
    }}
    .stRadio > div[role="radiogroup"] > label p {{ margin: 0; }}
    .stButton>button {{
        background: linear-gradient(135deg, #7c3aed, #6d28d9);
        color:white; border: 0; padding: 12px 16px; border-radius: 12px; font-weight: 700; width: 100%;
        box-shadow: 0 6px 18px rgba(124, 58, 237, .35);
    }}
    .stButton>button:hover {{ transform: translateY(-1px); box-shadow: 0 10px 20px rgba(124,58,237,.4); }}
    .footer-note {{ color:#6b7280; font-size:.85rem; margin-top:1rem; }}
    .ok {{ color: #166534; }} .fail {{ color: #991b1b; }}
    </style>
    """, unsafe_allow_html=True)

def ensure_db():
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submitted_at TEXT NOT NULL,
                name TEXT, email TEXT,
                score INTEGER NOT NULL, total INTEGER NOT NULL,
                duration_seconds REAL NOT NULL,
                answers_json TEXT NOT NULL
            )
        """)
        conn.commit()

def save_result(name: str, email: str, score: int, total: int, duration: float, answers: Dict[int, int]):
    ensure_db()
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute("""
            INSERT INTO results (submitted_at, name, email, score, total, duration_seconds, answers_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (datetime.utcnow().isoformat(timespec="seconds")+"Z", name or None, email or None,
              score, total, duration, json.dumps(answers, ensure_ascii=False)))
        conn.commit()

def load_all_results() -> pd.DataFrame:
    ensure_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        return pd.read_sql_query("SELECT * FROM results ORDER BY id DESC", conn)

def calculate_score(answers: Dict[int, int]) -> int:
    hits = 0
    for idx, q in enumerate(QUESTIONS):
        if answers.get(idx) == q["answer"]:
            hits += 1
    return hits

def render_hero():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown(f'<div class="title">{BRAND["emoji"]} {BRAND["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{BRAND["subtitle"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def form_participant():
    with st.container():
        st.markdown('<div class="paper">', unsafe_allow_html=True)
        st.subheader("Datos del participante (opcional)")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nombre", max_chars=80, placeholder="Ej. Ana Gómez")
        with col2:
            email = st.text_input("Correo", max_chars=120, placeholder="Ej. ana@empresa.com")
        st.markdown('</div>', unsafe_allow_html=True)
    return name.strip(), email.strip()

def quiz_page():
    inject_css()
    render_hero()

    if "quiz_start" not in st.session_state:
        st.session_state.quiz_start = time.time()

    name, email = form_participant()

    answers = {}
    with st.container():
        st.markdown('<div class="paper">', unsafe_allow_html=True)
        for i, q in enumerate(QUESTIONS):
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question-title">{i+1}. {q["text"]}</div>', unsafe_allow_html=True)
            choice = st.radio("Selecciona una opción", q["options"], index=None, key=f"q_{i}", label_visibility="collapsed")
            if choice is not None:
                answers[i] = q["options"].index(choice)
            st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.button("Enviar respuestas", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        duration = time.time() - st.session_state.quiz_start
        score = calculate_score(answers)
        pct = int(round((score / TOTAL_QUESTIONS) * 100, 0))
        status = "Aprobado ✅" if pct >= 80 else "Reprobado ❌"
        save_result(name, email, score, TOTAL_QUESTIONS, duration, answers)

        with st.container():
            st.markdown('<div class="paper">', unsafe_allow_html=True)
            st.success(f"Tu calificación es **{pct}/100** ({score} de {TOTAL_QUESTIONS}). {status}")
            st.caption(f"Tiempo empleado: {int(duration)} segundos")
            with st.expander("Ver qué respondí (solo tú lo ves ahora)"):
                for i, q in enumerate(QUESTIONS):
                    chosen = answers.get(i)
                    correct_idx = q["answer"]
                    if chosen is None:
                        st.write(f"{i+1}) Sin respuesta.")
                        continue
                    ok = (chosen == correct_idx)
                    css = "ok" if ok else "fail"
                    st.markdown(f"<div><strong>{i+1})</strong> {q['text']}<br>Elegiste: <span class='{css}'>{q['options'][chosen]}</span><br>Correcta: <span class='ok'>{q['options'][correct_idx]}</span></div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

def admin_page():
    inject_css()
    render_hero()
    with st.container():
        st.markdown('<div class="paper">', unsafe_allow_html=True)
        st.subheader("Panel de Administración")
        st.caption("Resultados almacenados localmente en SQLite.")
        pin = st.text_input("PIN de administrador", type="password")
        if st.button("Ingresar", type="primary"):
            st.session_state.is_admin = (pin == ADMIN_PIN)
        if not st.session_state.get("is_admin"):
            st.markdown('</div>', unsafe_allow_html=True); st.stop()
        st.success("Acceso concedido.")
        df = load_all_results()
        if df.empty:
            st.warning("Aún no hay resultados."); st.markdown('</div>', unsafe_allow_html=True); return
        df["pct"] = (df["score"] / df["total"] * 100).round(0).astype(int)
        aprobados = (df["pct"] >= 80).sum()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Intentos", len(df)); m2.metric("Promedio", f"{df['pct'].mean():.0f}/100"); m3.metric("Mediana", f"{df['pct'].median():.0f}/100"); m4.metric("Aprobados", f"{aprobados}")
        with st.expander("Ver tabla de respuestas"):
            show_cols = ["id","submitted_at","name","email","score","total","pct","duration_seconds","answers_json"]
            st.dataframe(df[show_cols], use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar CSV", csv, file_name="resultados_quiz.csv", mime="text/csv")
        st.subheader("Tasa de acierto por pregunta")
        per_q = []
        for idx, q in enumerate(QUESTIONS):
            correct_idx = q["answer"]; correct_count = 0; total_count = 0
            for _, row in df.iterrows():
                try:
                    ans = json.loads(row["answers_json"]); chosen = ans.get(str(idx), ans.get(idx))
                    if chosen is not None:
                        total_count += 1; 
                        if int(chosen) == int(correct_idx): correct_count += 1
                except Exception: pass
            rate = (correct_count / total_count * 100) if total_count else 0
            per_q.append({"#": idx+1, "Pregunta": q["text"], "Acierto %": round(rate, 0)})
        st.dataframe(pd.DataFrame(per_q), use_container_width=True)
        st.caption("Sugerencia: respalde el archivo 'quiz_results.db' si desea conservar los resultados.")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.sidebar.title("Navegación")
    mode = st.sidebar.radio("Elegí el modo", ["Cuestionario", "Administración"], index=0)
    if mode == "Cuestionario": quiz_page()
    else: admin_page()

if __name__ == "__main__":
    main()
