# 3. Secure Notes API accessible only by authenticated owners.
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "secret"

jwt = JWTManager(app)



users = [

    {
        "id":1,
        "username":"Rahul"
    },

    {
        "id":2,
        "username":"Amit"
    }

]


notes = []


@app.route("/login/<int:id>")
def login(id):

    for user in users:

        if user["id"] == id:

            token = create_access_token(
                identity=user["id"]
            )


            return jsonify({

                "token":token

            })



    return jsonify({

        "error":"User not found"

    }),404



@app.route("/notes", methods=["POST"])
@jwt_required()
def create_note():

    user_id = get_jwt_identity()

    data = request.get_json()


    note = {

        "id":len(notes)+1,

        "owner_id":user_id,

        "title":data["title"],

        "content":data["content"]

    }


    notes.append(note)


    return jsonify(note),201


@app.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():

    user_id = get_jwt_identity()


    user_notes = []


    for note in notes:

        if note["owner_id"] == user_id:

            user_notes.append(note)



    return jsonify(user_notes)



@app.route("/notes/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_note(id):

    user_id = get_jwt_identity()


    for note in notes:


        if note["id"] == id:


            if note["owner_id"] != user_id:

                return jsonify({

                    "error":"Not your note"

                }),403



            notes.remove(note)


            return jsonify({

                "message":"Deleted"

            })



    return jsonify({

        "error":"Note not found"

    }),404



if __name__ == "__main__":
    app.run(debug=True)