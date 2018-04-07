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


@app.route('/macVideos',methods=['POST',"GET"])
def get_mac_videos():
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
        itemMap["videoTitle"] = item["video_title"]
        itemMap["videoImgUrl"] = item["video_img_url"]
        itemMap["videoUrl"] = item["video_url"]
        itemMap["videoDuration"] = item["video_duration"]
        itemMap["videoLabel"] = item["video_label"]
        itemMap["timestamp"] = item["timestamp"]
        itemList.append(itemMap)
    videoResult["videos"] = itemList
    return json.dumps(videoResult, ensure_ascii=False)


@app.route('/saveVideos',methods=['POST'])
def save_videos():
    logging.info("invoke save_videos")
    video_title = ""
    video_img_url = ""
    video_url = ""
    video_duration = ""
    video_label = ""
    timestamp = ""
    item = {}
    if request.method == "POST":
        video_title = str(request.form.get("video_title").encode('utf-8'))
        video_img_url = str(request.form.get("video_img_url").encode('utf-8'))
        video_url = str(request.form.get("video_url").encode('utf-8'))
        video_duration = str(request.form.get("video_duration").encode('utf-8'))
        video_label = str(request.form.get("video_label").encode('utf-8'))
        timestamp = str(request.form.get("timestamp").encode('utf-8'))

        logging.info("title: "+video_title + "img_url: "+video_img_url)
        item["video_title"] = video_title
        item["video_img_url"] = video_img_url
        item["video_url"] = video_url
        item["video_duration"] = video_duration
        item["video_label"] = video_label
        item["timestamp"] = timestamp
        updateAndSaveVideo(item)
        return json.dumps("ok")

    return json.dumps("failed")

def updateAndSaveVideo(item):
    # self.db.img.insert(dict(item))
    result = db.video.find({"video_url": item["video_url"]})
    if result.count() == 0:
        db.video.insert(dict(item))
    else:
        logging.info("this video is exist url: " + item["video_url"])


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
