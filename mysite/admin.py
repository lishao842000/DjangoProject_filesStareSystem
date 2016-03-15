#coding:utf-8
from django.contrib import admin
from mysite.models import filesTree, filesData, myUser
class userRegister(admin.ModelAdmin):
    fields = ('userName', 'password', 'userEmail')
    list_display = ('userName', 'password', 'userEmail')
class filestree(admin.ModelAdmin):
    fields = ('tree_id', 'pId', 'name', 'open', 'User')
    list_display = ('tree_id', 'pId', 'name', 'get_user')
    list_filter = ('User', )

class files(admin.ModelAdmin):
    fields = ('filetree', 'files', 'user', 'ifShare', "fileStatus")
    list_display = ('get_fileTree_id', 'get_fileTree_pId', 'get_fileTree_name', 'get_fileTree_open', 'files', 'user', 'uploadDate', 'ifShare', 'fileStatus')


admin.site.register(myUser, userRegister)
admin.site.register(filesData, files)
admin.site.register(filesTree, filestree)


