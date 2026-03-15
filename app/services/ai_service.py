import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def clasificar_intencion(pregunta: str) -> dict:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Clasifica la pregunta del usuario en una de estas intenciones: "
                        "total_tickets, tickets_abiertos, tickets_cerrados, total_categorias, "
                        "lista_categorias, categoria_mas_usada, desconocida. "
                        "Responde SOLO en JSON con este formato: "
                        '{"intent":"...", "estado":"..."} '
                        "Si no aplica estado, usa cadena vacía."
                    )
                },
                {
                    "role": "user",
                    "content": pregunta
                }
            ],
            temperature=0,
            max_tokens=80
        )

        contenido = completion.choices[0].message.content
        return json.loads(contenido)

    except Exception:
        return {"intent": "desconocida", "estado": ""}


def generar_respuesta_ia(contexto: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente y analista de datos de un sistema de soporte técnico. "
                        "Responde siempre en español, de forma clara, breve, natural y profesional. "
                        "No uses markdown. No uses asteriscos. No pongas títulos. "
                        "No saludes de forma larga. No inventes información. "
                        "Si es un análisis de dashboard, redacta un párrafo corto de 3 a 4 líneas."
                    )
                },
                {
                    "role": "user",
                    "content": contexto
                }
            ],
            temperature=0.2,
            max_tokens=180
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error con IA: {str(e)}"