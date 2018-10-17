# -*- coding:utf-8 -*-
"""
----------------------------------------------
  File Name:   Test
  Description: 分析评论好评率
  Author:       Mr.Liu
  date:         2018/9/17
-----------------------------------------------
   Change Activity:
                2018/9/17:
-----------------------------------------------
"""
_author_ = 'Mr.Liu'
import happybase
import pandas as pd
import pymysql
import jieba
import jieba.analyse
import matplotlib.pylab as pl


# def Mysql(a,b,c,d,e,f):
#     name = a
#     message = b
#     ping = c
#     number = d
#     link = e
#     comment = f
#     # 打开数据库连接
#     db = pymysql.connect("localhost", "root", "", "book")
#     # 游标
#     cursor = db.cursor()
#     sql = 'insert into book2 (name, message, ping, number, link, comment) VALUES (%s,%s,%s,%s,%s,%s)'
#     cursor.execute(sql, (name, message, ping, number, link, comment))
#     try:
#         db.commit()
#         print('操作成功')
#     except:
#         print('操作失败')
#     # 关闭数据库
#     db.close()


def  Hbase(i,a,b,c,d,e,f):
    s1 = a
    s2 = b
    s3 = c
    s4 = d
    s5 = e
    s6 = f
    connection = happybase.Connection('192.168.247.10')
    t = connection.table('book')
    book = {'cf1:name': s1, 'cf1:message': s2, 'cf1:ping': s3, 'cf1:number': s4,
            'cf1:link': s5, 'cf1:comment': s6}
    t.put(row=str(i), data=book)


def stopwordslist(filepath):
    """
    取出停用词
    :param filepath:停用词文件路径
    :return: 返回停用词之后的列表
    """
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


def seg_sentence(sentence):
    """
    对评论进行停用词处理
    :param sentence: 评论
    :return: 返回处理之后的字符串
    """
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += ''
    x, y = test2(outstr)
    return x, y

def drawLine(x, y):
    """
    把分词处理后的结果以折线图的形式展示
    :param x: 横坐标集合
    :param y: 纵坐标集合
    :return:
    """
    pl.plot(x, y)
    pl.show()


def test2(s):
    """

    :param s: 传过来的字符串
    :return:基于 TF-IDF（term frequency–inverse document frequency） 算法的关键词抽取
    sentence ：为待提取的文本
    topK： 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
    withWeight ： 为是否一并返回关键词权重值，默认值为 False
    allowPOS ： 仅包括指定词性的词，默认值为空，即不筛选
    """
    keywords = jieba.analyse.extract_tags(s, topK=20, withWeight=True, allowPOS=('a', 'd'))
    x = []
    y = []
    sum = 0
    num = 0
    for item in keywords:
        print(item[0], item[1])
        # 不错、有趣、不好、很好、好
        x.append(item[0])
        y.append(item[1])
    return x, y


def test1(k):
    print(k+'.csv')
    data = pd.read_csv(k+'.csv')
    x = []
    y = []
    for i in range(100):
        a = str(data['name'][i])
        b = str(data['messages'][i])
        c = str(data['ping'][i])
        d = str(data['number'][i])
        e = str(data['link'][i])
        f = str(data['comment'][i])
        # s =  '|'.join(jieba.cut(f,cut_all=True))   # 全模式切割
        # Mysql(a, b, c, d, e, f)
        # Hbase(i,a, b, c, d, e, f)
        x, y = seg_sentence(f)
    for i in range(100):
        drawLine(x, y)


def menu():
    print('******'+'请选择类型数据:1、文学  2、流行  3、文化  4、生活  5、经管  6、科技'+'******')
    m = int(input())
    if m == 1:
        k = 'wenxue'
        test1(k)
    if m == 2:
        k = 'liuxing'
        test1(k)
    if m == 3:
        k = 'wenhua'
        test1(k)
    if m == 4:
        k = 'sheghuo'
        test1(k)
    if m == 5:
        k = 'jingguan'
        test1(k)
    if m == 6:
        k = 'keji'
        test1(k)


if __name__ == '__main__':
    menu()
