# -*- coding:utf-8 -*-


# 导入Flask类
import hashlib
import time

import xmltodict
from flask import Flask
from flask import request

# 创建应用对象
app = Flask(__name__)

token = 'itcast'


# 定义视图
@app.route('/wechat8010', methods=['POST', 'GET'])
def index():
    # 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
    signature = request.args.get('signature')
    # 时间戳
    timestamp = request.args.get('timestamp')
    # 随机数
    nonce = request.args.get('nonce')
    # 随机字符串
    echostr = request.args.get('echostr')
    # 1）将token、timestamp、nonce三个参数进行字典序排序
    list = [token, timestamp, nonce]
    list.sort()
    # 2）将三个参数字符串拼接成一个字符串进行sha1加密
    list_str = ''.join(list)
    result = hashlib.sha1(list_str).hexdigest()
    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if result == signature:
        if request.method == 'POST':
            # 当普通微信用户向公众账号发消息时，微信服务器将POST消息的XML数据包到开发者填写的URL上
            #'<xml>  <ToUserName>< ![CDATA[toUser] ]></ToUserName>  ' \
            #'<FromUserName>< ![CDATA[fromUser] ]></FromUserName>  ' \
            #'<CreateTime>1348831860</CreateTime>  ' \
            #'<MsgType>< ![CDATA[text] ]></MsgType>  ' \
            #'<Content>< ![CDATA[this is a test] ]></Content>  ' \
            #'<MsgId>1234567890123456</MsgId>  </xml>'
            # 接受xml数据，字符串形式
            xml_str = request.data
            # 将字符串形式转成字典形式并接收文本消息中的字典
            xml_dict = xmltodict.parse(xml_str)
            request_dict = xml_dict.get('xml')
            if request_dict.get('MsgType') == 'text':
                # 需要返回xml格式给用户
                response_dict = {
                    'ToUserName': request_dict.get('FromUserName'),
                    'FromUserName': request_dict,
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': 'hello',
                }
                response_xml_dict = {'xml': response_dict}
                response_xml_str = xmltodict.unparse(response_xml_dict)
                return response_xml_str
            elif request_dict.get('MsgType') == 'voice':
                # 需要返回xml格式给用户
                response_dict = {
                    'ToUserName': request_dict.get('FromUserName'),
                    'FromUserName': request_dict,
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': 'hehe',
                }
                response_xml_dict = {'xml': response_dict}
                response_xml_str = xmltodict.unparse(response_xml_dict)
                return response_xml_str
            elif request_dict.get('MsgType') == 'event':
                if request_dict.get('Event') == 'subscribe':

                    event_key = request_dict.get('EventKey')
                    if event_key:
                        print u'你关注的是%s号推广人员的二维码' % event_key
                    response_dict = {
                        'ToUserName': request_dict.get('FromUserName'),
                        'FromUserName': request_dict,
                        'CreateTime': time.time(),
                        'MsgType': 'text',
                        'Content': u'谢谢关注',
                    }

                    response_xml_dict = {'xml': response_dict}
                    response_xml_str = xmltodict.unparse(response_xml_dict)
                    return response_xml_str
        elif request.method =='GET':
            # 原样返回echostr参数内容，则接入生效，成为开发者成功
            return signature

    else:
        return ''


if __name__ == '__main__':
    # 启动应用
    app.run(debug=True, port=8010)
