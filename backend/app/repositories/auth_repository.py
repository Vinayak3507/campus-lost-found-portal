from mysql.connector import Error
from app.db.session import get_connection

#fetching user details

def get_user_by_email(college_email: str):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM users
            WHERE college_email = %s
        """
        cursor.execute(query, (college_email,))
        return cursor.fetchone()

    except Error as e:
        print(f"Database Error: {e}")
        raise Exception(str(e))

    finally:
        cursor.close()
        connection.close()


def get_user_by_student_id(student_id: str):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM users
            WHERE student_id = %s
        """
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def get_user_by_id(user_id: str):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT *
            FROM users
            WHERE id = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()

#Inserting user details

def create_user(user_data: dict):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO users(
                id,
                student_name,
                student_id,
                college_email,
                password_hash,
                branch,
                academic_session,
                block,
                phone,
                role,
                reputation_score,
                is_verified
            )VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            user_data["id"],
            user_data["student_name"],
            user_data["student_id"],
            user_data["college_email"],
            user_data["password_hash"],
            user_data["branch"],
            user_data["academic_session"],
            user_data["block"],
            user_data["phone"],
            "STUDENT",
            0,
            False
        )
        cursor.execute(query, values)
        connection.commit()

    except Error:
        connection.rollback()
        raise Exception(str(e))

    finally:

        cursor.close()
        connection.close()