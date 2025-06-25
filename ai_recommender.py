import sqlite3
import requests

# 🟢 Your FREE OpenRouter API Key
API_KEY = "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"  # 👈 Replace with your real key

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

    # 📘 Prompt for AI
    prompt = "Based on these books, recommend 5 similar books:\n"
    for title, author in books:
        prompt += f"- {title} by {author}\n"

    # 📡 API call to OpenRouter
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ Free model on OpenRouter
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body
    )

    # 🛠 Debug print to see actual response
    print("DEBUG:", response.json())

    # ✅ Handle missing 'choices' safely
    data = response.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"AI Error: {data.get('error', {}).get('message', 'Unknown Error')}"
