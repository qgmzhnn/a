import base64
from fontTools.ttLib import TTFont
import re
import requests
import csv
from lxml import etree
# font_face = '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'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
# b = base64.b64decode(font_face)
# with open('猫眼01.ttf', 'wb')as f :
#     f.write(b)
text=''
def get_ttf():
    global  text
    font1 = TTFont('猫眼01.ttf')  # 打开本地字体文件猫眼01.ttf
    obj_list1 = font1.getGlyphNames()[1 :-1]  # 获取所有字符的对象，去除第一个和最后一个
    uni_list1 = font1.getGlyphOrder()[2 :]  # 获取所有编码，去除前2个
    # 手动确认编码和数字之间的对应关系，保存到字典中
    dict = {'uniF848' : '9', 'uniE2A8' : '2', 'uniEA5D' : '8', 'uniE51B' : '4', 'uniE335' : '3', 'uniE42F' : '1',
            'uniF373' : '6', 'uniF649' : '7', 'uniE052' : '5', 'uniE7A3' : '0'}
    while True:
        try:
            r=requests.get(url='https://piaofang.maoyan.com/?ver=normal',headers=headers)
            text=r.text
            font_face=re.findall("base64,(.*)\)",r.text)[0]
            # print(font_face)
            b = base64.b64decode(font_face)
            with open('猫眼02.ttf', 'wb')as f :
                f.write(b)
        except Exception as e:
            pass
        # exit()

        font2 = TTFont('猫眼02.ttf')  # 打开访问网页新获得的字体文件02.ttf
        obj_list2 = font2.getGlyphNames()[1 :-1]
        uni_list2 = font2.getGlyphOrder()[2 :]
        for uni2 in uni_list2 :
            obj2 = font2['glyf'][uni2] # 获取编码uni2在02.ttf中对应的对象

            for uni1 in uni_list1 :
                obj1 = font1['glyf'][uni1]
                if obj1 == obj2 :
                    # print(uni2, dict[uni1])
                    new="&#x" + uni2[3:].lower() + ';'#lower()将字符串内的大写转为小写
                    # print(new)
                    if new in text:
                        # print("ok")
                        text=text.replace(new,dict[uni1])
        tree=etree.HTML(text)
        name=tree.xpath('//ul[@class="canTouch"]')
        with open('猫眼.csv', 'w', newline='') as csv_file :
            csv_writer = csv.writer(csv_file, dialect='excel')
            csv_writer.writerow(["片名", "上映时间", "累计票房", "实时票房", "票房占比", "排片占比", "上座率"])
            for i in name:
                name=str(i.xpath('li[1]/b/text()')[0])
                try:
                    day=str(i.xpath('li[1]/em[1]/text()')[0])
                except:
                    day=str(i.xpath('li[1]/i/text()')[0])
                try :
                    pf=str(i.xpath('li[1]/em[2]/i/text()')[0])
                except:
                    pf = str(i.xpath('li[1]/em/i/text()')[0])
                now_pf=str(i.xpath('li[2]/b/i/text()')[0]+'万元')
                pfzb=str(i.xpath('li[3]/i/text()')[0])
                ppzb=str(i.xpath('li[4]/i/text()')[0])
                go_up=str(i.xpath('li[5]/span[1]/i/text()')[0])
                # print(name,day,pf,now_pf,pfzb,ppzb,go_up)
                csv_file.write("{0},{1},{2},{3},{4},{5},{6}\n".format(name,day,pf,now_pf,pfzb,ppzb,go_up))
        print("Down")
        csv_file.close()
        break
if __name__ == '__main__':
    get_ttf()