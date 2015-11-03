# coding=utf-8
"""
Copyright (c) 2015 - Allwinner Technology Co., Ltd.

@version: 1.0

@author: zhangshuaiju@allwinnertech.com

@prerequisite:
    based on Python 2.7

@usage:
    1) this is the handler for testcase

@Others:
    No

@description: 3DMark性能跑分测试

@module: AS04.性能跑分

@caselevel: A

"""
import os
import time

def test():
    # self.cleanfolder()
    pullfile()
    getdata()
    # Run uiautomator.

def cleanfolder():
    # clean test result folder.
    cmd_clean = 'adb shell rm -fr /sdcard/3DMarkAndroid/*'
    os.system(rmfile)


def pullfile():
    # Pull test result to local temp folder.
    ktmp = './ktmp'
    cmd_pull = 'adb pull /sdcard/3DMarkAndroid/ %s' % ktmp
    os.system(cmd_pull)


def getdata():
    import zipfile

    ktmp = '%s/ktmp' % os.getcwd()
    filesName = []
    print os.walk('./ktmp')
    for root, dirs, files in os.walk(ktmp):
        print 'root:', root
        print 'dirs:', dirs
        print 'files:', files
        for fn in files:
            filesName.append(os.path.join(root, fn))
            # filesName.append(os.path.join(fn))
            # print filesName
    print filesName
    print '='*50
    for f in filesName:
        z = zipfile.ZipFile(f, 'r')
        for i in z.namelist():
            print i
        # z.extractall('./ktemp')
        z.extract('Result.xml', './ktmp')   # 解压指定文件到指定目录
        curtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        os.rename('./ktmp/Result.xml', './ktmp/3DMark_Result_%s.xml' % curtime)

        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        # root = ET.parse('./ktmp/Result.xml')    # 分析XML文件
        root = ET.parse('./ktmp/3DMark_Result_%s.xml' % curtime)
        books = root.findall('results/result')  # 查找所有根目录下的result的子节点

        for book_list in books[1]:  # 对查找后的结果遍历
            print book_list.tag, book_list.text
    import shutil
    shutil.rmtree('./ktmp')
if __name__ == '__main__':
    test()