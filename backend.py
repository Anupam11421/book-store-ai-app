import sqlite3

def connect():
    conn=sqlite3.connect("books.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title text, author text, year integer, isbn integer)")
    conn.commit()
    conn.close()

def insert(title,author,year,isbn):
    conn=sqlite3.connect("books.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL,?,?,?,?)",(title,author,year,isbn))
    conn.commit()
    conn.close()
    view()

def view():
    conn=sqlite3.connect("books.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM book")
    rows=cur.fetchall()
    conn.close()
    return rows

def search(title="",author="",year="",isbn=""):
    conn=sqlite3.connect("books.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title,author,year,isbn))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn=sqlite3.connect("books.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?",(id,))
    conn.commit()
    conn.close()

def update(id,title,author,year,isbn):
    conn=sqlite3.connect("books.db")
    cur=conn.cursor()
    cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",(title,author,year,isbn,id))
    conn.commit()
    conn.close()

def seed_books():
    sample_books = [
        ("Atomic Habits", "James Clear", 2018, 11111),
        ("The Alchemist", "Paulo Coelho", 1988, 22222),
        ("1984", "George Orwell", 1949, 33333),
        ("Deep Work", "Cal Newport", 2016, 44444),
        ("Clean Code", "Robert C. Martin", 2008, 55555),
    ]
    for title, author, year, isbn in sample_books:
        insert(title, author, year, isbn)

# seed_books()  # 👈 Uncomment this to run ONCE


connect()
# insert("The Earth","John Smith",1918,913123132)
delete(5)
update(4,"The moon","John Smooth",1917,99999)
print(view())
print(search(author="John Smith")) 
