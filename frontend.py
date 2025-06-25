from tkinter import *
from tkinter import messagebox
import ai_recommender 
import backend
import analytics
import auth

# 👇 User login check
auth.connect_user_table()

def open_bookstore(username):
    window = Tk()
    window.wm_title(f"BookStore – Welcome {username}")

    def get_selected_row(event):
        try:
            global selected_tuple
            index = list1.curselection()[0]
            selected_tuple = list1.get(index)
            e1.delete(0, END)
            e1.insert(END, selected_tuple[1])
            e2.delete(0, END)
            e2.insert(END, selected_tuple[2])
            e3.delete(0, END)
            e3.insert(END, selected_tuple[3])
            e4.delete(0, END)
            e4.insert(END, selected_tuple[4])
        except IndexError:
            pass

    def view_command():
        list1.delete(0, END)
        for row in backend.view():
            list1.insert(END, row)

    def search_command():
        list1.delete(0, END)
        for row in backend.search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()):
            list1.insert(END, row)

    def add_command():
        backend.insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        list1.delete(0, END)
        list1.insert(END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))

    def delete_command():
        backend.delete(selected_tuple[0])
        view_command()

    def update_command():
        backend.update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
        view_command()

    l1 = Label(window, text="Title")
    l1.grid(row=0, column=0)

    l2 = Label(window, text="Author")
    l2.grid(row=0, column=2)

    l3 = Label(window, text="Year")
    l3.grid(row=1, column=0)

    l4 = Label(window, text="ISBN")
    l4.grid(row=1, column=2)

    title_text = StringVar()
    e1 = Entry(window, textvariable=title_text)
    e1.grid(row=0, column=1)

    author_text = StringVar()
    e2 = Entry(window, textvariable=author_text)
    e2.grid(row=0, column=3)

    year_text = StringVar()
    e3 = Entry(window, textvariable=year_text)
    e3.grid(row=1, column=1)

    isbn_text = StringVar()
    e4 = Entry(window, textvariable=isbn_text)
    e4.grid(row=1, column=3)

    list1 = Listbox(window, height=6, width=35)
    list1.grid(row=2, column=0, rowspan=6, columnspan=2)

    sb1 = Scrollbar(window)
    sb1.grid(row=2, column=2, rowspan=6)

    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)

    list1.bind('<<ListboxSelect>>', get_selected_row)
    
    def show_ai_suggestions():
        result = ai_recommender.get_recommendation()
        messagebox.showinfo("AI Book Suggestions", result)

    Button(window, text="View all", width=12, command=view_command).grid(row=2, column=3)
    Button(window, text="Search entry", width=12, command=search_command).grid(row=3, column=3)
    Button(window, text="Add entry", width=12, command=add_command).grid(row=4, column=3)
    Button(window, text="Update selected", width=12, command=update_command).grid(row=5, column=3)
    Button(window, text="Delete selected", width=12, command=delete_command).grid(row=6, column=3)
    Button(window, text="Close", width=12, command=window.destroy).grid(row=7, column=3)
    b7 = Button(window, text="Analytics", width=12, command=analytics.show_analytics)
    b7.grid(row=8, column=3)
    b8 = Button(window, text="AI Suggest", width=12, command=show_ai_suggestions)
    b8.grid(row=9, column=3)

    
    
    window.mainloop()

# 👇 Login UI
login_win = Tk()
login_win.title("Login or Signup")

Label(login_win, text="Username").grid(row=0, column=0)
Label(login_win, text="Password").grid(row=1, column=0)

username_entry = Entry(login_win)
username_entry.grid(row=0, column=1)

password_entry = Entry(login_win, show="*")
password_entry.grid(row=1, column=1)

def handle_login():
    username = username_entry.get()
    password = password_entry.get()
    if auth.login(username, password):
        login_win.destroy()
        open_bookstore(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def handle_signup():
    username = username_entry.get()
    password = password_entry.get()
    if auth.signup(username, password):
        messagebox.showinfo("Signup Success", "You can now login.")
    else:
        messagebox.showerror("Signup Failed", "Username already exists.")

Button(login_win, text="Login", command=handle_login).grid(row=2, column=0)
Button(login_win, text="Signup", command=handle_signup).grid(row=2, column=1)

login_win.mainloop()
