import sqlite3
import requests
import os
from dotenv import load_dotenv

# 🔐 Load the API key from .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT title, author FROM book")
    data = cur.fetchall()
    conn.close()
    return data

def get_recommendation():
    books = get_books()
    if not books:
        return "No books found in your library."

    # 🧠 Prompt for AI model
    prompt = "Based on these books, recommend 5 similar books:\n"
    for title, author in books:
        prompt += f"- {title} by {author}\n"

    headers = {
    "HTTP-Referer": "https://github.com/Anupam11421/book-store-ai-app",  # <-- Required
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }

    headers = {
    "HTTP-Referer": "https://github.com/Anupam11421/book-store-ai-app",  # <-- Required
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }

    headers = {
    "HTTP-Referer": "https://github.com/Anupam11421/book-store-ai-app",  # <-- Required
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }

    headers = {
    "HTTP-Referer": "https://github.com/Anupam11421/book-store-ai-app",  # <-- Required
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }


    body = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body
    )

    data = response.json()
    print("DEBUG:", data)  # Remove this after testing

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"AI Error: {data.get('error', {}).get('message', 'Unknown Error')}"
