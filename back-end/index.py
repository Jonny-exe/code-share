# hello.py
import csv_funcs as csv_f

# import tensor_funcs as tensor_f
import db
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)












@app.route("/")
@cross_origin()
def hello_world():
    return "Hello, World!"


@app.route("/add_row", methods=["POST"])
@cross_origin()
def add_income():
    json = request.get_json()
    csv_f.add_row(dict(json))
    return json, 200


@app.route("/get_current_likes", methods=["POST"])
@cross_origin()
def get_current_likes():
    req = request.get_json(force=True)
    db_result = db.get_current_likes(req["id"])
    print(db_result)
    result = {"current_likes": db_result}
    return result


@app.route("/insert_message", methods=["POST"])
@cross_origin()
def insert_message():
    req = request.get_json(force=True)
    print("req: ", request.get_json())
    if req is None:
        return {"status": 500}
    db.insert_message(req["text"])
    return {"status": 200}


@app.route("/get_messages")
@cross_origin()
def get_messages():
    db_result = db.get_messages()
    final_result = []
    items_in_result = ["text", "likes", "id"]
    for result in db_result:
        final_item = {}

        for item in range(len(items_in_result)):
            final_item[items_in_result[item]] = result[item]

        final_result.append(final_item)

    return {"messages": final_result}


@app.route("/add_like", methods=["POST"])
@cross_origin()
def add_like():
    req = request.get_json(force=True)
    print("req: ", req)
    id = req["id"]
    newLikes = db.get_current_likes(id) + 1
    print(newLikes)
    db.add_like(id, newLikes)
    return {"status": 200}
