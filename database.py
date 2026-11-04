import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "NewPassword123!",
    "database": "interview_tracker",
}


def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print("Database connection error:", e)
    return None


def create_tables():
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                difficulty VARCHAR(50) DEFAULT 'Easy',
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS practice_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                category VARCHAR(100),
                questions_attempted INT DEFAULT 0,
                questions_correct INT DEFAULT 0,
                score DECIMAL(5,2) DEFAULT 0,
                session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mock_interviews (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                interview_type VARCHAR(100),
                questions_attempted INT DEFAULT 0,
                questions_correct INT DEFAULT 0,
                score DECIMAL(5,2) DEFAULT 0,
                feedback TEXT,
                interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                topic VARCHAR(100),
                completed_questions INT DEFAULT 0,
                correct_answers INT DEFAULT 0,
                score DECIMAL(5,2) DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        connection.commit()
        return True

    except Error as e:
        print("Error creating tables:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_or_create_default_user():
    connection = create_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        email = "test@gmail.com"
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return user["id"]

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            ("Test User", email, "test123"),
        )
        connection.commit()
        return cursor.lastrowid

    except Error as e:
        print("Error creating default user:", e)
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()


def add_user(name, email, password):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (name, email, password),
        )
        connection.commit()
        return True
    except Error as e:
        print("Error adding user:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_user(email, password):
    connection = create_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s AND password = %s
            """,
            (email, password),
        )
        return cursor.fetchone()
    except Error as e:
        print("Error checking user:", e)
        return None
    finally:
        cursor.close()
        connection.close()


def add_question(question, category, difficulty="Easy", answer=""):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO questions (question, category, difficulty, answer)
            VALUES (%s, %s, %s, %s)
            """,
            (question, category, difficulty, answer),
        )
        connection.commit()
        return True
    except Error as e:
        print("Error adding question:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_questions(category=None):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        if category and category != "All":
            cursor.execute(
                """
                SELECT *
                FROM questions
                WHERE category = %s
                ORDER BY id DESC
                """,
                (category,),
            )
        else:
            cursor.execute("SELECT * FROM questions ORDER BY id DESC")
        return cursor.fetchall()
    except Error as e:
        print("Error getting questions:", e)
        return []
    finally:
        cursor.close()
        connection.close()


def add_practice_session(
    user_id, category, questions_attempted, questions_correct, score
):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO practice_sessions
            (user_id, category, questions_attempted, questions_correct, score)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, category, questions_attempted, questions_correct, score),
        )
        connection.commit()
        return True
    except Error as e:
        print("Error saving practice session:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_practice_sessions(user_id):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT *
            FROM practice_sessions
            WHERE user_id = %s
            ORDER BY session_date DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()
    except Error as e:
        print("Error getting practice sessions:", e)
        return []
    finally:
        cursor.close()
        connection.close()


def add_mock_interview(
    user_id, interview_type, questions_attempted,
    questions_correct, score, feedback
):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO mock_interviews
            (user_id, interview_type, questions_attempted,
             questions_correct, score, feedback)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_id, interview_type, questions_attempted,
                questions_correct, score, feedback
            ),
        )
        connection.commit()
        return True
    except Error as e:
        print("Error saving mock interview:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_mock_interviews(user_id):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT *
            FROM mock_interviews
            WHERE user_id = %s
            ORDER BY interview_date DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()
    except Error as e:
        print("Error getting mock interviews:", e)
        return []
    finally:
        cursor.close()
        connection.close()


def add_progress(
    user_id, topic, completed_questions, correct_answers, score
):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO progress
            (user_id, topic, completed_questions, correct_answers, score)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, topic, completed_questions, correct_answers, score),
        )
        connection.commit()
        return True
    except Error as e:
        print("Error saving progress:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_progress(user_id):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT *
            FROM progress
            WHERE user_id = %s
            ORDER BY updated_at DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()
    except Error as e:
        print("Error getting progress:", e)
        return []
    finally:
        cursor.close()
        connection.close()


def get_dashboard_stats(user_id):
    connection = create_connection()
    empty = {
        "total_questions": 0,
        "practice_sessions": 0,
        "mock_interviews": 0,
        "average_score": 0,
    }

    if connection is None:
        return empty

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM questions")
        total_questions = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM practice_sessions WHERE user_id = %s",
            (user_id,),
        )
        practice_sessions = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM mock_interviews WHERE user_id = %s",
            (user_id,),
        )
        mock_interviews = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT AVG(score) AS average FROM practice_sessions WHERE user_id = %s",
            (user_id,),
        )
        average_score = cursor.fetchone()["average"] or 0

        return {
            "total_questions": total_questions,
            "practice_sessions": practice_sessions,
            "mock_interviews": mock_interviews,
            "average_score": round(float(average_score), 2),
        }
    except Error as e:
        print("Error getting dashboard statistics:", e)
        return empty
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print("=" * 50)
    print("INTERVIEW PREPARATION TRACKER")
    print("MYSQL DATABASE TEST")
    print("=" * 50)

    connection = create_connection()

    if connection:
        print("MySQL connection successful!")
        connection.close()

        if create_tables():
            user_id = get_or_create_default_user()
            print("Default user ID:", user_id)
            print("Database setup completed successfully!")
        else:
            print("Table creation failed.")
    else:
        print("MySQL connection failed!")
        print("Check MySQL username, password and database.")
