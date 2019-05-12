import requests
import json
import time
import  re
from  lxml import etree
import execjs

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer': 'https://xin.baidu.com/detail/compinfo?pid=xlTM-TogKuTwvxosgH5poHE*cNI4uVFPdAmd&tab=basic',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}
def mix(tk,bid):

    return tk[0:len(tk)-len(bid)]
def get_data():
    url='https://xin.baidu.com/detail/compinfo?pid=xlTM-TogKuTwvxosgH5poHE*cNI4uVFPdAmd&tab=basic'
    r=requests.get(url=url,headers=headers)
    tk=str(re.findall('var tk = document.getElementById\(\'(.*?)\'\).getAttribute\(\'(.*?)\'\);',r.text))
    baiducode=re.findall('id="baiducode">(.*?)<',r.text)[0]
    print(baiducode)
    r2=tk.split(",")[1].replace(')]','').replace("'",'')
    text=str(re.findall(r2+'="(.*?)"',r.text)[0])
    js='''
                function mix(tk, bid) {
                    var tk = tk.split("").reverse().join("");
                    return tk.substring(0, tk.length - bid.length);
                }
    
    '''
    ctx=execjs.compile(js)
    tot=ctx.call('mix',text,baiducode)
    print(tot)
    url='https://xin.baidu.com/detail/basicAjax?pid=xlTM-TogKuTwvxosgH5poHE*cNI4uVFPdAmd&tot={0}&_={1}'.format(tot,int(time.time()*1000))
    r=requests.get(url=url,headers=headers)
    data=json.loads(r.content.decode('unicode-escape'))['data']
    data={
        '审核/年检时间':data['annualDate'],
        '登记机关':data['authority'],
        '注册资本':data['regCapital'],
        '法定代表人':data['legalPerson'],
        '企业类型':data['entType'],
        '所属行业':data['industry'],
        '所在地址':data['regAddr'],
        '经营范围':data['scope']
    }
    print(json.dumps(data,indent=1,ensure_ascii=False))
if __name__ == '__main__':
    get_data()



