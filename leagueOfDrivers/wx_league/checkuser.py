from .WXDataCrypt import WXDataCrypt
import requests
import string
import random
import json


#配置文件
from . import config


def decrypt(*userinfo):
    appid,sessionkey,encrypteddata,iv = userinfo
    pc = WXDataCrypt(appid, sessionkey)

    return pc.decrypt(encrypteddata, iv)

def checkdata(code, ecrypteddata, iv):

    appid = 'wx199700fc60c13a4c'
    secret = 'a8f83b60580ab55c9d148f81f2f3fbb2'

    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code"
    v_url = url.format(appid, secret, code)
    try:
        print(v_url)
        req = requests.get(v_url)
        res = req.json()
        print(res)
        print(type(res))
        print(res['session_key'])
        print(res['openid'])
        sessionkey = res['session_key']
        openid = res['openid']

    except Exception as e:
        print('错误原因',e)
        data = {'error':'请求微信服务器错1误'}
        return data

    try:
        v_res = decrypt(appid, sessionkey, ecrypteddata, iv)

    except Exception as e:
        print('解码错误原因',e)
        data = {'error':'解码错误'}
        return data

    if openid != v_res['openId']:
        data = {'error':'用户认证错误'}
        return data

    cookie = gen_cookie(8)
    v_res['cookie'] = cookie
    v_res['openid'] = openid
    v_res['session_key'] = sessionkey
    return v_res

def gen_cookie(k):
    ascii_le = string.ascii_letters
    digits = string.digits

    str_dir = ascii_le + digits
    lst_dir = list(str_dir * 10)

    cookie = ''.join(random.sample(lst_dir,k))

    return cookie
