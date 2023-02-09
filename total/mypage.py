from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.animals

import requests
from bs4 import BeautifulSoup
import boto3

@app.route('/')
def home():
   return render_template('mypage.html')

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
        animal_type = request.form['animal_type']
        desc = request.form['desc']
        name = request.form['name']
        url = request.form['url']

        collection_name = determine_collection()
        collection = db[collection_name]
        key = f'{collection_name}/{image_file.filename}'


        # Upload the image to S3
        s3.upload_fileobj(image_file, bucket_name, key)

        # Get the URL of the uploaded image
        image_url = f"https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{key}"

        animal_data = {
            'name': name,
            'desc': desc,
            'animal_type': animal_type,
            'age': age,
            'url': url,
            'image_url': img_url,
        }

        collection.insert_one(animal_data)
        return "Animal stored in collection '{}'".format(collection_name)
    else:
        return render_template("mypage.html")
def determine_collection():
    animal_type = request.form['animal_type']
    if animal_type == "dogs":
        return "dog"
    elif animal_type == "cats":
        return "cat"
    else:
        return "etc"

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)