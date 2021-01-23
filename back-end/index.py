# index.py
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
import db
import csv_funcs as csv_f

import tensor_funcs as tensor_f

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


def hello():
    print("Hello")


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

    predict_values = make_messages_into_csv_values(req["message"])
    quality_prediction = tensor_f.predict_message(predict_values)
    db.insert_message(req["message"], quality_prediction)
    return {"status": 200}


@app.route("/get_messages")
@cross_origin()
def get_messages():
    db_result = db.get_messages()
    final_result = []
    items_in_result = ["text", "likes", "id"]
    for result in db_result:
        ordered_item = {}

        for item in range(len(items_in_result)):
            ordered_item[items_in_result[item]] = result[item]
            final_item = {
                "message": ordered_item
            }

        final_result.append(final_item)

    return {"messages": final_result}


@app.route("/add_like", methods=["POST"])
@cross_origin()
def add_like():
    req = request.get_json(force=True)
    id = req["id"]
    new_likes = db.get_current_likes(id) + 1
    db.add_like(new_likes, id)
    return {"status": 200}


@app.route("/did_give_like", methods=["POST"])
@cross_origin()
def did_give_like():
    req = request.get_json(force=True)
    print(req["messages"])
    for message in req["messages"]:
        csv_values = make_messages_into_csv_values(message["message"])
        csv_f.add_row(csv_values)

    return {"status": 200}


def make_messages_into_csv_values(message):
    final_values = {}
    final_values["likes"] = message["likes"]
    final_values["message_length"] = len(message["text"])

    if "time_to_like" in message:
        time_to_like = message["time_to_like"]
    else:
        final_values["group"] = 0
        return final_values

    if time_to_like == -1:
        final_values["group"] = 0
    elif time_to_like > 120:
        final_values["group"] = 1
    else:
        final_values["group"] = 2

    return final_values
