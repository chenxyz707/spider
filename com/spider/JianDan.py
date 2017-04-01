# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from HttpClient import HttpClient
import sys,re,os
class JianDan(HttpClient):
    def __init__(self):
        self.__pageIndex = 1500 #之前的图片被煎蛋吞了
        self.__Url = "http://jandan.net/ooxx/"
        self.__floder = "jiandan"
    def __getAllPicUrl(self,pageIndex):
        realurl = self.__Url + "page-" + str(pageIndex) + "#comments"
        pageCode = self.Get(realurl)
        type = sys.getfilesystemencoding()
        pattern = re.compile('<p>.*?<a .*?view_img_link">.*?</a>.*?<img src="(.*?)".*?</p>',re.S)
        items = re.findall(pattern,pageCode.decode("UTF-8").encode(type))
        for item in items:
            print item
        self.__savePics(items,self.__floder)

    def __savePics(self,img_addr,folder):
        for item in img_addr:
            filename = item.split('/')[-1]
            print "正在保存图片：" + filename
            with open(filename,'wb') as file:
                img = self.Get('http:' + item)#item=//ww2.sinaimg.cn/mw600/006b7bQngw1euu3paqgi3j30qo0zk482.jpg
                file.write(img)

    def __getNewPage(self):
        pageCode = self.Get(self.__Url)
        type = sys.getfilesystemencoding()
        pattern = re.compile(r'<div .*?cp-pagenavi">.*?<span .*?current-comment-page">\[(.*?)\]</span>',re.S)
        newPage = re.search(pattern,pageCode.decode("UTF-8").encode(type))
        print pageCode.decode("UTF-8").encode(type)
        if newPage != None:
            return newPage.group(1)
        return 1500

    def start(self):
        isExists=os.path.exists(self.__floder)#检测是否存在目录
        print isExists
        if not isExists:
            os.mkdir(self.__floder)
        os.chdir(self.__floder)
        page = int(self.__getNewPage())
        for i in range(self.__pageIndex,page):
            self.__getAllPicUrl(i)

if __name__ == '__main__':
    jd = JianDan()
    jd.start()

JianDan