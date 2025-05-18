# Spaced Repetition Reminder System

This project is a custom-built **Spaced Repetition Reminder System** that intelligently reminds users to review important questions or concepts at optimal intervals to improve long-term retention. It follows the **SM-2 algorithm**, famously used in Anki flashcards, to adaptively schedule reviews based on recall performance.

It combines a lightweight **SQLite** backend, **Windows toast notifications**, and a clean **Streamlit frontend** for a complete offline-first learning tool.

---

## 🧱 Project Structure

### 📁 Database: `rev_questions.db`

The database contains a single table named `tracker_1_1`:

```sql
CREATE TABLE IF NOT EXISTS tracker_1_1 (
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
);
```

Each row represents a reviewable question with:

* `question`: The item to be remembered
* `description`: (Optional) Details or explanation of the question
* `ease_factor`: Adaptive measure (default 2.5) updated after each review
* `interval`: Days until the next review
* `review_count`: Number of times this question was reviewed
* `last_review_date` / `next_review_date`: Used to determine when a reminder is due
* `difficulty`: User-assigned label (Easy / Medium / Hard)

---

## 🧠 Key Python Modules

### `database.py`

This module handles all interactions with the database and includes the following functions:

#### `init_db()`

Initializes the database and ensures the `tracker_1_1` table exists.

#### `add_questions(question, description, difficulty)`

Inserts a new question into the database with default review scheduling parameters.

#### `fetch_for_rev()`

Returns a list of questions whose `next_review_date` is today or earlier, i.e., due for review.

#### `update_review(quality, question_id)`

Implements the **SM-2 spaced repetition algorithm**:

* Takes user feedback (`quality` score from 0 to 5)
* Updates the `ease_factor`, `interval`, `next_review_date`, and `review_count` based on the SM-2 logic
* Resets the interval if the answer was forgotten (score < 3)

#### `del_entry(question_id)`

Deletes a specific question from the database.

#### `debug_dump()`

Prints the full contents of the table (useful for debugging/testing).

---

## 🖥️ Streamlit Frontend

The project includes a lightweight, intuitive Streamlit frontend to manage spaced repetition questions efficiently. Here's a breakdown of the features provided through the interface:

➕ Add Question:
Allows users to add new questions along with descriptions. The initial review date is set based on the SM-2 algorithm logic, and tracked automatically.

✅ Review Questions:
Displays questions that are due for review today based on SM-2 scheduling. Users can rate each question based on difficulty after recalling it. This feedback updates the next review date dynamically.

🗑️ Delete Question:
Offers a searchable list of all stored questions with the option to delete any of them cleanly from the database. Useful for removing outdated or irrelevant entries.

📅 Review Schedule:
Shows an overview of all stored questions and their next scheduled review date. Helps users plan upcoming revisions and ensure spaced repetition is on track.

---

## 🔔 Windows Notifications: `reminder.py`

This script runs in the background to show reminders via Windows 10 toast notifications using the `win10toast` library:

* On script execution:

  * Calls `fetch_for_rev()` to find due questions
  * Displays each question as a toast notification

## Automation with Batch File & Task Scheduler
To ensure review reminders trigger without keeping the app always running, the project smartly uses:

A custom Batch File (reminder.bat)
This batch script:

Navigates to the project directory

Runs the reminder script (reminder.py) using the appropriate Python interpreter

# Windows Task Scheduler
The batch file is registered with Task Scheduler to:

Run the script at login or at fixed intervals

Ensure reminders are shown even after reboot

Avoid the need for a 24/7 background process or custom daemon
---

## 📊 How SM-2 Algorithm Works

The SM-2 algorithm dynamically adjusts review frequency based on how well you remembered a concept:

| Score | Meaning              | Effect                     |
| ----- | -------------------- | -------------------------- |
| 5     | Perfect recall       | Increase interval, EF      |
| 4     | Correct, some effort | Slightly increase interval |
| 3     | Correct, hard recall | Maintain or slightly raise |
| 2     | Incorrect, familiar  | Reset interval             |
| 1     | Incorrect, vague     | Reset interval             |
| 0     | Complete blackout    | Reset interval             |

Formula updates:

```python
new_ef = old_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
```

Interval progression (in days): 1 → 6 → 10 → 21 → 45 …

---

## ✅ Setup Instructions

### 1. Clone the Repo

```bash
git clone <your-repo-url>
cd spaced-repetition-reminder
```

### 2. Create a Virtual Environment (Python 3.11)

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit App

```bash
streamlit run main.py
```

---

## ⚠️ Troubleshooting

* If `streamlit` or any package isn't recognized:

  * Ensure you're in the correct virtual environment
  * Check `python --version` to confirm it's Python 3.11
* For toast notifications:

  * Ensure `win10toast` is installed
  * Make sure Task Scheduler runs with user login

---

## 🙌 Final Notes

This reminder system is a productivity tool designed to help learners and students stay consistent with revision and retention. By using proven cognitive science principles and simple automation, it helps make learning more efficient and sustainable.

