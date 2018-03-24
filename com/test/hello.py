# -*- coding: utf-8 -*-
from flask import Flask
import pymongo
import logging
import json
app = Flask(__name__)

mongo = pymongo.MongoClient('127.0.0.1', 27017)
db = mongo.xnt

@app.route('/videos')
def index():
    itemList=[]
    items = db.col.find({})
    videoResult={}
    for item in items:
      # itemList.append(item)
        itemMap={}
        itemMap["videoTitle"]=item["title"][0]
        itemMap["videoDuration"]=item["timeVale"][0]
        if item.has_key("linkTarget"):
            itemMap["videoLabel"] = item["linkTarget"][0]
        itemMap["videoUrl"] = item["linkValue"][0]
        itemMap["videoCover"]=item["imgValue"][0]
        itemList.append(itemMap)
    videoResult["videos"]=itemList;
    return json.dumps(videoResult,ensure_ascii=False)
    # return '<h1>Hello World! this is my first project</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
