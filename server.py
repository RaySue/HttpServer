# -*- coding: utf-8 -*-

import os
import cv2
import base64
import configparser
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define
from tornado.options import options
from tornado.escape import json_decode
import requests
import time
import datetime
import uuid
import numpy as np


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



# 主服务
class IOTHandler(tornado.web.RequestHandler):
    # def __init__():
    # super 加载模型
    #     pass

    def post(self):
        post_args = json_decode(self.request.body)
        print(post_args.keys())
        im = bytes_to_numpy(base64_to_bytes(post_args["img"]))
        # 数据标准化 / 255; -mean; /std
        # 调用模型
        im = im[200:-200, 200:-200,:]

        imb = numpy_to_base64(im)
        print(im.shape)
        # 返回结果
        self.write({"surui":666,'code': 0, 'msg': 'success', 'ret': imb})


def main():
    host = "localhost"
    port = "8000"
    url = "http://%s:%s/iot_det" % (host, port)
    define("host", default=host, help="run on the given host")
    define("port", default=port, help="run on the given port", type=int)
    define("url", default=url, help="run on the given url")
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/%s" % url.split("/")[-1], IOTHandler)],
                                          default_host=options.host)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print('HTTP Server Running @ %s' % url)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()