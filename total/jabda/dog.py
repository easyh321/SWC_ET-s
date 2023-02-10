from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.animals

@app.route('/')
def dog():
    return render_template('dog.html')

@app.route("/total", methods=["GET"])
def dog_get():
    dog_list = list(db.dog.find({}, {'_id': False}))
    return jsonify({'dogs': dog_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)