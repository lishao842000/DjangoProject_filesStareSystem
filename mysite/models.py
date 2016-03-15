#coding:utf8
from django.db import models
import os
from django.db.models.signals import post_delete

class myUser(models.Model):
    userName = models.CharField(max_length=10, verbose_name="用户名", null=False)
    password = models.CharField(max_length=100, verbose_name="登陆密码", null=False)
    userEmail = models.EmailField(null=False, verbose_name="电子邮件")
    def __unicode__(self):
        return self.userName



class filesTree(models.Model):
    User = models.ForeignKey(myUser)
    tree_id = models.IntegerField(null=False)
    pId = models.IntegerField(null=False)
    name = models.CharField(max_length=30)
    open = models.BooleanField(default=False)
    def get_user(self):
        return self.User.userName
    def __unicode__(self):
        # return "%d   %d   %s   %r " % (self.id, self.pId, self.name, self.open)
        return str(self.tree_id)
    get_user.short_description = "User"

class filesData(models.Model):
    filetree = models.ForeignKey(filesTree)
    user = models.CharField(max_length=10)
    files = models.FileField(upload_to="Files")
    uploadDate = models.DateTimeField(verbose_name='文件上传日期', auto_now_add=True)
    ifShare = models.BooleanField(default=False)
    fileStatus = models.IntegerField(default=1)

    def get_fileTree_id(self):
        return self.filetree.tree_id
    def get_fileTree_pId(self):
        return self.filetree.pId
    def get_fileTree_name(self):
        return self.filetree.name
    def get_fileTree_open(self):
        return self.filetree.open
    def __unicode__(self):
        return self.files.url
    get_fileTree_id.short_description = 'id'
    get_fileTree_pId.short_description = 'pId'
    get_fileTree_name.short_description = 'name'
    get_fileTree_open.short_description = 'open'
#后台删除fileData数据时，同时删除对应文件
def delete_file(sender, **kwargs):
        patch = kwargs['instance']
        os.remove(patch.files.path)
post_delete.connect(delete_file, sender=filesData)


