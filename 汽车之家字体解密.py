from fontTools.ttLib import TTFont
import re
import requests
from scrapy import Selector
from lxml import etree
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
def deal_font():
    url = 'https://club.autohome.com.cn/bbs/thread/2d8a42404ba24266/77486027-1.html#pvareaid=2199101'
    r = requests.get(url=url, headers=headers).text
    tree = etree.HTML(r)
    text = tree.xpath('//div[@class="tz-paragraph"]//text()')
    # print(text)
    text = ''.join(text)
    # print(text)
    url = 'https:' + re.findall(",url\('(//.*.ttf)'\)", r)[0]
    print(url)
    # print(url)
    world_content = requests.get(url=url).content
    with open('./word.ttf', 'wb') as f :
        f.write(world_content)
    world = TTFont('./word.ttf')
    # 读取响应的映射关系
    uni_list = world['cmap'].tables[0].ttFont.getGlyphOrder()
    # print(uni_list)
    unicode_list = [eval(r"u'\u" + uni[3 :] + "'") for uni in uni_list[1 :]]

    world_list = ["右", "远", "高", "呢", "了", "短", "得", "矮", "多", "二", "大", "一", "不", "近",
                  "是", "着", "五", "三", "九", "六", "少", "好", "上", "七", "和", "很", "十",
                  "四", "左", "下", "八", "小", "坏", "低", "长", "更", "的", "地"]  # # 录入字体文件中的字符。必须要以国际标准的unicode编码
    for i in range(len(unicode_list)) :
        text = text.replace(unicode_list[i], world_list[i])
    print(text)
    # print(unicode_list)
if __name__ == '__main__':
    deal_font()

