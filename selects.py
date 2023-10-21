import sqlite3
import os

DATABASE_FILE = "database.db"

def connect_to_db():
    return sqlite3.connect(DATABASE_FILE)

def show_all_persons():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM persons")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def search_by_first_name():
    name = input("Write the first name to search: ")
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM persons WHERE first_name=?", (name,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def search_by_last_name():
    name = input("Write the last name to search: ")
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM persons WHERE last_name=?", (name,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Show all persons")
        print("2. Search by first name")
        print("3. Search by last name")
        print("4. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            show_all_persons()
        elif choice == "2":
            search_by_first_name()
        elif choice == "3":
            search_by_last_name()
        elif choice == "4":
            print("Closing...")
            break
        else:
            print("Option invalid! Try again.")

if __name__ == "__main__":
    menu()
