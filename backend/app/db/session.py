""""Purpose:
Create database connection.

Responsibilities:
create database engine
create database session
handle session lifecycle

---> All database operations will use this session."""

import mysql.connector
from mysql.connector import Error

from app.config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


BASE_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
}

DB_CONFIG = {
    **BASE_CONFIG,
    "database": DB_NAME,
}


def create_database():

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**BASE_CONFIG)
        cursor = connection.cursor()

        cursor.execute(
            f"""
            CREATE DATABASE IF NOT EXISTS {DB_NAME}
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci;
            """
        )

        print(f"Database '{DB_NAME}' is ready.")

    except Error as e:
        print(f"Database Creation Error: {e}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def create_tables():
    """
    Creates all project tables.
    """

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id CHAR(36) PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            student_id VARCHAR(30) UNIQUE NOT NULL,
            college_email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            branch VARCHAR(50),
            academic_session VARCHAR(20),
            block VARCHAR(20),
            phone VARCHAR(20),
            role ENUM('STUDENT','ADMIN') DEFAULT 'STUDENT',
            reputation_score INT DEFAULT 0,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id CHAR(36) PRIMARY KEY,

            category_name VARCHAR(50) UNIQUE NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id CHAR(36) PRIMARY KEY,

            user_id CHAR(36) NOT NULL,

            report_type ENUM('LOST','FOUND') NOT NULL,

            category_id CHAR(36),

            title VARCHAR(150) NOT NULL,

            description TEXT,

            location VARCHAR(255),

            date_time DATETIME,

            image_url VARCHAR(255),

            status ENUM(
                'ACTIVE',
                'MATCHED',
                'CLAIMED',
                'CLOSED'
            ) DEFAULT 'ACTIVE',

            visibility ENUM(
                'PUBLIC',
                'PRIVATE'
            ) DEFAULT 'PUBLIC',

            importance ENUM(
                'LOW',
                'MEDIUM',
                'HIGH'
            ) DEFAULT 'MEDIUM',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (category_id)
                REFERENCES categories(id)
                ON DELETE SET NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id CHAR(36) PRIMARY KEY,

            report_id CHAR(36) NOT NULL,

            claimer_id CHAR(36) NOT NULL,

            proof_description TEXT,

            proof_image VARCHAR(255),

            status ENUM(
                'PENDING',
                'APPROVED',
                'REJECTED'
            ) DEFAULT 'PENDING',

            admin_note TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (report_id)
                REFERENCES reports(id)
                ON DELETE CASCADE,

            FOREIGN KEY (claimer_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id CHAR(36) PRIMARY KEY,

            user_id CHAR(36) NOT NULL,

            title VARCHAR(255),

            message TEXT,

            is_read BOOLEAN DEFAULT FALSE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        );
        """)

        connection.commit()

        print("All tables are ready.")

    except Error as e:
        print(f"Table Creation Error: {e}")

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_connection():
    """
    Returns a new database connection.
    """

    return mysql.connector.connect(**DB_CONFIG)


def initialize_database():
    """
    Call this once when the application starts.
    """

    create_database()
    create_tables()