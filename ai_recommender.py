import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # 🟢 Load variables from .env

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

    prompt = "Based on these books, recommend 5 similar books:\n"
    for title, author in books:
        prompt += f"- {title} by {author}\n"

    headers = {
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
    print("DEBUG:", data)  # 🔍 Debug log

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"AI Error: {data.get('error', {}).get('message', 'Unknown Error')}"
