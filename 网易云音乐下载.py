import requests
import re
from multiprocessing import Pool
import json
import math
import codecs
import base64
import random
import Crypto
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import urllib
import bs4
url="https://music.163.com/weapi/song/enhance/player/url?csrf_token="
head={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Cookie': 'iuqxldmzr_=32; _ntes_nnid=00683d2723cb1a23b074e99bdb062e35,1553240704274; _ntes_nuid=00683d2723cb1a23b074e99bdb062e35; WM_TID=WO0f0qWdHDVAVQUFUUJ805xwNqUkDA5e; hb_MA-9F44-2FC2BD04228F_source=www.baidu.com; __root_domain_v=.163.com; _qddaz=QD.k77j4t.iutkz6.jtkr0n43; _ga=GA1.2.1422568841.1553300510; _gid=GA1.2.306460327.1553300510; playerid=40624588; WM_NI=ZA9LEgaE7UqTXYQEzzReqMIz3%2BwH%2FdCD93zTI%2FayBDMOgaPKeiOj2Mfktvj9tbj3Jt2oULqqIg%2FYZEjipLT%2BlE63hvLK4GgKCoVAfP0SqO0BHByfyunewJ5EfEZzMhZoQW0%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee90d04d978ea790f73d8c9a8aa3d55a829f8baaf774b1ee8fd4c43dad89a7d6fc2af0fea7c3b92a9a9ff7adc86da39bf9b6f4609c879fa6f97292bbbfaecc72f1f5b9a9ae70819cf7d4f9608bf1af9ac1508f91a982d341a7b7818bb147a6b5bc97e933b8bea6d4c980f2b19badf47b8bb9e1bad94faab7c0add721b09bfad4eb7e9095fca8e64181b19aa2e55cf48dbfb0b34a8c9eb787fc7faebbb9abb84fa69b969bd0649ab19fb8b337e2a3; JSESSIONID-WYYY=dM%5CdXUXOtgTHkhGChpsRlq2wjuonipQ8KF%2FBbRcej5IlqDTwk8fBk1CwPvSXmc%5CwkiIv2RUO%5CtWE1rH%2BiJC3Jx%2FVXX8Dq7G2yQBAmjyBe3ImItUlbrSQe9jxo5%5CRjUP0S%5CHMUXBcaOVIh4qElVPxNO2HrizMB0JuSGUZZXOZbf%5CkwzqD%3A1553316011166',
'Host': 'music.163.com',
'Referer': 'https://music.163.com/',
'Upgrade-Insecure-Requests': '1',
'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',


}
# code={
#     'params':"5qiat%2FQVQ8cGmixhkFzDa%2BsH%2BD5%2FZIUTlWCWi8wGjtWpU%2FzvFy8pSKHoqD6mW%2FGFJpVP%2BGXCf8sDTNruTxuXR4BVjqQRJSM2GjBtmMVEElHmU8BCssiFJ08XnGFlJF3DyyRC364lNaPlDMmQGPKOpw%3D%3D",
#     'encSecKey':"764029cdc4e7671ababe1a87863c579cc65e83631a8fdef287adab20aedd38c4747cb0e31d7c58e28314b26f31de96a8496fa8cbfbedaecafe168c0207a607e1f0367048572e39d96982f5def4dd2ee6d4dbb8590e373edc3f50f6c9483b7823cb632003a94e2b6c26f758a659712f8e0eef4b7665cf67f2a27673e060062f9ev1?csrf_token=	weblog?csrf_token=	3238061746556733.jpg?param=34y34	get?csrf_token=	67e5121d1fca62759ab1f44e50d9ce07.m4a	weblog?csrf_token=	v1?csrf_token=	weblog?csrf_token=	get?csrf_token=	aff3fbcfc35e593432200fdc7e110fe2.m4a	aff3fbcfc35e593432200fdc7e110fe2.m4a	weblog?csrf_token=	v1?csrf_token=	weblog?csrf_token=	weblog?csrf_token=	get?csrf_token=	aff3fbcfc35e593432200fdc7e110fe2.m4a",
# }
code={

}
# d=bytes('{"ids":"[523946593]","br":128000,"csrf_token":""}','utf-8')
# e="010001"
# f="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7",
# g="0CoJUm6Qyw8W8jud"
i = 0
def getsong_id():
    id_url = 'https://music.163.com/artist?id=6452'
    pattern = re.compile('<a href="/song\?id=(\d+)">(.*?)</a>')
    song_id = requests.get(url=id_url, headers=head)
    msg_list = pattern.findall(song_id.text)
    for i in range(20) :
        real_list=msg_list[i][0]
    return    real_list
class wangyiyun():
    def __init__(self):
        self.d=getsong_id()
        self.e='010001'
        self.f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.g="0CoJUm6Qyw8W8jud"
        def get_random_str(self):
            str='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            res=''
            for x in range(16):
                    index=math.floor(random.random()*len(str))
                    res+=str[index]
            return res
        self.i=get_random_str(16)
    def aes_encode(self,text,key):
        iv='0102030405060708'#偏移量
        BS = AES.block_size
        # 加密算法
        pad = lambda s : s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        text=str(pad(text))
        encryptor=AES.new(str.encode(key),AES.MODE_CBC,str.encode(iv))
        msg=encryptor.encrypt(bytes(text,'utf-8'))
        msg=str((base64.encodebytes(msg)),encoding='utf-8')
        return msg
    def get_params(self,id):
        d=str({"ids":"[" + str(id) + "]","br":128000,"csrf_token":""})
        return self.aes_encode(self.aes_encode(d,self.g),self.i)
    def rsa_encode(self,text,pubKey,modulus):
        text=text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs,'x').zfill(256)
    def get_data(self,id):
        # id=getsong_id()
        # params=self.aes_encode(self.d,self.g)
        # params=self.aes_encode(str(params),self.i)
        encseckey=self.rsa_encode(self.i,self.e,self.f)
        return {
            'params':self.get_params(id),
            'encSecKey':encseckey
        }
    def download(self):
        id_url = 'https://music.163.com/artist?id=6452'
        pattern = re.compile('<a href="/song\?id=(\d+)">(.*?)</a>')
        song_id = requests.get(url=id_url, headers=head)
        # soup=bs4.BeautifulSoup(pattern,'lxml')
        # msg=soup.select()通过bs4的属性选择器选取想获取的内容

        msg_list = pattern.findall(song_id.text)
        for i in range(20):
            music_id=msg_list[i][0]
            music_name=msg_list[i][1]
            result = self.get_data(music_id)
            song_url = requests.post(url=url, headers=head, data=result)
            # print(song_url.text)
            pattern=re.compile('http://[\w|/|\.|&|?|=|,|%|:]+')
            msg=pattern.findall(song_url.text)
            msg_real=str(msg).strip("'[,]'")
            if msg_real:
                urllib.request.urlretrieve(msg_real, 'd:/music/' + music_name + '.mp4')
                print('Successfully Download:' + music_name + '.mp4')
            else:
                print('Fail Download:' + music_name + '.mp4')

def main():
    music = wangyiyun()
    music.download()
if __name__ == '__main__':
    main()







