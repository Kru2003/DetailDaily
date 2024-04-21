import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

def register_user(username, password):
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    
def check_existing_user(username):
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user is not None

def main():
    st.title("User Registration")
    
    st.header("Register")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    register_button = st.button("Register")

    if register_button:
        if check_existing_user(new_username):
            st.error("User already exists. Please login.")
            st.markdown("[Login Here](Login)")
            return
        else:
            register_user(new_username, new_password)
            st.success("Registration successful! Please proceed to login.")

if __name__ == "__main__":
    main()
