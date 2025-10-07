# quiz_app.py
# -*- coding: utf-8 -*-
"""
Quiz de Capacitación - Creación de Presupuestos
MVP con página pública y panel de administración.
Stack: Streamlit + SQLite (almacenamiento local).

Cómo ejecutar:
1) pip install streamlit pandas
2) streamlit run quiz_app.py
"""

import os
import json
import time
import sqlite3
from contextlib import closing
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import streamlit as st

# -----------------------------
# CONFIGURACIÓN BÁSICA
# -----------------------------
st.set_page_config(page_title="Cuestionario: Creación de Presupuestos", page_icon="📝", layout="centered")

# Cambiar el PIN acá o mediante variable de entorno ADMIN_PIN
ADMIN_PIN = os.environ.get("ADMIN_PIN", "4321")
DB_PATH = os.environ.get("QUIZ_DB_PATH", "quiz_results.db")

BRAND = {
    "title": "Cuestionario: Creación de Presupuestos",
    "subtitle": "10 preguntas de selección única • Calificación automática",
}

# -----------------------------
# BANCO DE PREGUNTAS
# -----------------------------
# Fuente: Guion del usuario (resumen curado para opciones claras).
# Estructura: cada pregunta tiene 'text', 'options' y 'answer' (índice correcto)
QUESTIONS: List[Dict[str, Any]] = [
    {
        "text": "¿En qué pestaña se inicia la creación de un presupuesto?",
        "options": ["Finanzas", "Reportes", "Trabajo (naranja)", "Administración"],
        "answer": 2,
    },
    {
        "text": "Una vez que el presupuesto está aprobado, ¿qué se puede modificar sin tocar los ítems?",
        "options": [
            "Ítems y montos libremente",
            "Nada, queda bloqueado por completo",
            "Solo impuestos en los ítems",
            "Solo el encabezado, y se debe re-actualizar la aprobación",
        ],
        "answer": 3,
    },
    {
        "text": "En la columna Unidades, ¿qué opción se debe seleccionar?",
        "options": ["Paquetes", "Horas", "Cantidad", "Monto fijo"],
        "answer": 2,
    },
    {
        "text": "El Costo de cada ítem debe ingresarse como:",
        "options": ["Monto bruto con impuesto y comisión", "Impuesto únicamente", "Comisión únicamente", "Monto neto (sin impuesto ni comisión)"],
        "answer": 3,
    },
    {
        "text": "Si la comisión se calcula automáticamente, ¿dónde y cómo se configura?",
        "options": [
            "En “Costo”, sumando 13%",
            "En el título, escribiendo el porcentaje",
            "No se puede calcular automáticamente",
            "En el campo “MB”, indicando el % de utilidad; el sistema calcula el monto",
        ],
        "answer": 3,
    },
    {
        "text": "Si la comisión va en línea aparte, ¿qué corresponde hacer?",
        "options": [
            "Agregar cualquier ítem y escribir “comisión”",
            "Sumarla a los impuestos",
            "Omitirla y avisar por correo",
            "Seleccionar el ítem de comisión ligado a la venta principal y colocar el monto según el plan aprobado",
        ],
        "answer": 3,
    },
    {
        "text": "¿Qué tipo de impuesto corresponde habitualmente?",
        "options": ["TE0 (0%)", "TE1 (13%)", "TE2 (Exento)", "TE4 (reducido)"],
        "answer": 1,
    },
    {
        "text": "¿Cuándo se utiliza el tipo de impuesto TE4?",
        "options": [
            "Siempre en servicios digitales",
            "Solo en casos específicos con clientes que tienen una tasa menor al 13%",
            "Cuando hay comisión separada",
            "Cuando hay descuentos",
        ],
        "answer": 1,
    },
    {
        "text": "Para enviar el presupuesto al cliente en PDF, en “Imprimir para” se debe seleccionar:",
        "options": ["Borrador", "Vista preliminar", "Versión", "Plantilla"],
        "answer": 2,
    },
    {
        "text": "Tras completar, revisar y guardar, ¿a qué estatus se debe cambiar el presupuesto?",
        "options": ["En proceso", "Aprobado internamente", "Pendiente de Aprobación", "Facturado"],
        "answer": 2,
    },
]

TOTAL_QUESTIONS = len(QUESTIONS)

# -----------------------------
# ESTILOS
# -----------------------------
def inject_css():
    st.markdown(
        """
        <style>
        .app-header { text-align:center; margin-bottom: 1rem; }
        .app-title { font-weight: 800; font-size: 1.6rem; }
        .app-subtitle { color: #5a5f6a; margin-top: .25rem; }
        .question-card { border: 1px solid #e6e8ef; border-radius: 14px; padding: 1rem 1rem; margin-bottom: 1rem; }
        .footer-note { color:#6b7280; font-size:.85rem; margin-top:1rem; }
        .score-badge { font-weight:800; font-size:1.25rem; }
        .ok { color: #166534; } /* verde */
        .fail { color: #991b1b; } /* rojo */
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# DB HELPERS
# -----------------------------
def ensure_db():
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submitted_at TEXT NOT NULL,
                name TEXT,
                email TEXT,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                duration_seconds REAL NOT NULL,
                answers_json TEXT NOT NULL
            )
            """
        )
        conn.commit()

def save_result(name: str, email: str, score: int, total: int, duration: float, answers: Dict[int, int]):
    ensure_db()
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            """
            INSERT INTO results (submitted_at, name, email, score, total, duration_seconds, answers_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(timespec="seconds") + "Z",
                name or None, email or None,
                score, total, duration, json.dumps(answers, ensure_ascii=False),
            ),
        )
        conn.commit()

def load_all_results() -> pd.DataFrame:
    ensure_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        df = pd.read_sql_query("SELECT * FROM results ORDER BY id DESC", conn)
    return df

# -----------------------------
# LÓGICA DE NEGOCIO
# -----------------------------
def calculate_score(answers: Dict[int, int]) -> int:
    hits = 0
    for idx, q in enumerate(QUESTIONS):
        correct = q["answer"]
        chosen = answers.get(idx, None)
        if chosen is not None and chosen == correct:
            hits += 1
    return hits

# -----------------------------
# UI COMPONENTS
# -----------------------------
def render_header():
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    st.markdown(f'<div class="app-title">{BRAND["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="app-subtitle">{BRAND["subtitle"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def form_participant():
    st.write("Completa tus datos (opcional):")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nombre (opcional)", max_chars=80)
    with col2:
        email = st.text_input("Correo (opcional)", max_chars=120)
    return name.strip(), email.strip()

def quiz_page():
    inject_css()
    render_header()

    if "quiz_start" not in st.session_state:
        st.session_state.quiz_start = time.time()

    name, email = form_participant()
    st.divider()

    answers = {}
    for i, q in enumerate(QUESTIONS):
        with st.container():
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f"**{i+1}) {q['text']}**")
            choice = st.radio(
                "Selecciona una opción",
                q["options"],
                index=None,
                key=f"q_{i}",
                label_visibility="collapsed",
            )
            if choice is not None:
                answers[i] = q["options"].index(choice)
            st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.button("Enviar respuestas", type="primary", use_container_width=True)

    if submitted:
        duration = time.time() - st.session_state.quiz_start
        score = calculate_score(answers)
        save_result(name, email, score, TOTAL_QUESTIONS, duration, answers)

        pct = int(round((score / TOTAL_QUESTIONS) * 100, 0))
        status = "Aprobado ✅" if pct >= 80 else "Reprobado ❌"

        st.success(f"Tu calificación es **{pct}/100** ({score} de {TOTAL_QUESTIONS}). {status}")
        st.caption(f"Tiempo empleado: {int(duration)} segundos")
        st.session_state["last_score"] = pct

        with st.expander("Ver qué respondí (solo tú lo ves ahora)"):
            for i, q in enumerate(QUESTIONS):
                chosen = answers.get(i, None)
                correct_idx = q["answer"]
                if chosen is None:
                    st.write(f"{i+1}) Sin respuesta.")
                    continue
                ok = (chosen == correct_idx)
                css = "ok" if ok else "fail"
                st.markdown(
                    f"""<div>
                    <strong>{i+1})</strong> {q['text']}<br>
                    Elegiste: <span class="{css}">{q['options'][chosen]}</span><br>
                    Correcta: <span class="ok">{q['options'][correct_idx]}</span>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.info("¡Gracias por participar! Podés cerrar la página.")

def admin_page():
    inject_css()
    st.title("Panel de Administración")
    st.caption("Resultados almacenados localmente en SQLite.")

    pin = st.text_input("PIN de administrador", type="password")
    if st.button("Ingresar", type="primary"):
        st.session_state.is_admin = (pin == ADMIN_PIN)

    if not st.session_state.get("is_admin"):
        st.stop()

    st.success("Acceso concedido.")
    df = load_all_results()

    if df.empty:
        st.warning("Aún no hay resultados.")
        return

    # Métricas rápidas
    df["pct"] = (df["score"] / df["total"] * 100).round(0).astype(int)
    aprobados = (df["pct"] >= 80).sum()
    st.subheader("Métricas")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Intentos", len(df))
    m2.metric("Promedio", f"{df['pct'].mean():.0f}/100")
    m3.metric("Mediana", f"{df['pct'].median():.0f}/100")
    m4.metric("Aprobados", f"{aprobados}")

    # Tabla
    with st.expander("Ver tabla de respuestas"):
        show_cols = ["id", "submitted_at", "name", "email", "score", "total", "pct", "duration_seconds", "answers_json"]
        st.dataframe(df[show_cols], use_container_width=True)

    # Descarga CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar CSV", csv, file_name="resultados_quiz.csv", mime="text/csv")

    # Análisis por pregunta (tasa de acierto)
    st.subheader("Tasa de acierto por pregunta")
    per_q = []
    for idx, q in enumerate(QUESTIONS):
        correct_idx = q["answer"]
        # contar correctas
        correct_count = 0
        total_count = 0
        for _, row in df.iterrows():
            try:
                ans = json.loads(row["answers_json"])
                chosen = ans.get(str(idx))
                if chosen is None:
                    chosen = ans.get(int(idx))  # por si guardó como int
                if chosen is not None:
                    total_count += 1
                    if int(chosen) == int(correct_idx):
                        correct_count += 1
            except Exception:
                pass
        rate = (correct_count / total_count * 100) if total_count else 0
        per_q.append({"#": idx + 1, "Pregunta": q["text"], "Acierto %": round(rate, 0)})

    st.dataframe(pd.DataFrame(per_q), use_container_width=True)

    st.caption("Sugerencia: respaldar el archivo 'quiz_results.db' si desea conservar los resultados.")

# -----------------------------
# RUTEO
# -----------------------------
def main():
    # Sidebar: modo
    st.sidebar.title("Navegación")
    mode = st.sidebar.radio("Elegí el modo", ["Cuestionario", "Administración"], index=0)

    if mode == "Cuestionario":
        quiz_page()
    else:
        admin_page()

if __name__ == "__main__":
    main()
