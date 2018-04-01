# -*- coding: utf-8 -*-
from flask import Flask
import pymongo
import logging
import json
from flask import request
app = Flask(__name__)

mongo = pymongo.MongoClient('127.0.0.1', 27017)
db = mongo.xnt

@app.route('/user',methods=['POST',"GET"])
def user():
    if request.method == "POST":
        timestamp = request.form.get("timestamp")
        page_size = request.form.get("page_size")
        return "post timestamp: "+ str(timestamp) + "page_size: " + str(page_size)
    else:
        timestamp = request.args.get("timestamp")
        page_size = request.args.get("page_size")
        return "get timestamp: " + str(timestamp) + "page_size: " + str(page_size)

@app.route('/img',methods=['POST',"GET"])
def get_imgs():
    timestamp = ""
    page_size = 20
    is_refresh = 1
    if request.method == "POST":
        timestamp = str(request.form.get("timestamp"))
        page_size = int(request.form.get("page_size"))
        is_refresh = int(request.form.get("is_refresh"))
    else:
        timestamp = str(request.args.get("timestamp"))
        page_size = int(request.args.get("page_size"))
        is_refresh = int(request.args.get("is_refresh"))

    logging.info("timestamp: "+timestamp+ " page_size: "+str(page_size))
    itemList = []
    if "-1" in timestamp:
        items = db.img_cover.find({}).sort([("timestamp",1)]).limit(page_size)
    else:
        if 1 == is_refresh:
            items = db.img_cover.find({"timestamp":{"$gt" : timestamp}}).sort([("timestamp",1)]).limit(page_size)
        else:
            items = db.img_cover.find({"timestamp":{"$ls" : timestamp}}).sort([("timestamp",-1)]).limit(page_size)
    imgResult = {}
    for item in items:
        # itemList.append(item)
        itemMap = {}

        coverMap = {}

        coverMap["imgUrl"] = item["img_url"][0]
        coverMap["imgLabel"] = item["img_label"][0]

        itemMap["cover"] = coverMap
        itemMap["timestamp"] = item["timestamp"][0]
        itemList.append(itemMap)
    imgResult["imgs"] = itemList
    return json.dumps(imgResult, ensure_ascii=False)


@app.route('/videos',methods=['POST',"GET"])
def get_videos():
    timestamp = ""
    page_size = 20
    is_refresh = 1
    if request.method == "POST":
        timestamp = str(request.form.get("timestamp"))
        page_size = int(request.form.get("page_size"))
        is_refresh = int(request.form.get("is_refresh"))
    else:
        timestamp = str(request.args.get("timestamp"))
        page_size = int(request.args.get("page_size"))
        is_refresh = int(request.args.get("is_refresh"))

    logging.info("timestamp: " + timestamp + " page_size: " + str(page_size))
    if "-1" in timestamp:
        items = db.video.find({}).sort([("timestamp", 1)]).limit(page_size)
    else:
        if 1 == is_refresh:
            items = db.video.find({"timestamp": {"$gt": timestamp}}).sort([("timestamp", 1)]).limit(page_size)
        else:
            items = db.video.find({"timestamp": {"$ls": timestamp}}).sort([("timestamp", -1)]).limit(page_size)
    itemList = []
    videoResult = {}
    for item in items:
        # itemList.append(item)
        itemMap = {}
        itemMap["videoTitle"] = item["video_title"][0]
        itemMap["videoImgUrl"] = item["video_img_url"][0]
        itemMap["videoUrl"] = item["video_url"][0]
        itemMap["videoDuration"] = item["video_duration"][0]
        itemMap["videoLabel"] = item["video_label"][0]
        itemMap["timestamp"] = item["timestamp"][0]
        itemList.append(itemMap)
    videoResult["videos"] = itemList
    return json.dumps(videoResult, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
