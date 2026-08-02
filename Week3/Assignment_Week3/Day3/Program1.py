# 1. Student Management CRUD API.
# and
# 3. Add validations for duplicate IDs, email, negative values and required fields

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

students = []

# Email Validation 
EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


# CREATE
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["id", "name", "email"]

    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({"error": f"{field} is required"}), 400

    for student in students:
        if student["id"] == data["id"]:
            return jsonify({"error": "Student ID already exists"}), 400

    if not re.match(EMAIL_REGEX, data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    students.append(data)

    return jsonify({
        "message": "Student added successfully",
        "student": data
    }), 201


# READ ALL
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students), 200


# READ ONE
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    for student in students:
        if student["id"] == id:
            return jsonify(student), 200

    return jsonify({"error": "Student not found"}), 404


# UPDATE
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    for student in students:

        if student["id"] == id:

            if "name" in data:
                student["name"] = data["name"]

            if "email" in data:

                if not re.match(EMAIL_REGEX, data["email"]):
                    return jsonify({"error": "Invalid email format"}), 400

                student["email"] = data["email"]

            return jsonify({
                "message": "Student updated successfully",
                "student": student
            }), 200

    return jsonify({"error": "Student not found"}), 404


# DELETE
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    for student in students:

        if student["id"] == id:
            students.remove(student)

            return jsonify({
                "message": "Student deleted successfully"
            }), 200

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)