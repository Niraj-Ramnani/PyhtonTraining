from flask import Flask, request, jsonify

app = Flask(__name__)

students = []


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body required"}), 400

    required = ["id", "name", "email"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    for student in students:
        if student["id"] == data["id"]:
            return jsonify({"error": "Student ID already exists"}), 400

    students.append(data)

    return jsonify({
        "message": "Student added successfully",
        "student": data
    }), 201


@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students), 200


@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    for student in students:
        if student["id"] == id:
            return jsonify(student), 200

    return jsonify({"error": "Student not found"}), 404


@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    for student in students:

        if student["id"] == id:

            if "name" in data:
                student["name"] = data["name"]

            if "email" in data:
                student["email"] = data["email"]

            return jsonify({
                "message": "Student updated",
                "student": student
            }), 200

    return jsonify({"error": "Student not found"}), 404


@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    for student in students:

        if student["id"] == id:
            students.remove(student)
            return jsonify({
                "message": "Student deleted"
            }), 200

    return jsonify({"error": "Student not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)