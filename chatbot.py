import streamlit as st
from groq import Groq

st.set_page_config(page_title= "Chat IA", page_icon= "©")
st.title("Chat IA-Talento Tech")
accion = st.text_input("¿Cuál es tu nombre?")
if st.button("Saludar"):
    st.write(f"Hola, {accion}, que bueno verte!")

MODELO =['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key = clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def configurar_pagina():
    st.title("Chatbot")
    st.sidebar.title("Configuración")
    elegir = st.sidebar.selectbox(
        "Elegir preferencias:",
        MODELO,
        index = 1
    )
    return elegir

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol,
    "content": contenido,
    "avatar": avatar}) #agrega datos a la lista
    

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border= True)
    with contenedorDelChat : mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()

    mensaje = st.chat_input("Escribi un mensaje...")
    if mensaje:
        actualizar_historial("user", mensaje, "🤺")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "💅")
                st.rerun()

if __name__ == "__main__":
    main() #funcion principal
