from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.animals

today = datetime.datetime.now().strftime("%Y-%m-%d")

doc = {
       'category':'etc',
       'nickname':'test03',
       'img_url':'https://animals-image.s3.ap-northeast-2.amazonaws.com/etc/E-003.png',
       'url':'https://www.naver.com',
       'name':'언더더씨',
       'age': '2살',
       'date':today,
       'desc': '우리 더씨 푸른빛 좀 구경하고 가세요~!!',
       'love':777
}

db.etc.insert_one(doc)
