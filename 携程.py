import  requests
import execjs
import os
import re
import time
import json
from lxml import etree
os.environ["EXECJS_RUNTIME"]="Node"

headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',

}
headers_cmt = {
    'host': 'hotels.ctrip.com',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    'if-modified-since': 'Thu, 01 Jan 1970 00:00:00 GMT',
    'referer': 'https://hotels.ctrip.com/hotel/5599110.html',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
def get_callback():
    callback = """
           var callback = function() {
           for (var t = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], o = "CAS", n = 0; n < 15; n++) {
               var i = Math.ceil(51 * Math.random());
               o += t[i]
           }
           return o
           };
               """
    a=execjs.compile(callback)
    a=a.call('callback')
    return a
head="""
        var hotel_id = 5599110;
        var site = {};
        site.getUserAgent = function(){};
        var Image = function(){};
        var window = {};
        window.document = {body:{innerHTML:"1"}, documentElement:{attributes:{webdriver:"1"}}, createElement:function(x){return {innerHTML:"1"}}};
        var document = window.document;
        window.navigator = {"appCodeName":"Mozilla", "appName":"Netscape", "language":"zh-CN", "platform":"Win"};
        window.navigator.userAgent = site.getUserAgent();
        var navigator = window.navigator;
        window.location = {};
        window.location.href = "http://hotels.ctrip.com/hotel/5599110.html";
        var location = window.location;
         var navigator = {userAgent:{indexOf: function(x){return "1"}}, geolocation:"1"};
    """
get_callback()


def get_eleven():
    r = requests.get('https://hotels.ctrip.com/domestic/cas/oceanball?callback={0}&_={1}'.format(get_callback(),int(time.time()*1000)),
                     headers=headers)
    text = r.text
    #     # text=r.text
    # text=re.findall('eval(.*)join('')',text)
    # print(text)
    # text='function a(){'+r.text.replace('eval','console.log')+'}'
    text = re.sub('eval', 'return', text)
    a=''
    a=''+head
    b = execjs.compile(text)
    b = b.call('f')
    a += re.sub(';!function', 'function eleven', b)[:-3]  # 去掉最后三个字符

    CAS = 'CAS' + re.findall('CAS(.*)', a)[0]
    b = CAS.split('+')[1]  # 以加号为分割符，将CAS分割，取出列表里的第二个
    c='CAS' + CAS.split('(')[0]
    a = a.replace(CAS, 'return %s' % b) + '}'
    # print(a)
    num = re.findall(' \[32769,26495,32473.*,49,51,107,21734]\*/', a)[0]
    # num = num.split(';')[1]
    a = a.replace(num, '=1);')
    a = execjs.compile(a)
    evelen=a.call('eleven')
    print(evelen)
    return evelen,c


while True:
    try:
        evelen,c=get_eleven()
        break
    except Exception as e:
        # print(e)
        pass

url = ('https://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?')
# print(url)
params = {
    'psid' : '',
    'MasterHotelID' : '5599110',
    'hotel' : '5599110',
    'EDM' : 'F',
    'roomId' : '',
    'IncludeRoom' : '',
    'city' : '2',
    'showspothotel' : 'T',
    'supplier' : '',
    'IsDecoupleSpotHotelAndGroup' : 'F',
    'contrast' : '0',
    'brand' : '1155',
    'startDate' : '2019-04-22',
    'depDate' : '2019-04-23',
    'IsFlash' : 'F',
    'RequestTravelMoney' : 'F',
    'hsids' : '',
    'IsJustConfirm' : '',
    'contyped' : '0',
    'priceInfo' : '-1',
    'equip' : '',
    'filter' : '',
    'productcode' : '',
    'couponList' : '',
    'abForHuaZhu' : '',
    'defaultLoad' : 'T',
    'esfiltertag' : '',
    'estagid' : '',
    'Currency' : '',
    'Exchange' : '',
    'minRoomId' : '0',
    'maskDiscount' : '0',
    'TmFromList' : 'F',
    'th' : '40',
    'RoomGuestCount' : '1,1,0',
    'eleven': evelen,
    'callback': c,
    '_': int(time.time()*1000)}
r = requests.get(url, headers=headers_cmt,params=params)
print(r.text)
text=json.loads(r.text)['html']
print(text)

