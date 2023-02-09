from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from flask import redirect
app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client["UserID"]
users = db["users"]

@app.route('/')
def home():
   return render_template('login.html')

@app.route('/main')
def main():
   return render_template('main.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = db.users.find_one({"username": username})
    if user and user["password"] == password:
        return jsonify({"result": "success"})
    else:
        return jsonify({'msg':'로그인에 실패하였습니다. 다시 시도해주세요!'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)