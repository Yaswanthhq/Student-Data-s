
from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yaswanth",
        database="student_db"
    )


# Display the website
@app.route("/")
def home():
    return render_template("index.html")


# Get all students
@app.route("/api/students", methods=["GET"])
def get_students():
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, name, email FROM students ORDER BY id DESC"
        )
        students = cursor.fetchall()

        return jsonify(students)

    except Error:
        app.logger.exception("Could not retrieve students")
        return jsonify({"error": "Could not load students"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Save a new student
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email:
        return jsonify(
            {"error": "Name and email are required"}
        ), 400

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = "INSERT INTO students (name, email) VALUES (%s, %s)"
        cursor.execute(sql, (name, email))
        connection.commit()

        return jsonify({
            "message": "Student registered successfully",
            "id": cursor.lastrowid
        }), 201

    except Error:
        if connection and connection.is_connected():
            connection.rollback()

        app.logger.exception("Could not save student")
        return jsonify({"error": "Could not save student"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)
