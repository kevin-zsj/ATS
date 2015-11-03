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

@description: 安兔兔性能跑分测试

@module: AS04.性能跑分

@caselevel: A

"""
import os
import time
# from utilwithoutcylix import CylixUtilTestCase
from util import CylixUtilTestCase

class AS04004AntutuBenchMark(CylixUtilTestCase):
    PRE_INSTALL_JAR = ["apk/AbenchMark.jar"]
    PRE_INSTALL_APK = [("apk/AnTutu_Benchmark.apk", "com"),
                       ("apk/ABenchMark.plugin3d.apk", "com")]

    def test(self):
        # install apk.
        apkpath = '%s/apk/antutu-v5-64bit-plugin.apk' % self.ats_home
        armabi = os.popen('adb shell getprop ro.product.cpu.abi').read()
        print 'k'*30
        print apkpath
        print armabi
        if 'arm64' in armabi:
            os.system('adb install %s' % apkpath)
        print '-'*20, 'done', '-'*20
        # history dir.
        cmd1 = 'adb shell ls /sdcard/.antutu/benchmark/history_scores'
        # clean history dir.
        rmfile = 'adb shell rm -fr /sdcard/.antutu/benchmark/history_scores/*'
        os.system(rmfile)
        # Run uiautomator.
        result = self.device.run_uiautomator("com.softwinner.ABenchMark", "AbenchMark.jar",
                                             class_name="AbenchMark", method_name="testAntutu")
        assert result, "Test is FAILED, AnTutu is not run."
        # Mark start time.
        stime = time.time()
        # loop checking.
        while 1:
            # Mark current time.
            curtime = time.time()
            # print 'Start time:',stime
            # print 'Current time:', curtime
            print 'Rinning time:', curtime-stime
            if curtime - stime > 480:
                # test time above 8 minutes is FAILED.
                assert False, 'Time-outs(above 8min),this test to be completed in 5 minutes.'
            r_cmd1 = os.popen(cmd1)
            file2str = r_cmd1.read()
            # checking XML if exists.
            if 'xml' in file2str:
                cmd2 = 'adb shell "cat /sdcard/.antutu/benchmark/history_scores/*.xml"'
                r_cmd2 = os.popen(cmd2)
                l = r_cmd2.read()
                w1 = l.find('<score>')
                w2 = l.find('</score>')
                # 定位总分结果的位置
                score = l[w1 + 7:w2]
                print 'Total Score:', score
                if int(score) < 17000:
                    self.logger.error("Test is completed, but it is FAILED.")
                    assert False, 'Total score less then spec.'
                else:
                    # Test is PASS, break.
                    break
            else:
                print 'wait 20 sec'
                time.sleep(20)
                continue
