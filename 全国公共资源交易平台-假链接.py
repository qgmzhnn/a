import requests
import execjs
import os
import Crypto
from Crypto.Cipher import AES
import base64
os.environ["EXECJS_RUNTIME"]="Node"
print(execjs.get())
def aes() :
    hh = 'http://ggzy.gzlps.gov.cn:80/xxgkdt/21413.jhtml'
    aa = hh.split('/')
    aaa = len(aa)
    bbb = aa[aaa - 1].split('.')
    ccc = bbb[0]
    key = 'qnbyzzwmdgghmcnm'
    BS = AES.block_size
    # 加密算法
    pad = lambda s : s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    text = str(pad(ccc))
    encryptor = AES.new(str.encode(key), AES.MODE_ECB)
    msg = encryptor.encrypt(bytes(text, 'utf-8'))
    msg = str((base64.encodebytes(msg)), encoding='utf-8')

    return msg


js="""
            function a(){
              var ddd ="%s";
              ddd = ddd.replace(/\//g, "^");
              ddd = ddd.substring(0, ddd.length - 2);
              var bbbb = ddd + '.' + bbb[1];
              aa[aaa - 1] = bbbb;
              var uuu = '';
              for (i = 0; i < aaa; i++) {
              uuu += aa[i] + '/'
              }
              uuu = uuu.substring(0, uuu.length - 1);
              return uuu
        }
"""%aes()
print(js)
#
# ctx=execjs.compile(js)
# href=ctx.call('a')
with open('交易平台.js','r') as f:
    a=f.read()
ctx=execjs.compile(js)
href=ctx.call("a")
print(href)
