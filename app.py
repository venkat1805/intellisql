from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to convert user question into SQL using Gemini 1.5
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    full_prompt = prompt[0] + "\n\nQuestion: " + question
    response = model.generate_content(full_prompt)
    return response.text.strip()

# Function to run SQL query on the test.db database
def read_sql_query(sql, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Prompt for Gemini to understand the DB schema
prompt = ["""
You are an expert in converting English questions into SQL queries.
The SQL database has a table called STUDENT with the following columns:
- NAME (text)
- CLASS (text)
- SECTION (text)

Here are a few examples:
Q: How many entries of records are present?
A: SELECT COUNT(*) FROM STUDENT;

Q: Tell me all the students studying in Data Science class.
A: SELECT * FROM STUDENT WHERE CLASS="Data Science";

Only return the SQL query, no explanations, no markdown formatting.
"""]

# Streamlit app UI
st.set_page_config(page_title="IntelliSQL — Natural Language to SQL")
st.title("💡 IntelliSQL — Ask Questions, Get SQL")

question = st.text_input("Ask your question in English:")

if st.button("Submit"):
    try:
        sql_query = get_gemini_response(question, prompt)
        st.subheader("🧠 Generated SQL Query:")
        st.code(sql_query, language="sql")

        results = read_sql_query(sql_query, "test.db")

        st.subheader("📊 Query Results:")
        if results:
            for row in results:
                st.write(row)
        else:
            st.info("No results found.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
