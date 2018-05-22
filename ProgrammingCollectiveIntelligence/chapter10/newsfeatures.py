#-*- coding:utf-8 -*-

import feedparser
import re
import numpy as np


feedlist=[
          'http://www.foxnews.com/xmlfeed/rss/0,4313,0,00.rss',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,80,00.rss',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,81,00.rss',
          ]

def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0:
            p += c
    return p

def separatewords(text):
    spliter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]

def getarticlewords():
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0
    # 遍历每个订阅源
    for feed in feedlist:
        f = feedparser.parse(feed)

        # 遍历每篇文章
        for e in f.entries:
            # 跳过标题相同的文章
            if e.title in articletitles:
                continue

            # 提取单词
            txt = e.title.encode('utf8') + stripHTML(e.description.encode('utf8'))
            words = separatewords(txt)
            articlewords.append({})
            articletitles.append(e.title)

            # 在allwords和articlewords中增加针对当前单词的计数
            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[ec].setdefault(word, 0)
                articlewords[ec][word] += 1
            ed += 1
    return allwords, articlewords, articletitles


def makematrix(allw, articlew):
    wordvec = []

    # 只考虑那些普通的但又不至于非常普通的单词
    for w, c in allw.items():
        if c > 3 and c < len(articlew) * 0.6:
            wordvec.append(w)

    # 构造单词矩阵
    l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1, wordvec

# 展现特征
def showfeatures(w, h, titles, wordvec, out='features.txt'):
    outfile = file(out, 'w')
    pc, wc = np.shape(h)
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []

    # 遍历所有特征
    for i in range(pc):
        slist = []
        # 构造一个包含单词及其权重数据的列表
        for j in range(wc):
            slist.append((h[i, j], wordvec[j]))
        # 将单词列表倒序排列
        slist.sort()
        slist.reverse()

        # 打印开始的6个元素
        n = [s[1] for s in slist[0:6]]
        outfile.write(str(n) + '\n')
        patternnames.append(n)

        # 构造一个针对该特征的文章列表
        flist = []
        for j in range(len(titles)):
            # 加入文章及其权重数据
            flist.append((w[j, i], titles[j]))
            toppatterns[j].append((w[j, i], i, titles[j]))

        # 将该列表倒序排列
        flist.sort()
        flist.reverse()

        # 显示前3篇文章
        for f in flist[0:3]:
            outfile.write(str(f) + '\n')
        outfile.write('\n')

    outfile.close()

    # 返回模式名称，以供后续使用
    return toppatterns, patternnames

# 以文章的形式呈现
def showarticles(titles, toppatterns, patternnames, out='articles.txt'):
    outfile = file(out, 'w')

    # 遍历所有的文章
    for j in range(len(titles)):
        outfile.write(titles[j].encode('utf8') + '\n')

        # 针对该篇文章，获得排位最靠前的几个特征
        # 并将其倒序排列
        toppatterns[j].sort()
        toppatterns[j].reverse()

        # 打印前3个模式
        for i in range(3):
            outfile.write(str(toppatterns[j][i][0]) + ' ' + str(patternnames[toppatterns[j][i][1]]) + '\n')
        outfile.write('\n')
    outfile.close()

