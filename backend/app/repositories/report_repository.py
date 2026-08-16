from uuid import uuid4
from app.db.session import get_connection


def create_report(user_id: str,report_data: dict):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        report_id = str(uuid4())
        query = """
            INSERT INTO reports (
                id,
                user_id,
                report_type,
                category_id,
                title,
                description,
                location,
                date_time,
                image_url,
                visibility,
                importance)
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s)"""
        values = (
            report_id,
            user_id,
            report_data["report_type"],
            report_data["category_id"],
            report_data["title"],
            report_data.get("description"),
            report_data.get("location"),
            report_data.get("date_time"),
            report_data.get("image_url"),
            report_data["visibility"],
            report_data["importance"],
        )
        cursor.execute(query, values)
        connection.commit()

        return report_id

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

from mysql.connector import Error
from uuid import uuid4

from app.db.session import get_connection


def get_category_by_id(category_id: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id, category_name
            FROM categories
            WHERE id = %s
        """
        cursor.execute(query, (category_id,))

        return cursor.fetchone()

    except Error as e:
        print(f"Database Error: {e}")
        raise Exception(str(e))

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def find_duplicate_report(user_id: str,report_data: dict):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT id
            FROM reports
            WHERE user_id = %s
              AND report_type = %s
              AND category_id = %s
              AND LOWER(TRIM(title)) = LOWER(TRIM(%s))
              AND (
                    location = %s
                    OR (location IS NULL AND %s IS NULL)
                  )
              AND (
                    date_time = %s
                    OR (date_time IS NULL AND %s IS NULL)
                  )
              AND status = 'ACTIVE'
            LIMIT 1
        """
        values = (
            user_id,
            report_data["report_type"],
            report_data["category_id"],
            report_data["title"],
            report_data.get("location"),
            report_data.get("location"),
            report_data.get("date_time"),
            report_data.get("date_time"),
        )
        cursor.execute(query, values)

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()