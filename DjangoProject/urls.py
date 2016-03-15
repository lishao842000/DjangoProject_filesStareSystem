"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^list$', 'mysite.views.getAttribut'),
    # url(r'^$', 'mysite.views.showHome'),
    # url(r'^filelist$', 'mysite.views.getFilesList'),
    # url(r'^getFileTree$', 'mysite.views.getFilesTree'),
    url(r'^getdata$', 'mysite.views.getdata'),
    # url(r'', include('siteuser.urls')),
    url(r"^createTree$", "mysite.views.createTree"),
    url(r"^updateTree$", "mysite.views.updateTree"),
    url(r'^treeView$', 'mysite.views.treeView'),
    url(r'^get_file_count$', 'mysite.views.getFilesCount'),
    url(r'^filesUpload$', 'mysite.views.filesUpload'),
    url(r'^uploadFiles$', 'mysite.views.uploadFiles'),
    url(r"^$", "mysite.views.home"),
    url(r"^Login.html$", "mysite.views.openLogin"),
    url(r"^Register.html$", "mysite.views.openRegister"),
    url(r"^getVerificationCode$", "mysite.views.getVerificationCode"),
    url(r"^VerificationCode$", "mysite.views.VerificationCode"),
    url(r"^registerUser$", "mysite.views.registerUser"),
    url(r"^checkUser$", "mysite.views.if_exist_user"),
    url(r"^login$", "mysite.views.userLogin"),
    url(r"^removeTreeItem$", "mysite.views.removeTreeItem"),
    url(r"^checkSession$", "mysite.views.checkSession"),
    url(r"^loginOut$", "mysite.views.loginOut"),
    url(r"^expandNode$", "mysite.views.expandNode"),
    url(r"^CollapseNode$", "mysite.views.CollapseNode"),
    url(r"^oprationalRowsData$", "mysite.views.oprationalRowsData"),
    url(r"^node_has_files$", "mysite.views.node_has_files"),
    url(r"^removeFileTo$", "mysite.views.removeFileTo"),
    url(r"^get_max_node_id", "mysite.views.get_max_id"),
    url(r"^move_files_to$", "mysite.views.move_files_to"),
    url(r"^file_download/Files$", "mysite.views.file_download"),
    url(r"^get_accordion_files_count$", "mysite.views.get_accordion_files_count"),
    url(r"^get_files$", "mysite.views.get_files")
]
