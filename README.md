# 🎯 Interview Preparation Tracker

A Streamlit + MySQL project for interview preparation.

## Features

- Dashboard
- Question bank
- Python / SQL / Java / AIML / HR questions
- Practice sessions
- Mock interviews
- Progress tracking
- MySQL database

## Project Structure

```text
Interview_Preparation_Tracker/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
└── pages/
    ├── 1_Questions.py
    ├── 2_Practice.py
    ├── 3_Mock_Interview.py
    └── 4_Progress.py
```

## 1. Create the database

Open MySQL and run:

```sql
CREATE DATABASE interview_tracker;
```

## 2. Check database password

Open `database.py` and update:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "interview_tracker",
}
```

## 3. Install packages

```powershell
py -m pip install -r requirements.txt
```

## 4. Test MySQL

```powershell
py database.py
```

You should see:

```text
MySQL connection successful!
Database setup completed successfully!
```

## 5. Run Streamlit

```powershell
py -m streamlit run app.py
```

The app will open in your browser.

## Default user

The application automatically creates:

- Email: test@gmail.com
- Password: test123

This is only for the current simple demo version. For a production application, passwords should be securely hashed.
