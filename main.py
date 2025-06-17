import streamlit as st
import groq  #API

# MODELOS DE IA
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# CONFIGURAR PÁGINA
def configurar_pagina():
    st.set_page_config(page_title="Mi Primer ChatBot con Python")
    st.title('Bienvenidos a mi ChatBot')

# CREAR CLIENTE DE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets['GROQ_API_KEY']
    return groq.Groq(api_key=groq_api_key)

# BARRA LATERAL
def mostrar_sidebar():
    st.sidebar.title('Elegí el modelo de IA favorito')
    modelo = st.sidebar.selectbox('Elegí tu modelo', MODELOS, index=0)
    st.write(f'**Elegiste el modelo:** {modelo}')
    return modelo

# INICIALIZAR ESTADO DEL CHAT
def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# MOSTRAR MENSAJES PREVIOS
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje['role']):
            st.markdown(mensaje['content'])

# OBTENER MENSAJE USUARIO
def obtener_mensajes_usuario():
    return st.chat_input("Enviá tu mensaje")

# AGREGAR MENSAJE
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

# MOSTRAR MENSAJE
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# OBTENER RESPUESTA DEL MODELO
def obtener_respuestas_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

# FUNCIÓN PRINCIPAL
def ejecutar_chat():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()
    inicializar_estado_chat()
    obtener_mensajes_previos()

    mensaje_usuario = obtener_mensajes_usuario()
    if mensaje_usuario:
        agregar_mensajes_previos("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta_contenido = obtener_respuestas_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensajes_previos("assistant", respuesta_contenido)
        mostrar_mensaje("assistant", respuesta_contenido)

# EJECUTAR APP
if __name__ == '__main__':
    ejecutar_chat()
