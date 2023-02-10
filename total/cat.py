from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.animals

@app.route('/')
def cat():
    return render_template('cat.html')

@app.route("/total", methods=["GET"])
def cat_get():
    cat_list = list(db.cat.find({}, {'_id': False}))
    return jsonify({'cats': cat_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
