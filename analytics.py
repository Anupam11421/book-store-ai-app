import sqlite3
import matplotlib.pyplot as plt
from collections import Counter

def get_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT author, year FROM book")
    data = cur.fetchall()
    conn.close()
    return data

def show_analytics():
    data = get_books()

    if not data:
        print("No book data to show.")
        return

    authors = [row[0] for row in data]
    years = [row[1] for row in data]

    author_counts = Counter(authors).most_common(5)
    year_counts = Counter(years)

    # 📊 Subplot layout
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Reading Analytics")

    # ✍️ Top Authors
    axs[0].bar([a[0] for a in author_counts], [a[1] for a in author_counts], color="skyblue")
    axs[0].set_title("Top 5 Authors")
    axs[0].set_xlabel("Author")
    axs[0].set_ylabel("Books")

    # 📅 Books per Year
    axs[1].bar(year_counts.keys(), year_counts.values(), color="orange")
    axs[1].set_title("Books by Year")
    axs[1].set_xlabel("Year")
    axs[1].set_ylabel("Count")

    plt.tight_layout()
    plt.show()
