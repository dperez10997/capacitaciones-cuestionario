
# quiz_app.py
# -*- coding: utf-8 -*-
"""
Cuestionario de Capacitación (PLAIN, FIX)
- Sin formato/tema personalizado.
- Nombre y correo OBLIGATORIOS.
- 1 minuto por pregunta (flujo una-a-una).
- Feedback inmediato (correcto/incorrecto).
- Rotación de preguntas y barajado de opciones.
- Intentos: Solo 1 intento válido por usuario si ya aprobó (≥70). Si <70, debe repetir hasta aprobar.
- Panel de administración con PIN.
Nota: Usamos st.rerun() (no experimental) para compatibilidad con Streamlit Cloud reciente.
"""
import os, json, time, sqlite3, random, re
from contextlib import closing
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cuestionario: Creación de Presupuestos", page_icon="📊", layout="centered")

# -----------------------------
# CONFIG
# -----------------------------
ADMIN_PIN = os.environ.get("ADMIN_PIN", "4321")
DB_PATH = os.environ.get("QUIZ_DB_PATH", "quiz_results.db")
NUM_QUESTIONS = int(os.environ.get("NUM_QUESTIONS", "10"))
SECONDS_PER_QUESTION = 60  # 1 minuto por pregunta

# -----------------------------
# BANCO DE PREGUNTAS
# -----------------------------
BANK: List[Dict[str, Any]] = [
    {"id":"q1","text":"¿Desde qué pestaña se gestionan todas las solicitudes relacionadas con presupuestos?","options":["Finanzas","Clientes","Trabajo","Reportes"],"answer":2},
    {"id":"q2","text":"¿Por qué es fundamental completar correctamente el encabezado del presupuesto?","options":["Para facilitar la búsqueda del presupuesto más adelante.","Porque la información se utilizará en el cuerpo de la factura.","Para que el cliente vea un formato más profesional.","Para cumplir con los requisitos del área de Tráfico."],"answer":1},
    {"id":"q3","text":"En la columna Unidades, ¿qué opción se debe seleccionar?","options":["Paquetes","Horas","Cantidad","Monto fijo"],"answer":2},
    {"id":"q4","text":"El Costo de cada ítem debe ingresarse como:","options":["Monto bruto con impuesto y comisión","Impuesto únicamente","Comisión únicamente","Monto neto (sin impuesto ni comisión)"],"answer":3},
    {"id":"q5","text":"Si la comisión se calcula automáticamente, ¿dónde y cómo se configura?","options":["En “Costo”, sumando 13%","En el título, escribiendo el porcentaje","No se puede calcular automáticamente","En el campo “MB”, indicando el % de utilidad; el sistema calcula el monto"],"answer":3},
    {"id":"q6","text":"Si la comisión va en línea aparte, ¿qué corresponde hacer?","options":["Agregar cualquier ítem y escribir “comisión”","Sumarla a los impuestos","Omitirla y avisar por correo","Seleccionar el ítem de comisión ligado a la venta principal y colocar el monto según el plan aprobado"],"answer":3},
    {"id":"q7","text":"¿Qué tipo de impuesto corresponde habitualmente?","options":["TE0 (0%)","TE1 (13%)","TE2 (Exento)","TE4 (reducido)"],"answer":1},
    {"id":"q8","text":"¿Cuándo se utiliza el tipo de impuesto TE4?","options":["Siempre en servicios digitales","Solo en casos específicos con clientes que tienen una tasa menor al 13%","Cuando hay comisión separada","Cuando hay descuentos"],"answer":1},
    {"id":"q9","text":"Para enviar el presupuesto al cliente en PDF, en “Imprimir para” se debe seleccionar:","options":["Borrador","Vista preliminar","Versión","Plantilla"],"answer":2},
    {"id":"q10","text":"Tras completar, revisar y guardar, ¿a qué estatus se debe cambiar el presupuesto?","options":["En proceso","Aprobado internamente","Pendiente de Aprobación","Facturado"],"answer":2},
]

# -----------------------------
# DB HELPERS
# -----------------------------
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

def has_passed(email: str) -> Tuple[bool, int, Optional[int]]:
    """Return (passed>=70, attempts_count, best_pct). Email is case-insensitive."""
    ensure_db()
    email = (email or "").strip().lower()
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute("""
            SELECT COUNT(*) as n, MAX(CAST(score AS FLOAT)/total*100.0) as best
            FROM results WHERE LOWER(COALESCE(email,'')) = ?
        """, (email,))
        row = cur.fetchone()
    n = int(row[0] or 0)
    best = int(round(row[1],0)) if row and row[1] is not None else None
    return ((best is not None and best >= 70), n, best)

def save_result(name: str, email: str, score: int, total: int, duration: float, answers_payload: Dict[str, Any]):
    ensure_db()
    with closing(sqlite3.connect(DB_PATH)) as conn, closing(conn.cursor()) as cur:
        cur.execute("""
            INSERT INTO results (submitted_at, name, email, score, total, duration_seconds, answers_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (datetime.utcnow().isoformat(timespec="seconds")+"Z", name or None, (email or "").lower(),
              score, total, duration, json.dumps(answers_payload, ensure_ascii=False)))
        conn.commit()

def load_all_results() -> pd.DataFrame:
    ensure_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        return pd.read_sql_query("SELECT * FROM results ORDER BY id DESC", conn)

# -----------------------------
# QUIZ FLOW HELPERS
# -----------------------------
def prepare_session_questions():
    """Selecciona preguntas y baraja opciones. Guarda estructura para auditoría."""
    if "display_questions" in st.session_state:
        return
    seed = int(time.time() * 1000) ^ os.getpid()
    random.seed(seed)
    k = min(NUM_QUESTIONS, len(BANK))
    sample_indices = random.sample(range(len(BANK)), k=k)
    display_questions, served_meta = [], []
    for idx in sample_indices:
        q = BANK[idx]
        qid = q.get("id", f"q{idx+1}")
        options = list(q["options"])
        perm = list(range(len(options))); random.shuffle(perm)
        shuffled = [options[j] for j in perm]
        correct_new = perm.index(q["answer"])
        display_questions.append({"qid": qid, "text": q["text"], "options": shuffled, "correct": correct_new})
        served_meta.append({"qid": qid, "perm": perm, "correct_new_index": correct_new})
    st.session_state.display_questions = display_questions
    st.session_state.served_meta = served_meta
    st.session_state.q_index = 0
    st.session_state.answers = {}
    st.session_state.correct_map = {}
    st.session_state.locked = False
    st.session_state.quiz_start = time.time()
    st.session_state.q_start = time.time()

def remaining_seconds() -> int:
    return max(0, SECONDS_PER_QUESTION - int(time.time() - st.session_state.q_start))

def next_question():
    st.session_state.q_index += 1
    st.session_state.locked = False
    st.session_state.q_start = time.time()

def finish_quiz(name: str, email: str):
    total = len(st.session_state.display_questions)
    score = sum(1 for i, ok in st.session_state.correct_map.items() if ok)
    duration = time.time() - st.session_state.quiz_start
    payload = {
        "version": 3,
        "answers": {str(k): v for k, v in st.session_state.answers.items()},
        "served": st.session_state.served_meta,
        "per_question_seconds": SECONDS_PER_QUESTION,
    }
    save_result(name, email, score, total, duration, payload)
    pct = int(round(score/total*100, 0))

    passed, attempts, best = has_passed(email)
    if pct >= 70:
        st.success(f"Aprobado con {pct}/100 ({score} de {total}).")
        st.info("Ya no podrás volver a realizar el cuestionario con este correo (1 intento válido por usuario).")
        for k in ["display_questions","served_meta","q_index","answers","correct_map","locked","quiz_start","q_start","participant"]:
            st.session_state.pop(k, None)
    else:
        st.error(f"Calificación {pct}/100 ({score} de {total}). Debes repetir la prueba hasta obtener ≥ 70.")
        if st.button("Reintentar ahora"):
            for k in ["display_questions","served_meta","q_index","answers","correct_map","locked","quiz_start","q_start"]:
                st.session_state.pop(k, None)
            prepare_session_questions()
            st.rerun()   # <---- FIX

    with st.expander("Detalle de respuestas"):
        for i, dq in enumerate(st.session_state.display_questions):
            chosen = st.session_state.answers.get(i, None)
            if chosen is None:
                st.write(f"{i+1}) {dq['text']} — No respondida ⏱️")
                continue
            ok = (chosen == dq["correct"])
            if ok:
                st.write(f"{i+1}) {dq['text']} — ✅ Correcto (Elegiste: {dq['options'][chosen]})")
            else:
                st.write(f"{i+1}) {dq['text']} — ❌ Incorrecto (Elegiste: {dq['options'][chosen]} | Correcta: {dq['options'][dq['correct']]})")

# -----------------------------
# UI
# -----------------------------
def is_valid_email(email: str) -> bool:
    if not email: return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

def start_form():
    st.subheader("Datos del participante (obligatorios)")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nombre", max_chars=80, placeholder="Ej. Ana Gómez")
    with col2:
        email = st.text_input("Correo", max_chars=120, placeholder="Ej. ana@empresa.com")
    start = st.button("Comenzar")
    if start:
        if not name or not email:
            st.error("Nombre y correo son obligatorios para iniciar.")
        elif not is_valid_email(email.strip()):
            st.error("Por favor ingresa un correo válido.")
        else:
            email_norm = email.strip().lower()
            passed, attempts, best = has_passed(email_norm)
            if passed:
                st.error(f"Este correo ya aprobó el cuestionario (mejor nota: {best}/100). Solo 1 intento válido por usuario.")
                st.info("Si necesitas que alguien más lo haga, usa un correo distinto.")
            else:
                if attempts > 0:
                    st.warning(f"Este correo tiene {attempts} intento(s) registrado(s). Debes repetir hasta alcanzar ≥ 70.")
                st.session_state.participant = {"name": name.strip(), "email": email_norm}
                prepare_session_questions()
                st.rerun()  # <---- FIX
    return st.session_state.get("participant")

def quiz_runtime(name: str, email: str):
    dq = st.session_state.display_questions[st.session_state.q_index]
    st.write(f"**Pregunta {st.session_state.q_index+1} de {len(st.session_state.display_questions)}**")
    st.write(f"**Tiempo restante:** {remaining_seconds()} s")
    st.write(dq["text"])

    disabled = st.session_state.locked
    choice = st.radio("Selecciona una opción", dq["options"], index=None, key=f"q_{st.session_state.q_index}", disabled=disabled)

    if choice is not None and not st.session_state.locked:
        chosen_idx = dq["options"].index(choice)
        st.session_state.answers[st.session_state.q_index] = chosen_idx
        ok = (chosen_idx == dq["correct"])
        st.session_state.correct_map[st.session_state.q_index] = ok
        st.session_state.locked = True

    if st.session_state.locked:
        chosen = st.session_state.answers.get(st.session_state.q_index, None)
        if chosen is not None:
            ok = (chosen == dq["correct"])
            if ok:
                st.success("✅ ¡Correcto!")
            else:
                st.error(f"❌ Incorrecto. Correcta: {dq['options'][dq['correct']]}")

    if remaining_seconds() == 0 and not st.session_state.locked:
        st.session_state.answers[st.session_state.q_index] = None
        st.session_state.correct_map[st.session_state.q_index] = False
        st.session_state.locked = True
        st.info("⏱️ Tiempo agotado para esta pregunta.")

    cols = st.columns(2)
    with cols[0]:
        if st.button("Siguiente ➜"):
            if st.session_state.q_index + 1 >= len(st.session_state.display_questions):
                finish_quiz(name, email)
            else:
                next_question()
                st.rerun()  # <---- FIX
    with cols[1]:
        if st.button("Salir"):
            for k in ["display_questions","served_meta","q_index","answers","correct_map","locked","quiz_start","q_start"]:
                st.session_state.pop(k, None)
            st.rerun()  # <---- FIX

# -----------------------------
# PÁGINAS
# -----------------------------
def quiz_page():
    st.title("Cuestionario")
    st.caption("Creación de Presupuestos - Evaluación de Conocimientos")
    participant = st.session_state.get("participant")
    if "display_questions" not in st.session_state:
        st.write("Completa tus datos para iniciar el cuestionario.")
        start_form()
        return
    quiz_runtime(participant["name"], participant["email"])

def admin_page():
    st.title("Panel de Administración")
    st.caption("Resultados en SQLite con rotación, límite de tiempo, y bloqueo tras aprobar (≥70).")
    pin = st.text_input("PIN de administrador", type="password")
    if st.button("Ingresar"):
        st.session_state.is_admin = (pin == ADMIN_PIN)
    if not st.session_state.get("is_admin"):
        st.stop()
    st.success("Acceso concedido.")
    df = load_all_results()
    if df.empty:
        st.warning("Aún no hay resultados.")
        return
    df["pct"] = (df["score"]/df["total"]*100).round(0).astype(int)
    agg = df.groupby(df["email"].str.lower()).agg(best_pct=("pct","max"), attempts=("id","count")).reset_index().rename(columns={"email":"email_norm"})
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Intentos", len(df)); c2.metric("Promedio", f"{df['pct'].mean():.0f}/100"); c3.metric("Aprobados (≥70)", f"{(df['pct']>=70).sum()}"); c4.metric("Usuarios únicos", agg.shape[0])
    with st.expander("Tabla de respuestas"):
        st.dataframe(df[["id","submitted_at","name","email","score","total","pct","duration_seconds","answers_json"]], use_container_width=True)
    with st.expander("Resumen por usuario (mejor nota / intentos)"):
        st.dataframe(agg, use_container_width=True)
    st.download_button("Descargar CSV (crudo)", df.to_csv(index=False).encode("utf-8"), file_name="resultados_quiz.csv", mime="text/csv")
    st.download_button("Descargar resumen por usuario", agg.to_csv(index=False).encode("utf-8"), file_name="resumen_usuarios.csv", mime="text/csv")

def main():
    st.sidebar.title("Navegación")
    mode = st.sidebar.radio("Elegí el modo", ["Cuestionario", "Administración"], index=0)
    if mode == "Cuestionario": quiz_page()
    else: admin_page()

if __name__ == "__main__":
    main()
