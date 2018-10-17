# -*- coding:utf-8 -*-
"""
----------------------------------------------
  File Name:   book
  Description: 爬取豆瓣书评网
  Author:       Mr.Liu
  date:         2018/9/4
-----------------------------------------------
   Change Activity:
                2018/9/4:
-----------------------------------------------
"""
_author_ = 'Mr.Liu'
import scrapy
import time
import lxml
import urllib.request
from scrapy.http import Request, FormRequest
from Book.items import BookItem
from bs4 import BeautifulSoup
import requests
from PIL import Image
import json
from urllib.parse import quote


class TestBook(scrapy.Spider):
    name = "book"
    allowed_domains = ['douban.com']
    # start_urls = ["https://book.douban.com/"]

    def start_requests(self):  # 该方法必须返回一个可迭代对象。该对象包含了spider用于爬取的第一个Request。当spider启动爬取并且未制定URL时，该方法被调用。meta参数的作用是传递信息给下一个函数,下面start_requests中键‘cookiejar’是一个特殊的键，scrapy在meta中见到此键后，会自动将cookie传递到要callback的函数中。既然是键(key)，就需要有值(value)与之对应，例子中给了数字1，也可以是其他值，比如任意一个字符串。可以理解为：再次刷新网页时不丢失登陆信息？
        return [Request('https://accounts.douban.com/login?', callback=self.parse, meta={'cookiejar': 1})]

    def parse(self, response):
        capt = response.xpath('//div/img[@id="captcha_image"]/@src').extract()  # 获取验证码地址
        url = 'https://accounts.douban.com/login'
        print(capt)
        if len(capt) > 0:  # 判断是否有验证
            print('有验证码')
            local_path = 'capt.jpeg'
            urllib.request.urlretrieve(capt[0], filename=local_path)  # 保存验证码到本地
            print('查看本地验证码图片并输入')
            capt_id = response.xpath('//div/input[@name="captcha-id"]/@value').extract()
            captcha_value = input()  # 验证码
            data = {  # 均从chrome浏览器检查及查看源码抓包来
                'form_email': '1769301398@qq.com',  # 邮箱账号
                'form_password': 'lsy0901.',  # 密码
                'captcha-solution': captcha_value,
                'source': 'None',
                'captcha-id': capt_id,
                'redir': 'https://book.douban.com/tag/?view=type',  # 登陆成功要返回的link，我们返回主页
                'login' : '登录'
            }
        else:
            print('没有验证码')
            data = {
                'form_email': '1769301398@qq.com',  # 账号
                'form_password': 'lsy0901.',  # 密码
                'source': 'index_nav',
                'redir': 'https://book.douban.com/tag/?view=type'
            }
            print('login...')
        return [  # 使用Scrapy抓取网页时，如果想要预填充或重写像用户名、用户密码这些表单字段， 可以使用 FormRequest.from_response() 方法实现
            scrapy.FormRequest.from_response(response,
                                             meta={'cookiejar': response.meta['cookiejar']},
                                             dont_filter=False,
                                             formdata=data,
                                             callback=self.m_parse)
        ]

    def m_parse(self, response):
        print('*********'+"1、类型选择  2、自己搜寻"+'*********')
        n = int(input())
        if n == 1:
            print("1、文学   2、流行   3、文化   4、生活   5、经管   6、科技")
            m = int(input("请选择您喜欢的类型："))
            m_title = '//div[@class="article"]/div[2]/div[' + str(m) + ']/table/tbody/tr/td/a/text()'
            titles = response.xpath(m_title).extract()
            print(titles)
            item = BookItem()
            a = []
            for i, value in enumerate(titles):
                 item['title'] = value  # 每个种类的子分类
                 fulurl = 'https://book.douban.com/tag/' + item['title']  # 子分类的链接
                 item['href'] = fulurl
                 a.append(fulurl)
                 print(i+1, fulurl)
                 time.sleep(1)
            m = int(input("请继续选择您喜欢的种类:"))
            url = a[m-1]
            # print('_____________________'+url)
            yield scrapy.Request(url, callback=self.u_start)
        elif n == 2:
            m = input("请输入你要查询的书名:")
            n = quote(m)
            # https://api.douban.com/v2/book/search?q=
            url = 'https://api.douban.com/v2/book/search?q=' + n
            std = urllib.request.urlopen(url)
            rs = json.loads(std.read())
            s = []
            for i in rs['books']:
                s.append(i['id'])
            # https://book.douban.com/subject/1008145/
            ull = 'https://book.douban.com/subject/' + s[0]
            print(ull)
            yield scrapy.Request(ull, callback=self.u_parse)
        else:
            yield scrapy.Request(response, callback=self.m_parse)

    def u_start(self, response):
        s = '//div[@class="info"]/h2/a/@href'
        ss = response.xpath(s).extract()
        item = BookItem()
        for i in range(0, len(ss)):
            item['mhref'] = ss[i]   # 子分类的链接
            url = item['mhref']
            time.sleep(1)
            yield scrapy.Request(url, callback=self.u_parse)

    def u_parse(self, response):
        time.sleep(1)
        s = response.url
        fulurl = s + '/comments/'
        m_ltitle = '//div[@id="wrapper"]/h1/span/text()'
        # //div[@id="info"]/span/a/text()
        m_lauthor = '//div[@id="info"]/a[1]/text()'
        n_lauthor = '//div[@id="info"]/span/a/text()'
        m_lscore = '//strong/text()'
        m_lnumber = '//div[@class="rating_sum"]/span/a/span/text()'
        m_lbs = '//div[@id="info"]/text()'
        m_lcontent = '//div[@id="link-report"]/div/div/p[1]/text()'
        # //div[@id="link-report"]/*/div/div/p[1]/text()
        n_lcontent = '//div[@id="link-report"]/*/div/div/p[1]/text()'
        ltitles = response.xpath(m_ltitle).extract()      # 标题
        lauthors = response.xpath(m_lauthor).extract()    # 作者
        lscores = response.xpath(m_lscore).extract()      # 评分
        lnumbers = response.xpath(m_lnumber).extract()    # 人数
        lbss = response.xpath(m_lbs).extract()            #出版社
        lcontents = response.xpath(m_lcontent).extract()  # 内容简介
        if len(lauthors) == 0:
            lauthors = response.xpath(n_lauthor).extract()
        if len(lcontents) == 0:
            lcontents = response.xpath(n_lcontent).extract()  # 内容简介
        if len(lcontents) == 0:
            lcontents = ['null']  # 内容简介
        item = BookItem()
        for i in range(0, len(ltitles)):
            item['ltitle'] = ltitles[i]
            item['lauthor'] = lauthors[i]
            item['lscore'] = lscores[i]
            item['lnumber'] = lnumbers[i]
            item['lbs'] = lbss[i+4]
            item['lcontent'] = lcontents[i]
            print('**********'+item['ltitle']+item['lauthor']+item['lscore']+item['lnumber']+item['lbs']+item['lcontent'])
            yield scrapy.Request(fulurl, meta={'item': item}, callback=self.PLk)

    def PLk(self, response):
        time.sleep(1)
        item = response.meta['item']
        m_PL = '//span[@class="short"]/text()'
        PLs = response.xpath(m_PL).extract()
        contents = ""
        for i in range(0, len(PLs)):
            contents += PLs[i] + '*******'     # 加入2个空格在数据库中作区分，后期处理数据一空格切割
        item['PL'] = contents
        yield item












