# coding=utf-8

import os
import tempfile
import time


# 下一步，完成logcat打印与取值，将logcat的执行
# def keywordin(keyword):
#     '''
#     '''
#     cmd1 = 'adb shell "logcat | grep -n %s > /data/local/tmp/AutoTest.log"' % keyword
#     cmd2 = 'adb shell "cat /data/local/tmp/AutoTest.log"'
#     run_cmd = os.popen(cmd1)
#     time.sleep(5)
#     # killpid('logcat')
#     file2str = run_cmd.read()
#     print type(file2str)
#     print file2str
#     if 'AnTuTuBenchmarkInfo' in file2str:
#         if '100%' in file2str:
#             return True
#         else:
#             print 'Test is running.'
#             pass
#     else:
#         print 'Test is not run.'
#         pass

def killpid(keyword):
    print type(keyword)
    cmd = 'adb shell "ps | grep -n %s"' % keyword  # 格式化命令，keyword类型为字符串
    print cmd
    run_cmd = os.popen(cmd)  # 命令执行的结果保存为一个参数，类型为file
    file2str = run_cmd.read()  # 读取file内容，类型str
    # print file2str
    print '-' * 30, 'Contains the process of "%s"' % keyword, '-' * 30  # 分割线
    print file2str  # 打印包含关键字的进程
    str2list = file2str.split('\n')  # 以\n为分割符将字符串转化为列表
    for i in str2list[:-1]:  # 循环将满足条件的结果以空格进行格式化，并删除列表中的空元素
        l = i.split(' ')
        while '' in l:
            l.remove('')
        # print l[1]
        os.popen('adb shell kill %s' % (l[1]))  # kill pid
        print 'Killed %s' % l[1]


# def main():
#     # tmpdir = tempfile.tempdir
#     tmpdir = tempfile.gettempdir()
#     curdir = os.getcwd()
#     print "-"*50
#     # print tmpdir
#     # print curdir
#     pullcmd = 'adb pull /sdcard/.antutu/benchmark/history_scores %s' % curdir
#     print pullcmd
#     time.sleep(5)
#     os.system(pullcmd)
#     print os.system('dir %s' % curdir)


def main():
    from xml.dom.minidom import parse
    import xml.dom.minidom
    xmlfile = r'D:\Workspace\Codespace\UIAutomatorProjects\testcase\2015-10-27 09_57_22.xml'

    tree = xml.dom.minidom.parse(xmlfile)
    collection = tree.documentElement
    if collection.hasAttribute("scores"):
        print "Root element : %s" % collection.getAttribute("shelf")

    # 在集合中获取所有电影
    items = collection.getElementsByTagName("item")

    # 打印每部电影的详细信息
    for item in items:
        print "*****items*****"
        # if item.hasAttribute("memory"):
        #    print "memory: %s" % item.getAttribute("memory")
        smt = item.getElementsByTagName('smt')[0]
        print "Multitask: %s" % smt.childNodes[0].data
        svm = item.getElementsByTagName('svm')[0]
        print "Runtime: %s" % svm.childNodes[0].data
        integer = item.getElementsByTagName('integer')[0]
        print "CPU integer: %s" % integer.childNodes[0].data
        cpufloat = item.getElementsByTagName('float')[0]
        print "CPU float-point: %s" % cpufloat.childNodes[0].data
        ints = item.getElementsByTagName('ints')[0]
        print "Single-thread integer: %s" % ints.childNodes[0].data
        floats = item.getElementsByTagName('floats')[0]
        print "Single-thread float-point: %s" % floats.childNodes[0].data
        memory = item.getElementsByTagName('memory')[0]
        print "RAM Operation: %s" % memory.childNodes[0].data
        sram = item.getElementsByTagName('sram')[0]
        print "RAM Speed: %s" % sram.childNodes[0].data
        score2d = item.getElementsByTagName('score2d')[0]
        print "2D graphics: %s" % score2d.childNodes[0].data
        score3d = item.getElementsByTagName('score3d')[0]
        print "3D graphics: %s" % score3d.childNodes[0].data
        snand = item.getElementsByTagName('snand')[0]
        print "Storage I/O: %s" % snand.childNodes[0].data
        database = item.getElementsByTagName('database')[0]
        print "Database I/O: %s" % database.childNodes[0].data
        score = item.getElementsByTagName('score')[0]
        print "score: %s" % score.childNodes[0].data
        date = item.getElementsByTagName('date')[0]
        print "Test date: %s" % date.childNodes[0].data


if __name__ == '__main__':
    main()
    # killpid('antutu')
