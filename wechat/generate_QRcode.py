# -*- coding:utf-8 -*-


# 导入Flask类
import json
import time
import urllib2

from flask import Flask

app = Flask(__name__)

APPID = 'wx7cff827b6bc20e6a'
APPSECRET = 'bbf718718ec0ae228972d20c65c8d926'


# 定义类获取access_token
class Access_Toke(object):
    _access_token = {
        'access_token': '',
        'create_tiem': time.time(),
        'expires_in': None,
    }

    @classmethod
    def get_access_token(cls):
        asc = cls._access_token
        # 如果没有access_token或者超时，就需要重新获取_access_token
        if not asc.get('access_token') or time.time() - asc.get('create_tiem') > asc.get('expires_in'):
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            APPID, APPSECRET)
            response_json_str = urllib2.urlopen(url).read()
            print response_json_str
            response_json_dict = json.loads(response_json_str)
            print response_json_dict
            # 判断是否成功获取
            if response_json_dict.get('errcode'):
                # 获取失败
                raise Exception(response_json_dict.get('errcode'))
            asc['access_token'] = response_json_dict.get('access_token')
            asc['expires_in'] = response_json_dict.get('expires_in')
            asc['create_tiem'] = time.time()
        else:
            return asc.get('access_token')


# 定义视图
@app.route('/<int:code_num>')
def index(code_num):
    url = 'URL: https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % Access_Toke.get_access_token()
    params = {"action_name": "QR_LIMIT_SCENE",
              "action_info": {"scene": {"scene_id": code_num}}}

    response_json_str = urllib2.urlopen(url, data=json.dumps(params)).read()
    response_dict = json.loads(response_json_str)

    ticket = response_dict.get('ticket')
    return '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s">' % ticket


if __name__ == '__main__':
    # 启动应用
    app.run(debug=True)
