#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务文本离线检测结果获取接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python text_callback.py
"""
__author__ = 'yidun-dev'
__date__ = '2019/11/27'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib.request as urlrequest
import urllib.parse as urlparse
import json


class TextCallbackAPIDemo(object):
    """文本离线检测结果获取接口示例代码"""
    
    API_URL = "https://as.dun.163yun.com/v3/text/callback/results"
    VERSION = "v3.1"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode("utf8")).hexdigest()

    def check(self):
        """请求易盾接口
        Returns:
            请求结果，json格式
        """
        params = {}
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_signature(params)

        try:
            params = urlparse.urlencode(params).encode()
            request = urlrequest.Request(self.API_URL, params)
            content = urlrequest.urlopen(request, timeout=10).read()
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = TextCallbackAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    
    ret = api.check()

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        if len(resultArray) == 0:
            print("暂时没有人工复审结果需要获取, 请稍后重试!")
        for result in resultArray:
            action: int = result["action"]
            taskId: str = result["taskId"]
            callback: str = result["callback"]
            labelArray: list = result["labels"]
            # for labelItem in labelArray:
            #     label: int = labelItem["label"]
            #     level: int = labelItem["level"]
            #     details: dict = labelItem["details"]
            #     hintArray: list = labelItem["hint"]
            if action == 0:
                print("taskId: %s, callback: %s, 文本人工复审结果: 通过" % (taskId, callback))
            elif action == 2:
                print("taskId: %s, callback: %s, 文本人工复审结果: 不通过, 分类信息如下: %s" % (taskId, callback, labelArray))
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))