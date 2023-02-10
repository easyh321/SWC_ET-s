from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client["UserID"]
users = db["users"]

@app.route('/')
def home():
   return render_template('signup.html')

@app.route('/login')
def login():
   return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    soyn = request.form.get('soyn')

    # check if username is entered
    if not username:
        return jsonify({"result": "error", "msg": "ID를 입력해주세요."})

    # check if username already exists
    existing_users = db.users.find_one({"username": username})
    if existing_users:
        return jsonify({"msg": "이미 존재하는 ID입니다."})

        # check if nickname is entered
    if not nickname:
        return jsonify({"result": "error", "msg": "사용 가능한 ID입니다. \nNickname을 입력해주세요."})

    existing_users = db.users.find_one({"nickname": nickname})
    if existing_users:
        return jsonify({"msg": "이미 존재하는 Nickname입니다"})

    # check if password is entered
    if not password:
        return jsonify({"result": "error", "msg": "사용 가능한 Nickname입니다. \nPassword를 입력해주세요."})

    if soyn == 'Y':
        user_data = {
            "username": username,
            "nickname": nickname,
            "password": password
        }
        db.users.insert_one(user_data)
        return jsonify({"msg": "회원가입에 성공하였습니다!"})
    else:
        return jsonify({"msg": "중복확인을 해주세요."})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)