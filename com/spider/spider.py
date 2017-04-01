# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from HttpClient import HttpClient
import sys, re, os
from threading import Thread
from Queue import Queue
from time import sleep

q = Queue()  # 图片集url队列
imgCount = 0


class getRosiUrl(HttpClient):  # 一级url爬取类
    def __init__(self):
        self.__pageIndex = 1
        self.__Url = "http://www.5442.com/tag/rosi/"
        self.__refer = 'http://www.5442.com/tag/rosi.html'

# 将爬取的图片集url放入队列
def __getAllPicUrl(self, pageIndex):
    realurl = self.__Url + str(pageIndex) + ".html"
    print realurl
    pageCode = self.Get(realurl, self.__refer)
    type = sys.getfilesystemencoding()
    # print pageCode[0:1666].decode("gb2312",'ignore').encode(type)
    pattern = re.compile('<div.*?title">.*?<span><a href="(.*?)".*?</a>', re.S)
    items = re.findall(pattern, pageCode.decode("gb2312", 'ignore').encode(type))
    for item in items:
        # print item
        global q
        q.put(item)
        # print "放入队列"

# 得到最新页码
def __getNewPage(self):
    pageCode = self.Get("http://www.5442.com/tag/rosi.html", self.__refer)
    type = sys.getfilesystemencoding()
    pattern = re.compile(r'<ul.*?<li .*?pageinfo">(.*?)</li>', re.S)
    newPage = re.search(pattern, pageCode.decode("gb2312", 'ignore').encode(type))
    num = re.search("[0-9]+", newPage.group(1).decode("gb2312", 'ignore').split("/")[0]).group()
    if newPage != None:
        return int(num)
    return 0


def start(self):
    page = self.__getNewPage()
    for i in range(1, page):
        self.__getAllPicUrl(i)


# 图片下载类
class downloadImg(HttpClient):
    def __init__(self):
        self.__pageIndex = 1
        self.__floder = "rosi"
        self.__Url = "http://www.5442.com/meinv/20150904/27058.html"
        self.__refer = 'http://www.5442.com/tag/rosi.html'

    def __getNewPage(self):
        pageCode = self.Get(self.__Url, self.__refer)
        type = sys.getfilesystemencoding()
        pattern = re.compile(r'<ul.*?<li>.*?<a>(.*?)</a></li>', re.S)
        newPage = re.search(pattern, pageCode.decode("gb2312", 'ignore').encode(type))
        if newPage != None: 59
        num = re.search("[0-9]+", newPage.group(1).decode("gb2312", 'ignore').split("/")[0]).group()
        60
        return int(num)
        return 0

 # 得到图片集名称
def __getBookName(self):
    pageCode = self.Get(self.__Url, self.__refer)
    type = sys.getfilesystemencoding()
    pattern = re.compile(r'<h1><a.*?>(.*?)</a>', re.S)
    title = re.findall(pattern, pageCode.decode("gb2312", 'ignore').encode(type))
    if title != None:
        return title[0]
    return "未命名"

 # 得到每页图片url
def __getAllPicUrl(self, pageIndex):
    realurl = self.__Url[:-5] + "_" + str(pageIndex) + ".html"
    pageCode = self.Get(realurl)
    type = sys.getfilesystemencoding()
    pattern = re.compile('<p align="center" id="contents">.*?<a.*?<img src=(.*?) alt=.*?>', re.S)
    items = re.findall(pattern, pageCode.decode("gb2312", 'ignore').encode(type))
    self.__savePics(items, self.__floder)

 # 下载保存图片
def __savePics(self, img_addr, folder):
    for item in img_addr:
        filename = self.__floder + "\\" + item.split('/')[-1][:-1]
        print "正在保存图片：" + filename
        print item[1:-1]
        with open(filename, 'wb') as file:
            img = self.Get(item[1:-1])
            file.write(img)
        global imgCount
        imgCount = imgCount + 1


def start(self):
    while True:
        global q
        self.__Url = q.get()  # 从队列中取出一条图片集url
        title = self.__getBookName()
        self.__floder = os.getcwd() + "\\rosi\\" + title.decode("gb2312", 'ignore')
        isExists = os.path.exists(self.__floder)
        if not isExists:
            type = sys.getfilesystemencoding()
            os.mkdir(self.__floder)

        page = self.__getNewPage() + 1
        for i in range(self.__pageIndex, page):
            self.__getAllPicUrl(i)

        q.task_done()  # 完成一项任务


if __name__ == '__main__':
    isExists = os.path.exists("rosi")  # 创建保存目录
    if not isExists:
        os.mkdir("rosi")
    for i in range(5):  # 新建5个线程 等待队列
        print i
        downImg = downloadImg()
        t = Thread(target=downImg.start)
        t.setDaemon(True)
        t.start()
    rosi = getRosiUrl()
    rosi.start()

    q.join