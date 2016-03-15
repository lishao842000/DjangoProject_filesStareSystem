# coding:utf8
import hashlib
import os, zipfile, tempfile
import random
import uuid
# from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
# import time
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from DjangoProject.settings import MEDIA_ROOT
from mysite.models import filesTree, filesData, myUser
from django.core import serializers
# from django.http.request import HttpRequest
import json
from django.http import JsonResponse
from DjangoCaptcha import Captcha
import datetime
from django.core.servers.basehttp import FileWrapper
from django.conf.global_settings import MEDIA_ROOT


# Create your views here.
def getAttribut(request):
    ID = request.GET.get('ID')
    return render(request, 'test.html', {'ID': ID})


def getFilesList(request):
    files = filesTree.objects.all()
    return render(request, 'test.html', {'files': files})


def showHome(request):
    return render(request, 'test.html')


def getFilesTree(request):
    data = filesTree.objects.all()
    List = []
    for i in data:
        Dict = {}
        Dict['id'] = i.tree_id
        Dict['pId'] = i.pId
        Dict['name'] = i.name
        Dict['open'] = i.open
        Dict['isParent'] = True
        List.append(Dict)
    mylist = json.dumps(List)
    # print mylist
    return render(request, 'test.html', {'mylist': mylist})


def getdata(request):
    node_array = request.POST.get("fileData")
    user = request.session.get('userName')
    files = []
    alldataObj = []
    node_array = json.loads(node_array)
    for node in node_array:
        data = filesTree.objects.filter(tree_id=node["id"], pId=node["pid"])
        idata = filesData.objects.filter(filetree=data, user=user, fileStatus=1)
        files.extend(idata)
    for i in files:
        allDataJson = {}
        allDataJson['fileName'] = (i.files.name).encode('utf8').split("/")[-1]
        allDataJson['user'] = i.user
        allDataJson['uploadDate'] = (i.uploadDate).strftime("%Y-%m-%d %H:%M:%S")
        if i.ifShare == False:
            ifShare_status = "否"
        else:
            ifShare_status = "是"
        allDataJson['ifShare'] = ifShare_status
        alldataObj.append(allDataJson)
    return JsonResponse(alldataObj, safe=False)


def home(request):
    user = None
    userName = request.session.get("userName")
    if userName:
        user = userName
    return render_to_response("ligerUI_test.html", {"userName": user})


def treeView(request):
    data = [{'id': 1, 'pid': 0, 'text': "文件管理根目录"}]
    userName = request.session.get("userName")
    if userName:
        user = myUser.objects.get(userName=userName)
        treeObj = filesTree.objects.filter(User=user)
        files = filesData.objects.filter(user=user, fileStatus=0)
        for file in files:
            tree_data = treeObj.filter(tree_id=file.filetree.tree_id, pId=file.filetree.pId)
            if len(filesData.objects.filter(filetree=tree_data, fileStatus=1)) > 0:
                break
            treeObj = treeObj.exclude(tree_id=file.filetree.tree_id, pId=file.filetree.pId)
        for node in treeObj:
            nodeDict = {}
            nodeDict["id"] = node.tree_id
            nodeDict["pid"] = node.pId
            nodeDict["text"] = node.name
            nodeDict["isExpand"] = node.open
            data.append(nodeDict)
    data = json.dumps(data)
    return HttpResponse(data)


def getFilesCount(request):
    userName = request.session.get("userName")
    Files = None
    if userName:
        user = myUser.objects.get(userName=userName)
        treeObj = filesTree.objects.filter(User=user)
        totleFile = len(filesData.objects.filter(user=user, fileStatus=1))
        files = [{'id': 1, 'pid': 0, 'filesCount': totleFile}]
        # print treeObj
        for node in treeObj:
            filesCount = {}
            filesCount["id"] = node.tree_id
            filesCount["pid"] = node.pId
            tree = filesTree.objects.filter(tree_id=node.tree_id, pId=node.pId, User=user)

            filesCount['filesCount'] = len(filesData.objects.filter(filetree=tree, fileStatus=1, user=user))
            files.append(filesCount)
        Files = files
        # print Files
        return JsonResponse(Files, safe=False)
    else:
        return JsonResponse([{'id': 1, 'pid': 0, 'filesCount': 0}], safe=False)


def node_has_files(request):
    hasfile = None
    userName = request.session.get("userName")
    if userName:
        id = request.POST.get("id")
        pId = request.POST.get("pid")
        user = myUser.objects.filter(userName=userName)
        # print user
        if id and pId:
            treeObj = filesTree.objects.filter(tree_id=id, pId=pId, User=user)
            treeData = filesData.objects.filter(filetree=treeObj)
            # print "treeData:", treeData
            if len(treeData) == 0:
                hasfile = 'false'
            else:
                hasfile = 'true'
    return HttpResponse(hasfile)


def removeFileTo(request):
    user = request.session.get("userName")
    Uer = myUser.objects.filter(userName=user)
    # oldNode = json.loads(request.POST.get("oldNode"))
    # newNode = json.loads(request.POST.get("newNode"))

    oldNode_id = request.POST.get("oldNode[id]")
    oldNode_pid = request.POST.get("oldNode[pid]")
    newNode_id = request.POST.get('newNode[id]')
    newNode_pid = request.POST.get('newNode[pid]')
    newNode_text = request.POST.get('newNode[text]')
    # print 'oldNone', oldNode_id, oldNode_pid
    # print 'newNode', newNode_id, newNode_pid, newNode_text
    ifUpdate = "false"
    if oldNode_id and oldNode_pid and newNode_id and newNode_pid and newNode_text:
        tree_old = filesTree.objects.filter(tree_id=oldNode_id, pId=oldNode_pid, User=Uer)
        tree_new = filesTree.objects.get(tree_id=newNode_id, pId=newNode_pid, User=Uer)
        # print tree_new, "------>tree_new"
        node_files = filesData.objects.filter(filetree=tree_old)
        node_files.update(filetree=tree_new)
        ifUpdate = "true"
    return HttpResponse(ifUpdate)


def move_files_to(request):
    if request.method == "POST":
        user = request.session.get("userName")
        Uer = myUser.objects.filter(userName=user)
        oldNode_id = request.POST.get("old_node[id]")
        oldNode_pid = request.POST.get("old_node[pid]")
        newNode_id = request.POST.get('new_node[id]')
        files_name = request.POST.get('gride_data')
        newNode_pid = filesTree.objects.get(tree_id=newNode_id, User=Uer).pId
        print newNode_pid, newNode_id
        print oldNode_pid, oldNode_id
        if Uer and oldNode_id and oldNode_pid and newNode_id and files_name and newNode_pid:
            files_name = json.loads(files_name)
            for file_name in files_name:
                _file = "Files/" + file_name["fileName"]
                try:
                    # files_tree = filesData.objects.get(files=_file, user=user).filetree
                    # trees = filesTree.objects.filter(tree_id=files_tree.tree_id, pId=files_tree.pId, User=Uer)
                    tree_new = filesTree.objects.get(tree_id=newNode_id, pId=newNode_pid, User=Uer)
                    tree_old = filesTree.objects.get(tree_id=oldNode_id, pId=oldNode_pid, User=Uer)
                    # print files_tree.tree_id, type(trees), newNode_id
                    # trees.update(tree_id=newNode_id, pId=newNode_pid)
                    print tree_new, tree_old
                    node_files = filesData.objects.filter(filetree=tree_old, files=_file, user=user)
                    node_files.update(filetree=tree_new)

                except Exception, e:
                    print e
                    return HttpResponse("false")
            return HttpResponse("true")


def checkSession(request):
    if request.method == "POST":
        try:
            userName = request.session.get("userName")
            if userName:
                return HttpResponse('true')
            else:
                return HttpResponse('false')
        except:
            return HttpResponse('false')


def get_max_id(request):
    node_id = []
    all_tree_node = filesTree.objects.all()
    for tree_node in all_tree_node:
        node_id.append(tree_node.tree_id)
    max_id = max(node_id)
    return render_to_response(locals())


def createTree(request):  # 前端ajax请求动态创建目录树
    treeDict = {}
    # try:
    userName = request.session.get("userName")
    print "username:" + userName
    if userName:
        id = int(request.POST.get("id"))
        pid = request.POST.get("pid")
        text = request.POST.get("text")
        isExpand = request.POST.get("isExpand")
        # print id, pid, text, isExpand
        user = myUser.objects.get(userName=userName)
        filesTree.objects.create(tree_id=int(id), pId=int(pid), name=text, open=isExpand, User=user)
        treeDict["id"] = id
        treeDict["pid"] = pid
        treeDict["text"] = text
        treeDict["isExpand"] = isExpand
        return JsonResponse(treeDict)


def removeTreeItem(request):
    if request.method == "GET":
        id = int(request.GET.get("id"))
        pid = int(request.GET.get("pid"))
        if_checked = request.GET.get("checked")
        userName = request.session.get("userName")
        user = myUser.objects.get(userName=userName)
        print if_checked
        if id and pid and user:
            if if_checked == "false":
                treeItem = filesTree.objects.get(User=user, tree_id=id, pId=pid)
                if len(filesData.objects.filter(filetree=treeItem, fileStatus=0)) > 0:
                    filesData.objects.filter(filetree=treeItem, fileStatus=1).delete()
                    return JsonResponse({"text": '1'})
                treeItem.delete()
                return JsonResponse({"text": '1'})
            elif if_checked == "true":
                treeItem = filesTree.objects.get(User=user, tree_id=id, pId=pid)
                files = filesData.objects.filter(filetree=treeItem)
                for file in files:
                    file.fileStatus = 0
                    file.save()
                return JsonResponse({"text": '1'})


def updateTree(request):
    userName = request.session.get("userName")
    user = myUser.objects.get(userName=userName)
    id = request.GET.get("id")
    pid = request.GET.get("pid")
    text = request.GET.get("text")
    updateObj = filesTree.objects.filter(User=user, tree_id=int(id), pId=int(pid))
    if len(updateObj) != 0:
        updateObj.update(name=text)
    return JsonResponse({"text": text})


def filesUpload(request):
    return render(request, "filesUpload.html")

@csrf_exempt
def uploadFiles(request):  # 文件上传
    files = request.FILES.getlist("file")
    userName = request.session.get("userName")
    # print userName
    if request.POST.get("treeid") and request.POST.get("treepid") and files and userName:
        id = request.POST.get("treeid")
        pid = request.POST.get("treepid")
        user = myUser.objects.get(userName=userName)
        filetree = filesTree.objects.get(User=user, tree_id=id, pId=pid)
        print filetree
        for i in files:
            filesData.objects.update_or_create(filetree=filetree, files=i, user=userName)
    return render(request, "filesUpload.html")


def openLogin(request):
    return render(request, "Login.html")


def openRegister(request):
    return render(request, "Register.html")


def getVerificationCode(request):
    ca = Captcha(request)
    figures = [2, 3, 4, 5, 6, 7, 8, 9]
    ca.img_width = 103
    ca.img_height = 30
    ca.words = [''.join([str(random.sample(figures, 1)[0]) for i in range(0, 4)])]
    ca.type = 'word'
    # print ca.words
    return ca.display()


def VerificationCode(request):
    _code = request.GET.get("verificationData") or ''
    if not _code:
        return HttpResponse(json.dumps([request]))
    ca = Captcha(request)
    if ca.check(_code):
        result = True
        return HttpResponse(json.dumps(result))
    else:
        result = False
        return HttpResponse(json.dumps(result))


def if_exist_user(request):
    if request.method == "GET":
        userName = request.GET.get("reg_username")
        print userName
        try:
            if len(myUser.objects.filter(userName=userName)) == 0:
                result = True
            else:
                result = False
        except:
            result = False
        return HttpResponse(json.dumps(result))


def registerUser(request):
    # time.sleep(3)
    if request.method == "POST":
        userName = request.POST.get("reg_username")
        password = hashlib.md5(request.POST.get("reg_password") + uuid.UUID(int=(uuid.getnode())).hex[-12:]).hexdigest()
        userEmail = request.POST.get("reg_usermail")
        # print userName, password, userEmail
        myUser.objects.create(userName=userName, password=password, userEmail=userEmail)
    return render(request, "Register.html", {"ok": 1, "userName": userName})


def userLogin(request):
    # expiryTime = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    if request.method == "POST":
        information = ""
        userName = request.POST.get("userName")
        password = request.POST.get("password")
        password = hashlib.md5(password + uuid.UUID(int=(uuid.getnode())).hex[-12:]).hexdigest()
        ifRemember = request.POST.get("checkbox")
        if myUser.objects.filter(userName=userName, password=password):
            request.session['userName'] = userName
            if ifRemember == 'on':
                request.session.set_expiry(7 * 24 * 3600)
            else:
                request.session.set_expiry(0)
            information = "success"

        else:
            information = "您输入的账号或者密码不正确，请重新输入"
        # print information
        return render(request, "Login.html", {"information": information})


def loginOut(request):
    del request.session['userName']
    return render_to_response("ligerUI_test.html")


def expandNode(request):
    id = request.POST.get("id")
    pId = request.POST.get("pid")
    if id and pId:
        obj = filesTree.objects.filter(tree_id=id, pId=pId)
        obj.update(open=True)
        return HttpResponse('')


def CollapseNode(request):
    id = request.POST.get("id")
    pId = request.POST.get("pid")
    if id and pId:
        obj = filesTree.objects.filter(tree_id=id, pId=pId)
        obj.update(open=False)
        return HttpResponse('')


def oprationalRowsData(request):
    userName = request.session.get("userName")
    if request.method == "POST":
        if userName:
            flag = request.POST.get("fileOprational")
            # print flag
            rowsData = request.POST.get("rowsData")
            try:
                for row in json.loads(rowsData):
                    fileName = 'Files/' + row["fileName"]
                    File = filesData.objects.filter(files=fileName, user=userName)
                    if flag == '0':
                        File.update(fileStatus=0)
                    elif flag == '1':
                        File.update(ifShare=True)
                    elif flag == '2':
                        File.update(ifShare=False)
                    elif flag == '4':
                        File.delete()
                    elif flag == '5':
                        File.update(fileStatus=1)
                return HttpResponse("1")
            except Exception, e:
                return HttpResponse("0")

def get_accordion_files_count(request):
    userName = request.session.get("userName")
    if request.method == "POST":
        if userName:
            shared_files = filesData.objects.filter(user=userName, ifShare=True, fileStatus=1)
            others_shared_files = filesData.objects.exclude(user=userName).filter(ifShare=True, fileStatus=1)
            removed_files = filesData.objects.filter(user=userName, fileStatus=0)
            shared_files_count = len(shared_files)
            others_shared_files_count = len(others_shared_files)
            removed_files_count = len(removed_files)
            print shared_files_count, others_shared_files_count, removed_files_count
            return JsonResponse({"shared_files": shared_files_count, "others_shared_files_count": others_shared_files_count, "removed_files_count": removed_files_count}, safe=False)

@csrf_exempt
def file_download(request):
    userName = request.session.get("userName")
    print MEDIA_ROOT
    if request.method == "POST":
        files = request.POST.get("files")
        files = json.loads(files)
        if files and userName:
            media_root = r"C:\DjangoProject\uploadFiles\Files"
            # 创建临时文件
            temp = tempfile.TemporaryFile()
            if len(files) > 1:
                archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
                for File in files:
                    filename = File["fileName"]
                    file_path = os.path.join(media_root, filename)
                    # 遍历用户所选文件，并压缩为zip文件
                    archive.write(file_path)
                archive.close()
                temp.seek(0)
                wrapper = FileWrapper(temp)
                response = HttpResponse(wrapper, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=files.zip'
                response['Content-Length'] = temp.tell()
                return response
            else:
                filename = files[0]["fileName"]
                wrapper = FileWrapper(open(os.path.join(media_root, filename), 'rb'))
                response = HttpResponse(wrapper, content_type='application/octet-stream')
                response['Content-Length'] = os.path.getsize(os.path.join(media_root, filename))
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                return response

def get_files(request):
    userName = request.session.get("userName")
    gride_data = []
    alldataObj = []
    if request.method == "POST":
        opration_flag = int(request.POST.get("opration_flag"))
        # print opration_flag, type(opration_flag)
        if opration_flag == 1:
            data = filesData.objects.filter(ifShare=True, fileStatus=1, user=userName)
            gride_data.extend(data)
        if opration_flag == 2:
            data = filesData.objects.exclude(user=userName).filter(ifShare=True, fileStatus=1)
            gride_data.extend(data)
        if opration_flag == 3:
            data = filesData.objects.filter(fileStatus=0, user=userName)
            gride_data.extend(data)
        for i in gride_data:
            allDataJson = {}
            allDataJson['fileName'] = (i.files.name).encode('utf8').split("/")[-1]
            allDataJson['user'] = i.user
            allDataJson['uploadDate'] = (i.uploadDate).strftime("%Y-%m-%d %H:%M:%S")
            if i.ifShare == False:
                ifShare_status = "否"
            else:
                ifShare_status = "是"
            allDataJson['ifShare'] = ifShare_status
            alldataObj.append(allDataJson)
        print alldataObj
        return JsonResponse(alldataObj, safe=False)




