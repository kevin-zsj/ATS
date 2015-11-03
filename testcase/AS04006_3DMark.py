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
from utilwithoutcylix import CylixUtilTestCase


class AS040063DMark(CylixUtilTestCase):
    # PRE_INSTALL_JAR = ["apk/AbenchMark.jar"]
    # PRE_INSTALL_APK = [("apk/AnTutu_Benchmark.apk", "com"),
    #                    ("apk/ABenchMark.plugin3d.apk", "com")]

    def test(self):
        # self.cleanfolder()
        self.pullfile()
        self.getdata()
        # Run uiautomator.

    def cleanfolder(slef):
        # clean test result folder.
        cmd_clean = 'adb shell rm -fr /sdcard/3DMarkAndroid/*'
        os.system(rmfile)

    def pullfile(self):
        # Pull test result to local temp folder.
        ktmp = '%s/ktmp' % self.ats_home
        cmd_pull = 'adb pull /sdcard/3DMarkAndroid/ %s' % ktmp
        os.system(cmd_pull)

    def getdata(self):
        import zipfile

        ktmp = '%s/ktmp' % self.ats_home
        filesName = []
        for root, dirs, files in os.walk(ktmp):
            for fn in files:
                # filesName.append(os.path.join(root, fn))
                filesName.append(os.path.join(fn))
        # print filesName

                z = zipfile.ZipFile(fn, 'r')
                curtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
                # for i in z.namelist():
                #     print i
                # z.extractall('./ktemp')
                z.extract('Result.xml', ktmp)   # 解压指定文件到指定目录
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        # root = ET.parse('./ktmp/Result.xml')    # 分析XML文件
        root = ET.parse('%s/Result.xml' % ktmp)
        books = root.findall('results/result')  # 查找所有根目录下的result的子节点

        for book_list in books[1]:  # 对查找后的结果遍历
            print book_list.tag, book_list.text

    def backupdata(self):
        pass

    def debugmail(self):
        import sys

        pass
