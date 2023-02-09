from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.animals

@app.route('/')
def etc():
    return render_template('etc.html')

@app.route("/total", methods=["GET"])
def etc_get():
    etc_list = list(db.etc.find({}, {'_id': False}))
    return jsonify({'etcs': etc_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)