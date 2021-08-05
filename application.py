import sqlite3
from sqlite3 import Error
from tkinter import *
from tkinter.ttk import Treeview


class runGUI:

    # Initializing the GUI with buttons and text boxes
    def __init__(self, root):
        self.root = root

        # Initiate GUI
        root.title("Movie Database")
        root.iconbitmap("ponyo.ico")
        root.geometry('1000x600')

        # Three wrappers: Result, Search and Data Field
        top_wrapper = LabelFrame(root, text="Result Field")
        middle_wrapper = LabelFrame(root, text="Search Field")
        bottom_wrapper = LabelFrame(root, text="Data Field")

        top_wrapper.pack(fill="both", expand="yes", padx=20, pady=10)
        middle_wrapper.pack(fill="both", expand="yes", padx=20, pady=10)
        bottom_wrapper.pack(fill="both", expand="yes", padx=20, pady=10)

        # Creating Tree
        global tree
        columns = ['ID', 'Name', 'Release Date', 'Director', 'Ratings']
        tree = Treeview(top_wrapper, columns=columns, show="headings")
        tree.pack()

        tree.heading(0, text="ID")
        tree.heading(1, text="Name")
        tree.heading(2, text="Release Date")
        tree.heading(3, text="Director")
        tree.heading(4, text="Ratings")

        # Double Click Method
        tree.bind('<Double 1>', self.getrow)

        global search_release_box, search_name_box

        search_release_label = Label(middle_wrapper, text="Search by Release Date:")
        search_release_label.grid(row=0, column=0, padx=10, pady=(10, 0))

        search_release_box = Entry(middle_wrapper, width=30)
        search_release_box.grid(row=0, column=1, padx=(0, 20), pady=(10, 0))

        search_name_label = Label(middle_wrapper, text="Search by Name:")
        search_name_label.grid(row=0, column=2, padx=10, pady=(10, 0))

        search_name_box = Entry(middle_wrapper, width=30)
        search_name_box.grid(row=0, column=3, padx=(0, 20), pady=(10, 0))

        global name, release_date, director, ratings

        name_label = Label(bottom_wrapper, text="Name")
        name_label.grid(row=0, column=0, pady=(10, 0))
        name = Entry(bottom_wrapper, width=30)
        name.grid(row=0, column=1, padx=20, pady=(10, 0))

        release_date_label = Label(bottom_wrapper, text="Release Date")
        release_date_label.grid(row=0, column=2)
        release_date = Entry(bottom_wrapper, width=30)
        release_date.grid(row=0, column=3)

        director_label = Label(bottom_wrapper, text="Director")
        director_label.grid(row=1, column=0)
        director = Entry(bottom_wrapper, width=30)
        director.grid(row=1, column=1)

        ratings_label = Label(bottom_wrapper, text="Ratings")
        ratings_label.grid(row=1, column=2)
        ratings = Entry(bottom_wrapper, width=30)
        ratings.grid(row=1, column=3)

        # Buttons:
        search_btn = Button(middle_wrapper, text="Search", command=self.search, font="Raleway", bg="#20bebe", fg="white",
                            height=2, width=10, justify=CENTER)
        search_btn.grid(row=0, column=4, columnspan=2, sticky=S, pady=(10, 0), padx=(20, 0))

        clear_btn = Button(middle_wrapper, text="Clear", command=self.clear, font="Raleway", bg="#20bebe", fg="white",
                           height=2, width=10, justify=CENTER)
        clear_btn.grid(row=0, column=6, columnspan=2, sticky=S, pady=(10, 0), padx=(20, 0))

        add_btn = Button(bottom_wrapper, text="Add", command=self.add, font="Raleway", bg="#20bebe", fg="white",
                         height=2, width=10, justify=CENTER)
        add_btn.grid(row=0, column=6, columnspan=2, sticky=E + S, pady=(10, 0), padx=(30, 0))

        edit_btn = Button(bottom_wrapper, text="Edit", command=self.edit, font="Raleway", bg="#20bebe", fg="white",
                          height=2, width=10, justify=CENTER)
        edit_btn.grid(row=0, column=8, columnspan=2, sticky=E + S, pady=(10, 0), padx=(30, 0))

        delete_btn = Button(bottom_wrapper, text="Delete", command=self.delete, font="Raleway", bg="#20bebe", fg="white",
                            height=2, width=10, justify=CENTER)
        delete_btn.grid(row=0, column=10, columnspan=2, sticky=E + S, pady=(10, 0), padx=(30, 0))

    # Method to get information from Treeview (double clicking function)
    def getrow(self, event):

        # Delete text box entry
        name.delete(0, END)
        release_date.delete(0, END)
        director.delete(0, END)
        ratings.delete(0, END)

        selected = tree.focus()
        values = tree.item(selected, 'values')
        name.insert(0, values[1])
        release_date.insert(0, values[2])
        director.insert(0, values[3])
        ratings.insert(0, values[4])

    # Method to search with name of movie & release date (both must be entered in)
    def search(self):
        conn = sqlite3.connect('my_movies.db')
        c = conn.cursor()

        release_var = search_release_box.get()
        name_var = search_name_box.get()

        # Delete text box entry
        search_release_box.delete(0, END)
        search_name_box.delete(0, END)

        c.execute("SELECT * FROM movies WHERE release_date LIKE ? AND name LIKE ?",
                  ('%' + release_var + '%', '%' + name_var + '%',))

        rows = c.fetchall()
        update(rows)

        # Commit changes
        conn.commit()
        conn.close()

    #  Clear the search field and show all data in treeview
    def clear(self):
        conn = sqlite3.connect('my_movies.db')
        showTree(conn)

        search_release_box.delete(0, END)
        search_name_box.delete(0, END)

        conn.commit()
        conn.close()

    # Method to add data to database
    def add(self):
        # Database connection:
        conn = sqlite3.connect('my_movies.db')
        c = conn.cursor()

        add_query = """ INSERT INTO movies (name, release_date, director, ratings) VALUES (?, ?, ?, ?); """

        data_tuple = (name.get(), release_date.get(), director.get(), ratings.get())

        c.execute(add_query, data_tuple)

        # Delete text box entry
        name.delete(0, END)
        release_date.delete(0, END)
        director.delete(0, END)
        ratings.delete(0, END)
        # Commit changes
        conn.commit()

        showTree(conn)
        # Close connection
        conn.close()

    # Method to edit data - double click data to fill the data field then modify data by pressing edit
    def edit(self):
        # Database connection:
        conn = sqlite3.connect('my_movies.db')
        c = conn.cursor()

        selected = tree.focus()
        values = tree.item(selected, 'values')

        edit_query = """UPDATE movies SET name = ?, release_date = ?, director = ?, ratings = ? WHERE ID = ?"""
        data_edit = (name.get(), release_date.get(), director.get(), ratings.get(), values[0])

        c.execute(edit_query, data_edit)
        # Delete text box entry
        name.delete(0, END)
        release_date.delete(0, END)
        director.delete(0, END)
        ratings.delete(0, END)

        # Commit changes
        conn.commit()
        showTree(conn)
        # Close connection
        conn.close()

    # Method to delete data - double click data to delete and press button to delete
    def delete(self):
        # Database connection:
        conn = sqlite3.connect('my_movies.db')
        c = conn.cursor()

        selected = tree.focus()
        values = tree.item(selected, 'values')
        id_var = values[0]

        delete_query = """DELETE FROM movies WHERE id = ?"""
        c.execute(delete_query, (id_var,))

        x = tree.selection()
        for record in x:
            tree.delete(record)

        name.delete(0, END)
        release_date.delete(0, END)
        director.delete(0, END)
        ratings.delete(0, END)

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

""" Function for creating connection, creating table and showing treeview"""

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, my_table):
    try:
        c = conn.cursor()
        c.execute(my_table)
    except Error as e:
        print(e)

def update(rows):
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)

def showTree(conn):
    c = conn.cursor()
    query = "SELECT * from movies"
    c.execute(query)
    rows = c.fetchall()
    update(rows)

def main():
    connection = "my_movies.db"

    my_table = """CREATE TABLE IF NOT EXISTS movies (

            id integer PRIMARY KEY,
            name text,
            release_date text,
            director text,
            ratings integer

    );"""

    conn = create_connection(connection)

    if conn is not None:
        create_table(conn, my_table)

    else:
        print("Error, could not create database connection.")

    with conn:
        showTree(conn)


if __name__ == '__main__':
    root = Tk()
    my_gui = runGUI(root)
    main()
    root.mainloop()