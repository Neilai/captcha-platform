#coding:utf-8
__author__ = "Neil"
__time__ = "2018/3/22 10:39"
import requests
import re
import  os,sys,time
dir=os.getcwd()
captchaDir=os.path.join(dir,"captcha\\")
timeStamp=round(int(time.time()*1000))
session=requests.session()
url="http://www.libopac.seu.edu.cn:8080/reader/redr_verify.php"
captchaUrl="http://www.libopac.seu.edu.cn:8080/reader/captcha.php"
user="1131894367@qq.com"
pwd="Wo19971008"
html = session.get(captchaUrl)
with open(captchaDir+str(timeStamp)+'.jpg', 'wb') as f:
    f.write(html.content)
captcha=input("输入验证码：")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36','Referer':'http://www.libopac.seu.edu.cn:8080/reader/login.php'}
data={"number":user,"passwd":pwd,"captcha":captcha,"returnUrl":"","select":"email"}
response=session.post(url,headers=headers,data=data)
result=re.search(r"赖敬之",response.text)
if result:
    os.rename(captchaDir+str(timeStamp)+'.jpg',captchaDir+str(captcha)+'.jpg')
    print("验证码识别成功")
else:
    os.remove(captchaDir+str(timeStamp)+'.jpg')
    print("验证码识别失败")

