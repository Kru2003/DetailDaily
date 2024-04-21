import streamlit as st
import sqlite3
    
# Create or connect to the SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def authenticate_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    return user is not None
    
def main():
    st.title("User Login")

    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False
    
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate_user(username, password):
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()