#coding:utf-8
from django.shortcuts import render
from django.views.generic.base import View
import requests
import re
import os,sys, time,shutil
from django.http import HttpResponseRedirect

class IndexView(View):
    def get(self,request):
        cnt=request.GET.get('cnt',0)
        msg=request.GET.get('msg','')
        dir = os.getcwd()
        captchaDir = os.path.join(dir, "static\\captcha\\")
        resultDir = os.path.join(dir, "static\\result\\")
        timeStamp = round(int(time.time() * 1000))
        response = requests.get("http://www.libopac.seu.edu.cn:8080/reader/")
        sessionId = response.headers["Set-Cookie"].split(";")[0]
        headers = {'Cookie': sessionId,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Referer': 'http://www.libopac.seu.edu.cn:8080/reader/login.php'}
        captchaUrl = "http://www.libopac.seu.edu.cn:8080/reader/captcha.php"
        html = requests.get(captchaUrl, headers=headers)
        with open(captchaDir + str(timeStamp) + '.jpg', 'wb') as f:
            f.write(html.content)
        return render(request, 'index.html',{'path':"/static/captcha/" + str(timeStamp) + '.jpg','timeStamp':timeStamp,'sessionId':sessionId,'cnt':cnt,'msg':msg})

    def post(self,request):
        dir = os.getcwd()
        captchaDir = os.path.join(dir, "static\\captcha\\")
        resultDir = os.path.join(dir, "static\\result\\")
        sessionId=request.POST.get("sessionId")
        cnt = request.POST.get("cnt")
        captcha=request.POST.get("captcha")
        timeStamp=request.POST.get("timeStamp")
        user = "1131894367@qq.com"
        pwd = ""
        headers = {'Cookie': sessionId,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                   'Referer': 'http://www.libopac.seu.edu.cn:8080/reader/login.php'}
        data = {"number": user, "passwd": pwd, "captcha": captcha, "returnUrl": "", "select": "email"}
        url = "http://www.libopac.seu.edu.cn:8080/reader/redr_verify.php"
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        response = requests.post("http://www.libopac.seu.edu.cn:8080/reader/redr_info.php", headers=headers, data=data,
                                 allow_redirects=False)
        result = re.search(r"赖敬之", response.text)
        if result:
            cnt=int(cnt)+1
            shutil.copy(captchaDir + str(timeStamp) + '.jpg',resultDir+str(captcha)+'.jpg')
            os.remove(captchaDir + str(timeStamp) + '.jpg')
            return HttpResponseRedirect('/captcha?cnt='+str(cnt))
        else:
            os.remove(captchaDir + str(timeStamp) + '.jpg')
            return HttpResponseRedirect('/captcha?msg="验证码错误"&cnt='+cnt)