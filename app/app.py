import streamlit as st
import requests

# Configuración inicial de la aplicación
st.title("JARVIS - Asistente de Videojuegos 🎮")
st.write("Completa los campos a continuación para recibir ayuda personalizada sobre videojuegos.")

# Datos contextuales
st.header("Información del Contexto del Problema")
videogame = st.text_input("Videojuego", placeholder="Ejemplo: League of Legends")
issue = st.text_area("Describe tu problema", placeholder="Ejemplo: No puedo mejorar mi rendimiento.")
platform = st.selectbox("Plataforma", ["PC", "Consola", "Móvil o Tablet"])
controls = st.selectbox("Controles", ["Teclado y Ratón", "Mando", "Pantalla Táctil"])
sound = st.radio("¿Usas sonido?", ["Sí", "No"])

# Datos del usuario
st.header("Información del Usuario")
sex = st.selectbox("Sexo", ["M", "F", "Otro"])
age = st.number_input("Edad", min_value=13, max_value=100, step=1)
country = st.text_input("País", placeholder="Ejemplo: España")
language = st.text_input("Idioma", placeholder="Ejemplo: Español")

# Función para verificar que el backend esté en línea
def is_backend_alive(url="http://127.0.0.1:8000"):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Botón para enviar datos
if st.button("Enviar"):
    # Validar que los campos requeridos estén llenos
    if not videogame or not issue or not country or not language:
        st.error("Por favor, completa todos los campos obligatorios.")
    else:
        # Construir la solicitud
        data = {
            "context": {
                "videogame": videogame,
                "issue": issue,
                "platform": platform,
                "controls": controls,
                "sound": sound == "Sí"
            },
            "user": {
                "sex": sex,
                "age": age,
                "country": country,
                "language": language
            }
        }

        if not is_backend_alive():
            st.error("El backend no está disponible. Asegúrate de que el servidor esté en ejecución.")
        else:
            try:
                response = requests.post("http://127.0.0.1:8000/query", json=data)
                response.raise_for_status()
                # Intentar decodificar la respuesta como JSON
                st.success("Respuesta de JARVIS:")
                st.write(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error en la solicitud: {e}")
                st.write(f"Contenido de la respuesta: {response.text}")
            except ValueError as json_err:
                st.error(f"Error al decodificar JSON: {json_err}")
                st.write(f"Contenido de la respuesta: {response.text}")

# Opciones de depuración
if st.checkbox("Mostrar datos enviados"):
    st.json(data)
