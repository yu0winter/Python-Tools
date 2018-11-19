#!/usr/bin/python
# -*- coding: UTF-8 -*-


# SDK 有两种形式：xxx.framework 、xxx.a
# xxx.framework : lipo -info xxx.framework/xxx
# xxx.a : lipo -info xxx.a
# 输出一个文本文件
# 列名：文件名    指令集    是否支持64位模拟器(x86_64)


# 访问Mac os 系统文件路径
import os

# 匹配的文件类型: 'framework'、'a'

def main():
    print '程序入口';

    str = raw_input("请输入需要检查的目录：")
    checkPath = str.replace(' ','');

    print('文件名    是否支持64位模拟器(x86_64)    指令集')
    detect_walk(checkPath);
    print '程序执行结束';
    pass


def detect_walk(dir_path):

    for root, dirs, files in os.walk(dir_path):

        for dir in dirs:
            suffix = os.path.splitext(dir)[1]

            if suffix=='.framework':
                
                filePath = os.path.join(root,dir) + "/" + dir.split('.')[0]
                checkSDKWithPath(filePath)

        for filename in files:
            suffix = os.path.splitext(filename)[1]
            if suffix == '.a':
                filePath = os.path.join(root,filename)
                checkSDKWithPath(filePath)


def checkSDKWithPath(path):
    # 文件名
    filename = path.split("/")[-1];
    # 指令集
    codeTypes = ""
    # 是否支持模拟器
    supportMac = "支持"

    cmd_lipo = "lipo -info "
    p = os.popen(cmd_lipo + path, 'r')
    log = p.read()
    p.close()

    if log.find('are:') != -1:
        list = log.split('are:')
        if list.count > 1:
            codeTypes = list[-1].replace('\n','')
            isSupport = codeTypes.find('x86_64');
            if isSupport == -1:
                supportMac = "不支持"
    elif log.find('is architecture:') != -1:
        list = log.split('is architecture:')
        if list.count > 1:
            codeTypes = list[-1].replace('\n','')
            isSupport = codeTypes.find('x86_64');
            if isSupport == -1:
                supportMac = "不支持"
    else:
        supportMac = '位置错误'

    if supportMac == "不支持":
        print filename + '\t' + supportMac + '\t[' + codeTypes + ']'

    pass


if __name__ == '__main__':
    main()

