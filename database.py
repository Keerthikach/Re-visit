import sqlite3
import datetime
import os
import logging

def add_questions(question,difficulty,description=None):
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO tracker_1_1 (question,description,added_date,difficulty,next_review_date) VALUES(?,?,?,?,?)",
                   (question,description,datetime.datetime.now().strftime('%Y-%m-%d'),difficulty,datetime.date.today()+datetime.timedelta(days=1)))

    conn.commit()
    conn.close()

def debug_dump():
    conn = sqlite3.connect("rev_questions.db")
    cursor  = conn.cursor()
    cursor.execute("SELECT id, question,description, added_date, next_review_date FROM tracker_1_1")
    x=cursor.fetchall()
    conn.close() 
    return x 

LOG_PATH = r"C:\Users\keert\OneDrive\Desktop\projects\Re-visit\fetch.log"

# # 2) ensure the directory is there (optional guard)
# os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# # 3) configure logging
# logging.basicConfig(
#     filename=LOG_PATH,                   # your real .log file
#     filemode='a',                        # append, rather than overwrite
#     level=logging.INFO,                  # capture INFO+ messages
#     format="%(asctime)s %(levelname)s: %(message)s"
# )       

def fetch_for_rev():
    # cwd = os.getcwd()
    # dbpath = os.path.join(cwd, "rev_questions.db")
    # logging.info(f"cwd={cwd!r}, opening DB at {dbpath!r}")

    today=datetime.date.today().isoformat()
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()
    cursor.execute("SELECT id,question,description,difficulty FROM tracker_1_1 WHERE next_review_date <= ?",(today,))
    x=cursor.fetchall()
    #logging.info(f"rows returned: {x!r}")
    conn.close()
    return x 

def del_entry(ques_id):
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM tracker_1_1 WHERE id=?",(ques_id,))
    conn.commit()
    conn.close()

def init_db():
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()

    cursor.execute("""
              CREATE TABLE IF NOT EXISTS tracker_1_1(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   question TEXT NOT NULL,
                   description TEXT,
                   added_date TEXT NOT NULL DEFAULT (DATE('now')),
                   last_review_date TEXT,
                   next_review_date TEXT,
                   ease_factor REAL DEFAULT 2.5,
                   interval INTEGER DEFAULT 1,
                   review_count INTEGER DEFAULT 0,
                   difficulty TEXT 
                   )  
    """)

    conn.commit()
    conn.close()

def update_review(quality,question_id):
    conn=sqlite3.connect("rev_questions.db")
    cursor=conn.cursor()

    cursor.execute("SELECT ease_factor,interval FROM tracker_1_1 WHERE id=?",(question_id,))
    row=cursor.fetchone()

    if row is not None:
        ef,interval=row 

    if quality<3:
        interval=1  
    else:
        interval=int(ef*interval)
        ef += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        ef = max(1.3, ef) 

    next_review=(datetime.date.today()+datetime.timedelta(days=interval)).isoformat()    

    cursor.execute("""
            UPDATE tracker_1_1 SET 
            last_review_date=?,
            next_review_date=?,
            ease_factor=?,
            interval=?,
            review_count=review_count+1                                          
        WHERE id=? """,(datetime.date.today().isoformat(),next_review,ef,interval,question_id))
    
    conn.commit()
    conn.close()

# init_db()  
#add_questions("Three Sum","Medium")
#print(debug_dump())
#print(fetch_for_rev())
# update_review(3,7)
#del_entry(18)
