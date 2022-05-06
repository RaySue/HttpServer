# -*- coding: utf-8 -*-
import os
import cv2
import time
import json
import base64
import requests
import numpy as np

# 要调用的服务端的地址
alg_url = "http://localhost:8000/iot_det"


# numpy 转 base64
def numpy_to_base64(image_np): 
    data = cv2.imencode('.jpg', image_np)[1]
    image_bytes = data.tobytes()
    image_base4 = base64.b64encode(image_bytes).decode('utf8')
    return image_base4

# base64 转 numpy
def base64_to_numpy(image_base64):
    def base64_to_bytes(image_base64):    
        image_bytes = base64.b64decode(image_base64)
        return image_bytes

    def bytes_to_numpy(image_bytes):    
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        image_np2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        return image_np2
    return bytes_to_numpy(base64_to_bytes(image_base64))



def alg_request(img_dir=None):
    img_path = "/Users/surui/Documents/share1.jpg"
    im = cv2.imread(img_path)
    im = numpy_to_base64(im)

    # 请求的 json
    jsondata = {"id": "000000000066",
                "img": im,
                "token": "09c98662ee2245bd850aa5f49aae9a81",
                "timeStamp": int(time.time())}

    # print(jsondata)
    r = requests.post(alg_url, data=json.dumps(jsondata), headers={"Content-Type": "application/json"})
    ret_info = json.loads(r.text)
    print("alg_request ", ret_info.keys())

    # 处理服务返回内容，比如返回一个图片
    imret = base64_to_numpy(json.loads(r.text)["ret"])
    cv2.imwrite("test.jpg", imret)

if __name__ == '__main__':
    alg_request()
