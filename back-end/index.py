# hello.py
import csv_funcs as csv_f
# import tensor_funcs as tensor_f
import db
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/add_row", methods=["POST"])
def add_income():
    json = request.get_json()
    csv_f.add_row(dict(json))
    return json, 200


@app.route("/get_current_likes", methods=["POST"])
def get_current_likes():
    req = request.json
    db_result = db.get_current_likes(req["id"])
    print(db_result)
    result = {"current_likes": db_result}
    return result


@app.route("/insert_message", methods=["POST"])
def insert_message():
    req = request.json
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
def add_like():
    req = request.json
    id = req['id']
    newLikes = db.get_current_likes(id) + 1
    print(newLikes)
    db.add_like(id, newLikes)
    return {'status': 200}
