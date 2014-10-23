#!/usr/bin/python
#-*-coding:utf-8-*-

__author__ = 'cf'
import os, stat, time, random, base64, cgi
from flask import Flask, redirect, request, url_for, make_response, json, jsonify
from werkzeug.utils import secure_filename
from controller import root_path

'''
 Created by JetBrains PhpStorm.
 User: taoqili
 Date: 12-7-18
 Time: 上午11: 32
 UEditor编辑器通用上传类
'''


class Uploader():

    '''/**
     * 构造函数
     * @param string $fileField 表单名称
     * @param array $config 配置项
     * @param bool $base64 是否解析base64编码，可省略。若开启，则$fileField代表的是base64编码的字符串表单名
     */'''
    def __init__(self, fileField, config, type="upload"):

        #fileField #文件域名
        self.file = None #文件上传对象
        self.base64 = None #文件上传对象
        self.config = None #配置信息
        self.oriName = None #原始文件名
        self.fileName = None #新文件名
        self.fullName = None #完整文件名,即从当前配置目录开始的URL
        self.filePath = None #完整文件名,即从当前配置目录开始的URL
        self.fileSize = None #文件大小
        self.fileType = None #文件类型
        self.stateInfo = None #上传状态信息,
        self.stateMap = { #上传状态映射表，国际化用户需考虑此处数据的国际化
            0: "SUCCESS", #上传成功标记，在UEditor中内不可改变，否则flash判断会出错
            1: "文件大小超出 upload_max_filesize 限制",
            2: "文件大小超出 MAX_FILE_SIZE 限制",
            3: "文件未被完整上传",
            4: "没有文件被上传",
            5: "上传文件为空",
            "ERROR_TMP_FILE": "临时文件错误",
            "ERROR_TMP_FILE_NOT_FOUND": "找不到临时文件",
            "ERROR_SIZE_EXCEED": "文件大小超出网站限制",
            "ERROR_TYPE_NOT_ALLOWED": "文件类型不允许",
            "ERROR_CREATE_DIR": "目录创建失败",
            "ERROR_DIR_NOT_WRITEABLE": "目录没有写权限",
            "ERROR_FILE_MOVE": "文件保存时出错",
            "ERROR_FILE_NOT_FOUND": "找不到上传文件",
            "ERROR_WRITE_CONTENT": "写入文件内容错误",
            "ERROR_UNKNOWN": "未知错误",
            "ERROR_DEAD_LINK": "链接不可用",
            "ERROR_HTTP_LINK": "链接不是http链接",
            "ERROR_HTTP_CONTENTTYPE": "链接contentType不正确"
        }

        self.fileField = fileField
        self.config = config
        self.type = type
        if type == "remote":
            self.saveRemote()
        elif type == "base64":
            self.upBase64()
        else:
            self.upFile()

        #self.stateMap['ERROR_TYPE_NOT_ALLOWED'] = iconv('unicode', 'utf-8', self.stateMap['ERROR_TYPE_NOT_ALLOWED'])
        self.stateMap['ERROR_TYPE_NOT_ALLOWED'] = self.stateMap['ERROR_TYPE_NOT_ALLOWED']

    '''
    上传文件的主处理方法
    @return mixed
    '''
    def upFile(self):
        file = self.file = request.files[self.fileField]
        if not file:
            self.stateInfo = self.getStateInfo("ERROR_FILE_NOT_FOUND")
            return

        '''if self.file.error:
            self.stateInfo = self.getStateInfo(file['error'])
            return
        elif not os.path.exists(file['tmp_name']):
            self.stateInfo = self.getStateInfo("ERROR_TMP_FILE_NOT_FOUND")
            return
        elif not is_uploaded_file($file['tmp_name']):
            self.stateInfo = self.getStateInfo("ERROR_TMPFILE")
            return'''

        self.oriName = file.filename
        self.fileSize = file.content_length
        self.fileType = self.getFileExt()
        self.fullName = self.getFullName()
        self.filePath = self.getFilePath()
        self.fileName = self.getFileName()
        dirname = os.path.dirname(self.filePath)

        #检查文件大小是否超出限制
        if not self.checkSize():
            self.stateInfo = self.getStateInfo("ERROR_SIZE_EXCEED")
            return

        #检查是否不允许的文件格式
        if not self.checkType():
            self.stateInfo = self.getStateInfo("ERROR_TYPE_NOT_ALLOWED")
            return

        #创建目录失败
        print 'dirname ', dirname
        if not os.path.isdir(dirname):
            os.makedirs(dirname, 0777)
            if not os.path.isdir(dirname):
                self.stateInfo = self.getStateInfo("ERROR_CREATE_DIR")
                return
        elif not (os.stat(dirname).st_mode | stat.S_IWOTH):
            self.stateInfo = self.getStateInfo("ERROR_DIR_NOT_WRITEABLE")
            return

        #移动文件
        print 'filepath ', self.filePath
        self.file.save(self.filePath)
        if not os.path.isfile(self.filePath): #移动失败
            self.stateInfo = self.getStateInfo("ERROR_FILE_MOVE")
        else: #移动成功
            self.stateInfo = self.stateMap[0]

    '''/**
     * 处理base64编码的图片上传
     * @return mixed
     */'''
    def upBase64(self):
        base64Data = request.form[self.fileField]
        img = base64.decodestring(base64Data)

        self.oriName = self.config['oriName']
        self.fileSize = len(img)
        self.fileType = self.getFileExt()
        self.fullName = self.getFullName()
        self.filePath = self.getFilePath()
        self.fileName = self.getFileName()
        dirname = os.path.dirname(self.filePath)

        #检查文件大小是否超出限制
        if not self.checkSize():
            self.stateInfo = self.getStateInfo("ERROR_SIZE_EXCEED")
            return

        #创建目录失败
        if not os.path.isdir(dirname):
            os.makedirs(dirname, 0777)
            if not os.path.isdir(dirname):
                self.stateInfo = self.getStateInfo("ERROR_CREATE_DIR")
                return
        elif not (os.stat(dirname).st_mode | stat.S_IWOTH):
            self.stateInfo = self.getStateInfo("ERROR_DIR_NOT_WRITEABLE")
            return

        #移动文件
        fp = open(self.filePath, 'w')
        fp.write(img)
        if not os.path.isfile(self.filePath): #移动失败
            self.stateInfo = self.getStateInfo("ERROR_WRITE_CONTENT")
        else: #移动成功
            self.stateInfo = self.stateMap[0]

    '''/**
     * 拉取远程图片
     * @return mixed
     */'''
    def saveRemote(self):
        imgUrl = cgi.escape(self.fileField)
        imgUrl = imgUrl.replace("&amp;", "&")

        #http开头验证
        if not imgUrl.startswith("http"):
            self.stateInfo = self.getStateInfo("ERROR_HTTP_LINK")
            return
        '''
        #获取请求头并检测死链
        heads = get_headers(imgUrl)
        if (!(stristr($heads[0], "200") && stristr($heads[0], "OK"))) {
            self.stateInfo = self.getStateInfo("ERROR_DEAD_LINK");
            return;

        //格式验证(扩展名验证和Content-Type验证)
        $fileType = strtolower(strrchr($imgUrl, '.'));
        if (!in_array($fileType, self.config['allowFiles']) || stristr($heads['Content-Type'], "image")) {
            self.stateInfo = self.getStateInfo("ERROR_HTTP_CONTENTTYPE");
            return;
        }

        //打开输出缓冲区并获取远程图片
        ob_start();
        $context = stream_context_create(
            array('http' => array(
                'follow_location' => false // don't follow redirects
            ))
        );
        readfile($imgUrl, false, $context);
        $img = ob_get_contents();
        ob_end_clean();
        preg_match("/[\/]([^\/]*)[\.]?[^\.\/]*$/", $imgUrl, $m);

        self.oriName = $m ? $m[1]:"";
        self.fileSize = strlen($img);
        self.fileType = self.getFileExt();
        self.fullName = self.getFullName();
        self.filePath = self.getFilePath();
        self.fileName = self.getFileName();
        $dirname = dirname(self.filePath);

        //检查文件大小是否超出限制
        if (!self.checkSize()) {
            self.stateInfo = self.getStateInfo("ERROR_SIZE_EXCEED");
            return;
        }

        //创建目录失败
        if (!file_exists($dirname) && !mkdir($dirname, 0777, true)) {
            self.stateInfo = self.getStateInfo("ERROR_CREATE_DIR");
            return;
        } else if (!is_writeable($dirname)) {
            self.stateInfo = self.getStateInfo("ERROR_DIR_NOT_WRITEABLE");
            return;
        }

        //移动文件
        if (!(file_put_contents(self.filePath, $img) && file_exists(self.filePath))) { //移动失败
            self.stateInfo = self.getStateInfo("ERROR_WRITE_CONTENT");
        } else { //移动成功
            self.stateInfo = self.stateMap[0];
        }'''


    '''/**
     * 上传错误检查
     * @param $errCode
     * @return string
     */'''
    def getStateInfo(self,errCode):
        return self.stateMap[errCode] if self.stateMap[errCode] else self.stateMap["ERROR_UNKNOWN"]

    '''/**
     * 获取文件扩展名
     * @return string
     */'''
    def getFileExt(self):
        return self.oriName[self.oriName.rfind('.'):].lower()
        #return strtolower(strrchr(self.oriName, '.'))

    '''/**
     * 重命名文件
     * @return string
     */'''
    def getFullName(self):
        #替换日期事件
        t = str(int(time.time()))
        d = time.strftime("%Y-%y-%m-%d-%H-%M-%S").split('-')
        format = self.config["pathFormat"]
        format = format.replace("{yyyy}", d[0])
        format = format.replace("{yy}", d[1])
        format = format.replace("{mm}", d[2])
        format = format.replace("{dd}", d[3])
        format = format.replace("{hh}", d[4])
        format = format.replace("{ii}", d[5])
        format = format.replace("{ss}", d[6])
        format = format.replace("{time}", t)

        #过滤文件名的非法自负,并替换文件名
        oriName = self.oriName[:self.oriName.rfind('.')]
        oriName = secure_filename(oriName)
        format = format.replace("{filename}", oriName)

        #替换随机字符串
        randNum = str(random.randint(1, 10000000000))+str(random.randint(1, 10000000000))
        for i in range(1, 12):
            format = format.replace("{rand:%d}" % i, randNum[:i])

        ext = self.getFileExt()
        return format + ext


    '''/**
     * 获取文件名
     * @return string
     */'''
    def getFileName(self):
        return self.filePath[self.filePath.rfind('/')+1:]

    '''/**
     * 获取文件完整路径
     * @return string
     */'''
    def getFilePath(self):
        fullname = self.fullName
        rootPath = root_path

        if not fullname.startswith('/'):
            fullname = '/' + fullname

        return rootPath + fullname

    '''/**
     * 文件类型检测
     * @return bool
     */'''
    def checkType(self):
        return self.getFileExt() in self.config["allowFiles"]

    '''/**
     * 文件大小检测
     * @return bool
     */'''
    def checkSize(self):
        return self.fileSize <= (self.config["maxSize"])

    '''/**
     * 获取当前上传成功文件的各项信息
     * @return array
     */'''
    def getFileInfo(self):
        return {
            "state": self.stateInfo,
            "url": self.fullName,
            "title": self.fileName,
            "original": self.oriName,
            "type": self.fileType,
            "size": self.fileSize
        }
