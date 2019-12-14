# -*- coding: utf-8 -*-
import os
import json
from flask import Flask, request,make_response

UPLOAD_FOLDER = r'C:\Users\xieningtao\Desktop\temp'   # 上传路径
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])   # 允许上传的文件类型

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求，两者都满足则返回 true
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/imgUpload', methods=['POST'])
def upload_file():
    if request.method == 'POST':   # 如果是 POST 请求方式
        file = request.files['file']   # 获取上传的文件
        myRespnse = make_response()
        myRespnse.headers["content-type"] = "application/json"
        if file and allowed_file(file.filename):   # 如果文件存在并且符合要求则为 true
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # 保存文件
                myRespnse.data = json.dumps({"code":"100","msg":"图片上传成功"})   # 返回保存成功的信息
        else:
            myRespnse.data =  json.dumps({"code":"-101","msg":"只支持png,jpg,jpeg格式图片"})
        return myRespnse
if __name__ == '__main__':
    app.run(threaded=True)