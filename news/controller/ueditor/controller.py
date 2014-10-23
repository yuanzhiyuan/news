#!/usr/bin/python
#-*-coding:utf-8-*-

import os.path
import cgi
from flask import Flask, redirect, request, url_for, make_response, json, jsonify
from news import app
root_path = os.path.join(app.root_path)


@app.route('/ueditor/controller', methods=['GET', 'POST'])
def controller():
    """List the uploads."""
    #print request
    action = request.args.get('action', None)
    if action == 'config':
        config_path = os.path.join(app.root_path, 'controller/ueditor/config.json')
        fp = open(config_path, 'r')
        config = json.load(fp)
        fp.close()
        return jsonify(config)
    elif action in ['uploadimage', 'uploadscrawl', 'uploadvideo', 'uploadfile']:
        result = action_upload()
    elif action in ['listimage', 'listfile']:
        result = action_list()
    elif action == 'catchimage':
        result = action_crawler()
    else:
        result = json.dumps({'state': u'请求地址出错'})

    callback = request.args.get('callback', None)
    if callback:
        if callback.isalpha():
            return "%s(%s)" % (cgi.escape(callback), result)
        else:
            return json.dumps({'state': u'callback参数不合法'})
    else:
        return result


def action_upload():
    base64 = "upload"
    config_path = os.path.join(app.root_path, 'controller/ueditor/config.json')
    fp = open(config_path, 'r')
    config = json.load(fp)
    fp.close()
    action = request.args.get('action', None)
    if action == 'uploadimage':
        print '====================='
        config.update({
            "pathFormat": config['imagePathFormat'],
            "maxSize": config['imageMaxSize'],
            "allowFiles": config['imageAllowFiles']
        })
        fieldname = config['imageFieldName']

    elif action == 'uploadscrawl':
        config = {
            "pathFormat": config['scrawlPathFormat'],
            "maxSize": config['scrawlMaxSize'],
            "allowFiles": config['scrawlAllowFiles'],
            "oriName": "scrawl.png"
        }
        fieldname = config['scrawlFieldName']
        base64 = "base64"

    elif action == 'uploadvideo':
        config = {
            "pathFormat": config['videoPathFormat'],
            "maxSize": config['videoMaxSize'],
            "allowFiles": config['videoAllowFiles']
        }
        fieldname = config['videoFieldName']

    else:
    #elif action == 'uploadfile':
        config.update({
            "pathFormat": config['filePathFormat'],
            "maxSize": config['fileMaxSize'],
            "allowFiles": config['fileAllowFiles']
        })
        print config
        fieldname = config['fileFieldName']

    #print config,'==========='
    from uploader import Uploader
    up = Uploader(fieldname, config, base64)
    '''
    /**
     * 得到上传文件所对应的各个参数,数组结构
     * array(
     *     "state" => "",          //上传状态，上传成功时必须返回"SUCCESS"
     *     "url" => "",            //返回的地址
     *     "title" => "",          //新文件名
     *     "original" => "",       //原始文件名
     *     "type" => ""            //文件类型
     *     "size" => "",           //文件大小
     * )
     */

    /* 返回数据 */'''
    return jsonify(up.getFileInfo())


def getfiles(rootdir, exts):
    files = []
    for parent, dirnames, filenames in os.walk(rootdir):
        #for dirname in dirnames:
        #    print 'dirname ' + dirname
        for filename in filenames:
            #print 'filename ' + filename
            for ext in exts:
                if filename.endswith(ext):
                    fullname = os.path.join(parent, filename)
                    info = {
                        'url': fullname[len(root_path):],
                        'mtime': int(os.stat(fullname).st_mtime)}
                    files.append(info)
                    #print fullname
                    break
    return files


def action_list():
    base64 = "upload"
    config_path = os.path.join(app.root_path, 'controller/ueditor/config.json')
    fp = open(config_path, 'r')
    config = json.load(fp)
    fp.close()
    action = request.args.get('action', None)
    if action == 'listfile':
        allowFiles = config['fileManagerAllowFiles']
        listSize = config['fileManagerListSize']
        path = config['fileManagerListPath']
    else:
    #elif action == 'listimage':
        allowFiles = config['imageManagerAllowFiles']
        listSize = config['imageManagerListSize']
        path = config['imageManagerListPath']

    size = int(request.args.get('size', listSize))
    start = int(request.args.get('start', 0))
    end = start + size

    path = root_path + path
    files = getfiles(path, allowFiles)
    #print path, files
    if not len(files):
        return jsonify({
            "state": "no match file",
            "list": {},
            "start": start,
            "total": len(files)
        })

    #length = len(files)
    end = min(end, len(files))
    list = files[start:end]

    result = jsonify({
        "state": "SUCCESS",
        "list": list,
        "start": start,
        "total": len(files)
        })

    return result


def action_crawler():
    config_path = os.path.join(app.root_path, 'controller/ueditor/config.json')
    fp = open(config_path, 'r')
    config = json.load(fp)
    fp.close()

    config = {
        "pathFormat": config['catcherPathFormat'],
        "maxSize": config['catcherMaxSize'],
        "allowFiles": config['catcherAllowFiles'],
        "oriName": "remote.png"
    }
    fieldName = config['catcherFieldName']

    list = []
    source = request.form[fieldName] if request.form.has_key(fieldName) else request.args.get(fieldName, None)

    for imgUrl in source:
        from uploader import Uploader
        item = Uploader(imgUrl, config, "remote")
        info = item.getFileInfo()
        list.append({
            "state": info["state"],
            "url": info["url"],
            "size": info["size"],
            "title": cgi.escape(info["title"]),
            "original": cgi.escape(info["original"]),
            "source": cgi.escape(imgUrl)
        })

    return jsonify({
        'state': 'SUCCESS' if len(list) else 'ERROR',
        'list': list
    })
