#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import json
import sys
import time
from urllib.request import urlopen, quote

# 这个爬虫是获取安居客小区数据(需要header)
import requests
from bs4 import BeautifulSoup
from xpinyin import Pinyin  # 导入拼音模块

importlib.reload(sys)


# 创建一个类，类中有两个函数，分别是获取小区信息的getInfo()和得到小区名称后查询其经纬度的getlnglat()，其中getInfo()会调用getlnglat()函数
class myfirst:
    # 根据小区名称获取经纬度
    def getlnglat(self, address):
        """根据传入地名参数获取经纬度"""
        url = 'http://api.map.baidu.com/geocoder/v2/'
        output = 'json'  # 输出结果可以是json也可以是其他类型
        # 百度秘钥
        ak = 'Q5y8DeotwwHUzAwmBliS9hCE5W6BfpS9'
        add = quote(str(address))  # 有时候quote会出错KeyError，要先把quote里面转成字符串类型
        uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
        # 构建百度地图API查询需要的uri，uri与URL的区别见：https://www.zhihu.com/question/21950864

        # 下面这块代码是为了防止因为请求次数过多而产生的错误：urllib2.URLError: <urlopen error [Errno 10060] >
        # 如果出现该错误，就让程序暂停10秒（time.sleep(10)），继续重新获取该小区的坐标。
        # timeout=30是防止因为网络原因出现延迟错误

        maxNum = 5
        for tries in range(maxNum):
            try:
                req = urlopen(uri, timeout=30)  # 设置timeout30秒，防止百度屏蔽,如果被屏蔽就等30秒
            except:
                if tries < (maxNum - 1):
                    time.sleep(10)
                    continue
                else:
                    print("Has tried %d times, all failed!", maxNum)
                    break

        res = req.read().decode()
        temp = json.loads(res)
        lat = temp['result']['location']['lat']
        lng = temp['result']['location']['lng']
        return lat, lng

    # 获取小区信息的函数
    def getInfo(self, page, fh, city, citypy):
        url = 'https://' + citypy + '.anjuke.com/community/p' + str(page) + '/'
        headers = {  # 由于安居客网站的反爬虫，这里必须要设置header
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'https: // wuhan.anjuke.com / sale /?from=navigation',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        # 以下是解析网页的过程
        bs = BeautifulSoup(response.text, 'html.parser')
        lis = bs.find_all('div', class_='li-itemmod')
        for li in lis:
            infos = li.find_all('div', class_='li-info')
            for info in infos:
                titles = info.find_all('h3')
                for title in titles:
                    strTitle = title.get_text()
                    print(city, page, strTitle)
            li_sides = li.find_all('div', class_='li-side')
            strPrice = '暂无均价'
            for li_side in li_sides:
                ps = li_side.find_all('p')
                for p in ps:
                    strongs = p.find_all('strong')
                    for price in strongs:
                        strPrice = price.get_text()
                        print(strPrice)
                address = city + strTitle  # 在前面加上城市变量，限定查询城市
                try:
                    lat, lng = test.getlnglat(address)
                    print(lat, lng)
                    fh.write(city.strip() + ',' + strTitle.strip() + ',' + str(lat).strip() + ',' + str(
                        lng).strip() + ',' + strPrice.strip() + '\n')
                    # strip()是去掉每行后面的换行符，只有str类型才能用strip()
                except KeyError:  # 处理未知异常
                    print("Get A Error")


if __name__ == '__main__':
    print("开始爬数据，请稍等...")
    start_time = time.time()

    # tup1 = [    #设置元组，循环取元组中的元素
    #         '广州','深圳', '佛山', '东莞', '珠海', '中山', '惠州', '肇庆', '江门', '清远', '汕头','梅州', '河源',
    #          '揭阳', '潮州', '汕尾', '韶关', '阳江', '茂名', '湛江', '云浮'
    # ];
    tup1 = ['广州']
    for i in tup1:
        city = str(i)  # 构建拼音，这样每次就只要改这里的城市名就可以了
        # city = city.encode('utf-8')
        citypy = Pinyin()  # 实例化拼音模块的函数
        citypy = str(citypy.get_pinyin(city, ''))  # 还有其他转换拼音的方法，比如在两个字之间加符号等
        print(citypy)
        stradd = 'C://Users//changhf//Desktop//PycharmProjects//guangdong.txt'

        fh = open(stradd, "a")
        # 输入的文件编码格式必须要与上面type=sys.setdefaultencoding( "utf-8" )一致，即也必须是utf-8
        # for page in range(1, 101):
        for page in range(1, 2):
            test = myfirst()  # 实例化对象
            test.getInfo(page, fh, city, citypy)  # 方法必须由实例调用
        fh.close()
        # time.sleep(3)#爬完一个城市后暂停3秒
    end_time = time.time()
    print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))
