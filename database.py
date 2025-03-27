import sqlite3
from datetime import datetime

def add_questions(question,description=None):
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO tracker (question,description,added_date) VALUES(?,?,?)",
                   (question,description,datetime.now().strftime('%Y-%m-%d')))

    conn.commit()
    conn.close()

def fetch_for_rev():
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()
    cursor.execute("SELECT id,question,description FROM tracker WHERE date(added_date) <= date('now', '-1 day')")

    x=cursor.fetchall()
    conn.close()
    return x 

def del_entry(ques_id):
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM tracker WHERE id=?",(ques_id,))
    conn.commit()
    conn.close()

def init_db():
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()

    cursor.execute("""
              CREATE TABLE IF NOT EXISTS tracker(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   question TEXT NOT NULL,
                   description TEXT,
                   added_date TEXT NOT NULL DEFAULT (DATE('now'))
                   )  
    """)

    conn.commit()
    conn.close()
