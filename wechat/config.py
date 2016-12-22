#!/usr/bin/python

import os

Mode = 'DEBUG'
TOKEN = 'weixin'

AppID = 'wxf1cad953c13fccfc'

AppSecret = 'ea181a41a77bbaddd91766214e1fd69f'

FETCH_ACCESS_TOKEN_URL = \
        ('https://api.weixin.qq.com/cgi-bin/token'
        '?grant_type=client_credential&appid=%s&secret=%s')
FETCH_JSAPI_TICKET_URL = \
        'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi'

url ='http://dev.yijiayinong.com/ceshi/'
url1 = 'http://dev.yijiayinong.com/location/'
