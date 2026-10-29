
import streamlit as st
from datetime import date
import uuid

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Organizador de tareas ♡",
    page_icon="🎀",
    layout="wide"
)

# ==========================================
# COLORES
# ==========================================

FONDO = "#FFFAFC"
ROSA_CLARO = "#F5DCE7"
ROSA_TARJETAS = "#F9E8EF"
ROSA = "#D99AB5"
TEXTO = "#85405E"
TEXTO_SECUNDARIO = "#A8798E"

# ==========================================
# LISTAS DE OPCIONES
# ==========================================

ASIGNATURAS = [
    "Matemáticas",
    "Física",
    "Tecnología",
    "Castellano",
    "Catalán",
    "Inglés",
    "Geología",
    "Filosofía",
    "Historia"
]

TIPOS = [
    "Resumen",
    "Estudiar",
    "Esquema",
    "Trabajo",
    "Entregar"
]

PRIORIDADES = [
    "Alta",
    "Media",
    "Baja"
]

ORDEN_PRIORIDAD = {
    "Alta": 1,
    "Media": 2,
    "Baja": 3
}

# ==========================================
# INICIALIZAR DATOS
# ==========================================

if "tareas" not in st.session_state:
    st.session_state.tareas = []

if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def cambiar_pagina(nombre):
    st.session_state.pagina = nombre


def obtener_pendientes():
    return [
        t for t in st.session_state.tareas
        if not t["completada"]
    ]


def obtener_tareas_inicio():

    hoy = date.today()

    return [
        t for t in obtener_pendientes()
        if t["fecha"] >= hoy
    ]


def ordenar_tareas(tareas, criterio):

    if criterio == "Fecha (más próxima primero)":

        return sorted(
            tareas,
            key=lambda t: (
                t["fecha"],
                ORDEN_PRIORIDAD[t["prioridad"]]
            )
        )

    else:

        return sorted(
            tareas,
            key=lambda t: (
                ORDEN_PRIORIDAD[t["prioridad"]],
                t["fecha"]
            )
        )


def estilo_prioridad(prioridad):

    if prioridad == "Alta":
        return "🔴"

    elif prioridad == "Media":
        return "🟠"

    else:
        return "🟢"


# ==========================================
# MOSTRAR UNA TAREA
# ==========================================

def mostrar_tarea(tarea):

    with st.container(border=True):

        col1, col2 = st.columns([5, 1])

        with col1:

            st.markdown(f"**♡ {tarea['nombre']}**")

            st.caption(
                f"{tarea['asignatura']}  ·  "
                f"{tarea['tipo']}  ·  "
                f"{tarea['fecha'].strftime('%d/%m/%Y')}"
            )

            st.write(
                f"{estilo_prioridad(tarea['prioridad'])} "
                f"Prioridad: {tarea['prioridad']}"
            )

        with col2:

            if tarea["completada"]:
                st.write("✓")


# ==========================================
# COLUMNA IZQUIERDA: MENÚ
# ==========================================

def menu_lateral():

    st.markdown("## ୨୧ My Planner")

    st.caption("for Alice ♡")

    st.markdown("---")

    st.subheader("♡ Navegación")

    opciones = {
        "⌂ Inicio": "Inicio",
        "＋ Añadir tareas": "Añadir tareas",
        "✎ Modificar tareas": "Modificar tareas",
        "✿ Asignaturas": "Asignaturas"
    }

    for texto, pagina in opciones.items():

        if st.button(
            texto,
            key=f"menu_{pagina}",
            use_container_width=True
        ):

            cambiar_pagina(pagina)
            st.rerun()

    st.markdown("---")

    st.caption("♡ Little steps every day!")


# ==========================================
# PÁGINA DE INICIO
# ==========================================

def inicio():

    st.title("Hello, lovely! ♡")

    st.write(
        "Tu espacio para organizarte después de los exámenes."
    )

    st.markdown("---")

    st.subheader("♡ Tareas pendientes")

    tareas = obtener_tareas_inicio()

    # CONTADOR DE TAREAS POR ASIGNATURA

    st.markdown("##### Resumen por asignaturas")

    columnas = st.columns(3)

    for i, asignatura in enumerate(ASIGNATURAS):

        cantidad = sum(
            1 for t in tareas
            if t["asignatura"] == asignatura
        )

        with columnas[i % 3]:

            st.caption(
                f"♡ {asignatura}: **{cantidad}**"
            )

    st.markdown("---")

    # ORDENAR TAREAS

    criterio = st.selectbox(
        "Organizar tareas por:",
        [
            "Fecha (más próxima primero)",
            "Prioridad (alta primero)"
        ]
    )

    tareas_ordenadas = ordenar_tareas(
        tareas,
        criterio
    )

    # MOSTRAR TAREAS

    if tareas_ordenadas:

        for tarea in tareas_ordenadas:
            mostrar_tarea(tarea)

    else:

        st.info(
            "No tienes tareas pendientes por realizar. ♡"
        )


# ==========================================
# PÁGINA: AÑADIR TAREAS
# ==========================================

def añadir_tareas():

    st.title("＋ Añadir tareas")

    st.write(
        "Organiza tus próximas actividades. ♡"
    )

    st.markdown("---")

    with st.container(border=True):

        with st.form("formulario_nueva_tarea"):

            nombre = st.text_input(
                "Nombre de la tarea",
                placeholder="Ej. Ejercicios de matemáticas"
            )

            asignatura = st.selectbox(
                "Asignatura",
                ASIGNATURAS
            )

            fecha = st.date_input(
                "Fecha de entrega",
                value=date.today()
            )

            prioridad = st.selectbox(
                "Prioridad",
                PRIORIDADES
            )

            tipo = st.selectbox(
                "Tipo de tarea",
                TIPOS
            )

            guardar = st.form_submit_button(
                "Guardar tarea ♡",
                use_container_width=True
            )

            if guardar:

                if nombre.strip():

                    nueva_tarea = {
                        "id": str(uuid.uuid4()),
                        "nombre": nombre.strip(),
                        "asignatura": asignatura,
                        "fecha": fecha,
                        "prioridad": prioridad,
                        "tipo": tipo,
                        "completada": False
                    }

                    st.session_state.tareas.append(
                        nueva_tarea
                    )

                    st.success(
                        "¡Tarea añadida correctamente! ♡"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Debes escribir un nombre para la tarea."
                    )


# ==========================================
# PÁGINA: MODIFICAR TAREAS
# ==========================================

def modificar_tareas():

    st.title("✎ Modificar tareas")

    st.write(
        "Edita, completa o elimina tus tareas. ♡"
    )

    if not st.session_state.tareas:

        st.info("Todavía no tienes tareas guardadas.")

        return

    st.markdown("---")

    # SELECCIONAR TAREA

    tareas = st.session_state.tareas

    seleccion = st.selectbox(
        "Selecciona una tarea:",
        options=range(len(tareas)),
        format_func=lambda i: (
            f"{tareas[i]['nombre']} "
            f"({tareas[i]['asignatura']})"
        )
    )

    tarea = st.session_state.tareas[seleccion]

    st.markdown("---")

    with st.container(border=True):

        with st.form("formulario_modificar"):

            nuevo_nombre = st.text_input(
                "Nombre",
                value=tarea["nombre"]
            )

            nueva_asignatura = st.selectbox(
                "Asignatura",
                ASIGNATURAS,
                index=ASIGNATURAS.index(
                    tarea["asignatura"]
                )
            )

            nueva_fecha = st.date_input(
                "Fecha de entrega",
                value=tarea["fecha"]
            )

            nueva_prioridad = st.selectbox(
                "Prioridad",
                PRIORIDADES,
                index=PRIORIDADES.index(
                    tarea["prioridad"]
                )
            )

            nuevo_tipo = st.selectbox(
                "Tipo de tarea",
                TIPOS,
                index=TIPOS.index(
                    tarea["tipo"]
                )
            )

            completada = st.checkbox(
                "Marcar como completada",
                value=tarea["completada"]
            )

            guardar_cambios = st.form_submit_button(
                "Guardar cambios ♡",
                use_container_width=True
            )

            if guardar_cambios:

                if nuevo_nombre.strip():

                    tarea["nombre"] = nuevo_nombre.strip()
                    tarea["asignatura"] = nueva_asignatura
                    tarea["fecha"] = nueva_fecha
                    tarea["prioridad"] = nueva_prioridad
                    tarea["tipo"] = nuevo_tipo
                    tarea["completada"] = completada

                    st.success(
                        "¡Cambios guardados correctamente!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "El nombre de la tarea no puede estar vacío."
                    )

        # ELIMINAR TAREA

        if st.button(
            "Eliminar tarea",
            key=f"eliminar_{tarea['id']}",
            use_container_width=True
        ):

            st.session_state.tareas.pop(seleccion)

            st.success("Tarea eliminada.")

            st.rerun()


# ==========================================
# PÁGINA: ASIGNATURAS
# ==========================================

def asignaturas():

    st.title("✿ Mis asignaturas")

    st.write(
        "Todas tus tareas organizadas por materias. ♡"
    )

    st.markdown("---")

    for asignatura in ASIGNATURAS:

        tareas_materia = [
            t for t in st.session_state.tareas
            if t["asignatura"] == asignatura
        ]

        pendientes = [
            t for t in tareas_materia
            if not t["completada"]
        ]

        completadas = [
            t for t in tareas_materia
            if t["completada"]
        ]

        with st.expander(
            f"♡ {asignatura}  ·  "
            f"{len(pendientes)} pendientes"
        ):

            if tareas_materia:

                for tarea in ordenar_tareas(
                    tareas_materia,
                    "Fecha (más próxima primero)"
                ):

                    estado = (
                        "✓ Completada"
                        if tarea["completada"]
                        else "○ Pendiente"
                    )

                    st.markdown(
                        f"**{tarea['nombre']}**"
                    )

                    st.caption(
                        f"{tarea['tipo']} · "
                        f"{tarea['fecha'].strftime('%d/%m/%Y')} · "
                        f"{tarea['prioridad']} · "
                        f"{estado}"
                    )

            else:

                st.caption(
                    "Todavía no hay tareas en esta asignatura."
                )


# ==========================================
# FUNCIÓN PRINCIPAL
# ==========================================

def main():

    # DIVISIÓN DE LA PANTALLA: 1/3 Y 2/3

    izquierda, derecha = st.columns([1, 2])

    # COLUMNA IZQUIERDA

    with izquierda:

        with st.container(border=True):

            menu_lateral()

    # COLUMNA DERECHA

    with derecha:

        with st.container(border=True):

            pagina = st.session_state.pagina

            if pagina == "Inicio":

                inicio()

            elif pagina == "Añadir tareas":

                añadir_tareas()

            elif pagina == "Modificar tareas":

                modificar_tareas()

            elif pagina == "Asignaturas":

                asignaturas()


# ==========================================
# EJECUTAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    main()
