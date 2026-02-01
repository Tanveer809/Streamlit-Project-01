import streamlit as st
import numpy as np
import pandas as pd
import sqlite3

# -------------------- DATABASE SETUP --------------------
conn = sqlite3.connect("userdata.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    skill TEXT,
    experience INTEGER,
    available TEXT
)
""")
conn.commit()

 

# Page config
st.set_page_config(page_title="Assignment 07 - Streamlit Portal", layout="centered")
st.title("Streamlit portal - Assignment -7")
st.write("welcome! please fill in the details bellow")

name= st.text_input("Enter your name")

age= st.number_input("Enter your age",min_value=1,max_value=100)

skill = st.selectbox(
    "select your primary skills",[
        "Python","data science","machine learning","web development"
    ]
)
experience= st.slider("enter your experience",0,10)

available = st.checkbox("are you available for work?")

if st.button("Submit Details"):
    cursor.execute("""
    INSERT INTO user_data (name, age, skill, experience, available)
    VALUES (?, ?, ?, ?, ?)
    """, (name, age, skill, experience, "Yes" if available else "No"))
    
    conn.commit()
    st.success("✅ Data saved successfully!")

# -------------------- FILE UPLOADER COMPONENT --------------------
st.divider()
st.subheader("📂 Upload CSV File")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### 📊 Uploaded Data Preview")
    st.dataframe(df)

    # Save uploaded data into ONE table
    df.to_sql("uploaded_data", conn, if_exists="replace", index=False)
    st.success("✅ File data stored in database table!")

# -------------------- DISPLAY STORED DATA --------------------
st.divider()
st.subheader("🗄️ Stored User Data")

stored_df = pd.read_sql("SELECT * FROM user_data", conn)
st.dataframe(stored_df)