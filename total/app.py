# 임포트
from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

import datetime
import requests
from bs4 import BeautifulSoup
import boto3


# DB 연동
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client["UserID"]
users = db["users"]
animalsdb = client.animals


# 페이지 연동
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/main')
def main():
   return render_template('main.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/cat')
def cat():
    return render_template('cat.html')
@app.route('/dog')
def dog():
    return render_template('dog.html')

@app.route('/etc')
def etc():
    return render_template('etc.html')

@app.route('/mypage')
def mypage():
   return render_template('mypage.html')


# 로그인
@app.route("/main", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = db.users.find_one({"username": username})
    if user and user["password"] == password:
        return jsonify({"result": "success"})

# 회원 가입
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

# 니 새끼 보기
@app.route("/total.cat", methods=["GET"])
def cat_get():
    cat_list = list(animalsdb.cat.find({}, {'_id': False}))
    return jsonify({'cats': cat_list})

@app.route("/total.dog", methods=["GET"])
def dog_get():
    dog_list = list(animalsdb.dog.find({}, {'_id': False}))
    return jsonify({'dogs': dog_list})

@app.route("/total.etc", methods=["GET"])
def etc_get():
    etc_list = list(animalsdb.etc.find({}, {'_id': False}))
    return jsonify({'etcs': etc_list})

# 마이페이지 업로드
@app.route("/mypage", methods=["GET", "POST"])
def animals_post():
    if request.method == "POST":
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id='AKIA5HIYPCTFPPWPD3SK',
            aws_secret_access_key='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')
        bucket_name = 'animals-image'

        image_file = request.files["image"]
        age = request.form['age']
        category = request.form['category']
        desc = request.form['desc']
        name = request.form['name']
        url = request.form['url']
        save = request.form['save']
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        collection_name = determine_collection()
        collection = animalsdb[collection_name]
        key = f'{collection_name}/{image_file.filename}'


        # Upload the image to S3
        s3.upload_fileobj(image_file, bucket_name, key)

        # Get the URL of the uploaded image
        img_url = f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{key}"

        animal_data = {
            'name': name,
            'desc': desc,
            'category': category,
            'age': age,
            'url': url,
            'save': save,
            'img_url': img_url,
            'date': today,
        }

        collection.insert_one(animal_data)
        return render_template('mypage.html')
    else:
        return render_template("mypage.html")
def determine_collection():
    category = request.form['category']
    if category == "dogs":
        return "dog"
    elif category == "cats":
        return "cat"
    else:
        return "etc"


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)