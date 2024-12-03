import uvicorn
import os
from fastapi import FastAPI, HTTPException, Request
import sqlite3
import openai
from datetime import datetime
from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicializar FastAPI
app = FastAPI()

# Configurar la base de datos SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jarvis.db")
conn = sqlite3.connect('jarvis.db', check_same_thread=False)
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        videogame TEXT,
        issue TEXT,
        platform TEXT,
        controls TEXT,
        sound BOOLEAN,
        sex TEXT,
        age INTEGER,
        country TEXT,
        language TEXT,
        response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Ruta de prueba
@app.get("/")
async def hello():
    return {"message": "Hello, this is JARVIS - Video Game Assistant"}

@app.post("/query")
async def process_query(request: Request):
    """
    Procesa la consulta del usuario, obtiene información contextual y personal,
    y genera una respuesta personalizada usando GPT.
    """
    data = await request.json()

    # Extraer datos del cuerpo de la solicitud
    context = data.get("context", {})
    user = data.get("user", {})

    # Validar entradas
    required_context_fields = ["videogame", "issue", "platform", "controls", "sound"]
    required_user_fields = ["sex", "age", "country", "language"]

    for field in required_context_fields:
        if not context.get(field):
            raise HTTPException(status_code=400, detail=f"El campo '{field}' es obligatorio en el contexto.")

    for field in required_user_fields:
        if not user.get(field):
            raise HTTPException(status_code=400, detail=f"El campo '{field}' es obligatorio en la información del usuario.")

    # Construir el prompt para GPT
    prompt = (
        f"Presentate como JARVIS su asistente.\n"
        f"El usuario juega a {context['videogame']} en la plataforma {context['platform']} "
        f"usando {context['controls']}. ¿Juega con sonido? {'Sí' if context['sound'] else 'No'}.\n"
        f"Problema descrito: {context['issue']}.\n"
        f"Usuario:\n"
        f"- Sexo: {user['sex']}\n"
        f"- Edad: {user['age']}\n"
        f"- País: {user['country']}\n"
        f"- Idioma: {user['language']}.\n\n"
        f"Proporciona una respuesta clara y útil segun su idioma y edad."
    )

    try:
        # Llamar a la API de OpenAI para generar la respuesta
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente de videojuegos llamado JARVIS."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        gpt_response = response.choices[0].message.content

        # Guardar la interacción en la base de datos
        try:
            cursor.execute("""
                INSERT INTO interactions (
                    videogame, issue, platform, controls, sound,
                    sex, age, country, language, response, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                context['videogame'], context['issue'], context['platform'], context['controls'], context['sound'],
                user['sex'], user['age'], user['country'], user['language'], gpt_response, datetime.utcnow()
            ))
            conn.commit()
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {str(e)}")

        return {
            "query": {
                "context": context,
                "user": user
            },
            "response": gpt_response
        }

    except openai.OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"Error al obtener respuesta de GPT: {str(e)}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
# Ruta para obtener todas las interacciones
@app.get("/interactions")
async def get_interactions():
    """
    Devuelve todas las interacciones almacenadas en la base de datos.
    """
    print("hola q ase")
    cursor.execute("SELECT * FROM interactions ORDER BY timestamp DESC")
    results = cursor.fetchall()
    return {"results": results}

# Ruta para obtener una interacción específica por ID
@app.get("/interactions/{interaction_id}")
async def get_interaction(interaction_id: int):
    """
    Devuelve una interacción específica según su ID.
    """
    print("hola q ase")
    cursor.execute("SELECT * FROM interactions WHERE id = ?", (interaction_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Interacción no encontrada.")
    return {"interaction": result}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)