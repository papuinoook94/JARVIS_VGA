# JARVIS - Asistente de Videojuegos 🎮

JARVIS es un asistente personalizado para jugadores de videojuegos. Utiliza FastAPI como backend y Streamlit como frontend para ofrecer ayuda personalizada a los usuarios, combinando tecnología avanzada de OpenAI para generar respuestas útiles y relevantes.

## Características

- **Backend**: Proporcionado por FastAPI, maneja las consultas y se conecta con OpenAI GPT.
- **Frontend**: Interfaz de usuario amigable con Streamlit para que los jugadores describan sus problemas y reciban asistencia.
- **Persistencia**: Almacena interacciones en una base de datos SQLite para análisis futuro.

## Requisitos Previos

- Docker instalado en tu sistema.
- Una clave válida de OpenAI API.

## Instalación y Configuración

### Paso 1: Clonar el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/jarvis-app.git
cd jarvis-app
docker build -t jarvis-app .
docker run -p 8000:8000 -p 8501:8501 --env-file .env jarvis-app
```
### Paso 2: Configurar el archivo .env
Crea un archivo .env en el directorio raíz con tu clave de OpenAI API:

```plaintext
OPENAI_API_KEY=tu_clave_openai
(Opcionalmente, puedes copiar y editar el archivo de ejemplo):
```
```bash
cp .env.example .env
```
### Paso 3: Construir la imagen Docker
Construye la imagen de Docker para el proyecto:

```bash
docker build -t jarvis-app .
```
### Paso 4: Ejecutar la aplicación
Inicia el contenedor con los puertos necesarios expuestos:

```bash
docker run -p 8000:8000 -p 8501:8501 --env-file .env jarvis-app
```
### Paso 5: Acceder a la aplicación
Backend (FastAPI): http://localhost:8000

Frontend (Streamlit): http://localhost:8501

### Uso
Abre el frontend en tu navegador (http://localhost:8501).

Completa los campos del formulario:

Información sobre el videojuego, plataforma, controles, etc.

Información personal como edad, sexo, idioma y país.

Haz clic en "Enviar".

Recibe una respuesta personalizada generada por JARVIS.

Subida a Docker Hub
Para desarrolladores:
Si deseas distribuir esta imagen, sigue estos pasos para subirla a Docker Hub:

Etiqueta la imagen:

```bash
docker tag jarvis-app tu-usuario-docker/jarvis-app:latest
Inicia sesión en Docker Hub:
```
```bash
docker login
Sube la imagen:
```
```bash
docker push tu-usuario-docker/jarvis-app:latest
Para usuarios:
Para descargar y ejecutar la imagen:
```
```bash
docker pull tu-usuario-docker/jarvis-app:latest
docker run -p 8000:8000 -p 8501:8501 --env OPENAI_API_KEY=tu_clave_openai tu-usuario-docker/jarvis-app:latest
```
### Estructura del Proyecto
```plaintext
/jarvis-app
│
├── app_backend.py       # Código del backend (FastAPI)
├── app_frontend.py      # Código del frontend (Streamlit)
├── requirements.txt     # Dependencias del proyecto
├── Dockerfile           # Dockerfile unificado
├── start.sh             # Script de inicio para backend y frontend
├── jarvis.db            # Base de datos SQLite
├── .env                 # Variables de entorno (no subir a Git)
└── .env.example         # Archivo de ejemplo para configuración
```
### Tecnologías Utilizadas
FastAPI: Framework para la construcción del backend.

Streamlit: Framework para la creación de aplicaciones web interactivas.

SQLite: Base de datos ligera para almacenamiento de interacciones.

Docker: Contenedores para la portabilidad y distribución.

### Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar:

Haz un fork del repositorio.

Crea una rama con tu funcionalidad:

```bash
git checkout -b nueva-funcionalidad
Realiza tus cambios y sube la rama:
```
```bash
git push origin nueva-funcionalidad
Abre un pull request.
```