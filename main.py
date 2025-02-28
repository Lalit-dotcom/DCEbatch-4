import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

# Database Connection
def connect_db():
    conn = sqlite3.connect("mydb.db")
    return conn

# Create Table
def create_Table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS student 
                (name TEXT, password TEXT, roll INTEGER PRIMARY KEY, branch TEXT)''')
    conn.commit()
    conn.close()

# Add Record
def addRecord(data):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO student(name, password, roll, branch) VALUES (?, ?, ?, ?)', data)
        conn.commit()
        st.success("User registered successfully! 🎉")
    except sqlite3.IntegrityError as e:
        st.error("User already registered! ❌")
    finally:
        conn.close()

# View All Records
def view_record():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student')
    result = cur.fetchall()
    conn.close()
    return result

# Authenticate User
def authenticate(roll, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE roll=? AND password=?', (roll, password))
    user = cur.fetchone()
    conn.close()
    return user

# Search User
def search_user(roll):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student WHERE roll=?', (roll,))
    user = cur.fetchone()
    conn.close()
    return user

# Update Password
def reset_password(roll, new_password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE student SET password=? WHERE roll=?', (new_password, roll))
    conn.commit()
    conn.close()
    st.success("Password updated successfully!")

# Delete User
def delete_user(roll):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM student WHERE roll=?', (roll,))
    conn.commit()
    conn.close()
    st.success("User deleted successfully!")

# Initialize Table
create_Table()

# Sidebar - Displays Results
with st.sidebar:
    selected = option_menu('Navigation', ['Sign Up', 'Sign In', 'Search User', 'Reset Password', 'Delete User', 'View All'])

# Main Section - User Input Forms
if selected == 'Sign Up':
    st.subheader("Create an Account")
    name = st.text_input("Enter your Name")
    roll = st.number_input("Enter your Roll Number", step=1, format="%d")
    branch = st.text_input("Enter your Branch")
    password = st.text_input("Enter your Password", type="password")
    repass = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password != repass:
            st.error("Passwords do not match! ❌")
        else:
            addRecord((name, password, roll, branch))

elif selected == 'Sign In':
    st.subheader("Login to Your Account")
    roll = st.number_input("Enter your Roll Number", step=1, format="%d")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Login"):
        user = authenticate(roll, password)
        if user:
            st.sidebar.success(f"Welcome, {user[0]}! 🎉")
        else:
            st.error("Invalid Roll Number or Password! ❌")

elif selected == 'Search User':
    st.subheader("Search Student Record")
    roll = st.number_input("Enter Roll Number to Search", step=1, format="%d")
    
    if st.button("Search"):
        user = search_user(roll)
        if user:
            st.sidebar.write(f"**Name:** {user[0]}")
            st.sidebar.write(f"**Roll Number:** {user[2]}")
            st.sidebar.write(f"**Branch:** {user[3]}")
        else:
            st.error("User not found!")

elif selected == 'Reset Password':
    st.subheader("Reset Password")
    roll = st.number_input("Enter your Roll Number", step=1, format="%d")
    new_password = st.text_input("Enter New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if new_password != confirm_password:
            st.error("Passwords do not match! ❌")
        else:
            reset_password(roll, new_password)

elif selected == 'Delete User':
    st.subheader("Delete Student Record")
    roll = st.number_input("Enter Roll Number to Delete", step=1, format="%d")

    if st.button("Delete"):
        delete_user(roll)

elif selected == 'View All':
    st.subheader("All Student Records")
    data = view_record()
    st.sidebar.table(data)
