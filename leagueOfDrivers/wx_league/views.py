from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from .models import *
from .checkuser import checkdata
import json
import requests
# Create your views here.



def notice_list(request):
    return JsonResponse({"code":0,"data":{"totalRow":2,"totalPage":1,"dataList":[{"dateAdd":"2017-10-23 13:59:55","id":345,"isShow":"0","title":"天气又冷","userId":1614},{"dateAdd":"2017-10-23 13:59:44","id":344,"isShow":"0","title":"天气热","userId":1614}]},"msg":"success"})

def discounts_coupons(request):
    return JsonResponse({"code":0,"data":[{"dateAdd":"2017-11-14 11:04:41","dateEndDays":30,"dateEndType":1,"dateStartType":1,"id":546,"moneyHreshold":300.00,"moneyMax":30.00,"moneyMin":30.00,"name":"满减优惠券","needScore":0,"needSignedContinuous":0,"numberGit":1,"numberGitNumber":1,"numberLeft":2999,"numberPersonMax":1,"numberTotle":3000,"numberUsed":1,"status":0,"statusStr":"正常","type":"1"},{"dateAdd":"2017-11-14 11:03:48","dateEndDays":30,"dateEndType":1,"dateStartType":1,"id":545,"moneyHreshold":200.00,"moneyMax":20.00,"moneyMin":20.00,"name":"满减优惠券","needScore":0,"needSignedContinuous":0,"numberGit":1,"numberGitNumber":1,"numberLeft":2999,"numberPersonMax":1,"numberTotle":3000,"numberUsed":1,"status":0,"statusStr":"正常","type":"1"},{"dateAdd":"2017-11-14 11:02:31","dateEndDays":30,"dateEndType":1,"dateStartType":1,"id":544,"moneyHreshold":100.00,"moneyMax":10.00,"moneyMin":10.00,"name":"满减优惠券","needScore":0,"needSignedContinuous":0,"numberGit":1,"numberGitNumber":1,"numberLeft":2999,"numberPersonMax":1,"numberTotle":3000,"numberUsed":1,"status":0,"statusStr":"正常","type":"1"}],"msg":"success"})


def discounts_fetch(request):
    return JsonResponse()


def banner_list(request):
    return JsonResponse({"code":0,"data":[{"businessId":1222,"dateAdd":"2017-11-13 15:57:24","dateUpdate":"2017-11-21 10:24:56","id":2296,"linkUrl":"pages/shop-cart/index","paixu":1,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/20/56fc0ace26a05bbd6b46d4dcd77b736a.jpg","remark":"","status":0,"statusStr":"显示","title":"lkllk","type":"0","userId":1614},{"businessId":23334,"dateAdd":"2017-11-13 15:57:51","dateUpdate":"2017-11-17 10:47:58","id":2297,"linkUrl":"","paixu":2,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/17/4eed2ccae3178578326f3adcd60a7b06.jpg","remark":"","status":0,"statusStr":"显示","title":"23434","type":"0","userId":1614},{"businessId":3,"dateAdd":"2017-11-13 15:58:22","dateUpdate":"2017-11-17 10:48:06","id":2298,"linkUrl":"","paixu":3,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/17/21a4c81f728d81ae2de9793f86ae333b.jpg","remark":"","status":0,"statusStr":"显示","title":"3","type":"0","userId":1614},{"businessId":4,"dateAdd":"2017-11-13 15:58:36","dateUpdate":"2017-11-17 10:48:32","id":2299,"linkUrl":"","paixu":4,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/17/4779e9615165f4de8ba115a598ed584c.jpg","remark":"","status":0,"statusStr":"显示","title":"4","type":"0","userId":1614},{"businessId":5,"dateAdd":"2017-11-21 10:26:03","dateUpdate":"2017-11-21 10:26:11","id":2477,"linkUrl":"","paixu":5,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/20/43dc0b79b3ee8cd540c7f473d36f1c36.jpg","remark":"","status":0,"statusStr":"显示","title":"5","type":"0","userId":1614}],"msg":"success"})

def category(request):
    return JsonResponse({"code":0,"data":[{"dateAdd":"2017-11-16 15:21:37","icon":"","id":4019,"isUse":"0","key":"0","level":1,"name":"热销","paixu":0,"pid":0,"type":"0","userId":1614},{"dateAdd":"2017-11-16 15:32:13","icon":"https://cdn.it120.cc/apifactory/2017/11/13/016fa7b91d5c8d35d45e1af64c0124b2.png","id":4020,"isUse":"0","key":"00","level":2,"name":"热销0","paixu":0,"pid":4019,"type":"00","userId":1614},{"dateAdd":"2017-11-16 15:32:47","icon":"https://cdn.it120.cc/apifactory/2017/11/13/e7cfe993ad4fee74c22d7c3c5cf908fb.png","id":4021,"isUse":"0","key":"01","level":2,"name":"热销1","paixu":1,"pid":4019,"type":"01","userId":1614},{"dateAdd":"2017-11-16 15:37:43","icon":"https://cdn.it120.cc/apifactory/2017/11/13/2dd9076ad493d920a59df307c3ba0729.png","id":4022,"isUse":"0","key":"02","level":2,"name":"热销2","paixu":2,"pid":4019,"type":"02","userId":1614},{"dateAdd":"2017-11-16 15:38:54","icon":"https://cdn.it120.cc/apifactory/2017/11/13/471ee7d7a75de7fc5b9aaafd64c1c036.png","id":4023,"isUse":"0","key":"03","level":2,"name":"热销3","paixu":3,"pid":4019,"type":"03","userId":1614},{"dateAdd":"2017-11-16 15:39:45","icon":"https://cdn.it120.cc/apifactory/2017/11/13/fd894fe376cce4b3066b8a3f26be679f.png","id":4024,"isUse":"0","key":"04","level":2,"name":"热销4","paixu":4,"pid":4019,"type":"04","userId":1614},{"dateAdd":"2017-11-16 15:40:42","icon":"https://cdn.it120.cc/apifactory/2017/11/13/9299b30603384e107ef043bfb748c395.png","id":4025,"isUse":"0","key":"05","level":2,"name":"热销5","paixu":5,"pid":4019,"type":"05","userId":1614},{"dateAdd":"2017-11-16 15:41:47","icon":"https://cdn.it120.cc/apifactory/2017/11/13/c67680b925f3337d1a3f620f61cdbd8a.png","id":4026,"isUse":"0","key":"06","level":2,"name":"热销6","paixu":6,"pid":4019,"type":"06","userId":1614},{"dateAdd":"2017-11-17 09:29:44","icon":"https://cdn.it120.cc/apifactory/2017/11/17/f37c763a3e2f5ea865fc559714ddbe32.png","id":4049,"isUse":"0","key":"07","level":2,"name":"热销7","paixu":7,"pid":4019,"type":"07","userId":1614},{"dateAdd":"2017-11-17 09:30:21","icon":"https://cdn.it120.cc/apifactory/2017/11/17/637bf435b55faac1def00c97b25387ee.png","id":4050,"isUse":"0","key":"08","level":2,"name":"热销8","paixu":8,"pid":4019,"type":"08","userId":1614},{"dateAdd":"2017-11-17 09:31:14","icon":"https://cdn.it120.cc/apifactory/2017/11/17/25401590eeff2e9d51f81dad80fe82cd.png","id":4051,"isUse":"0","key":"09","level":2,"name":"热销9","paixu":9,"pid":4019,"type":"09","userId":1614},{"dateAdd":"2017-11-17 10:37:22","icon":"https://cdn.it120.cc/apifactory/2017/11/17/ec399bf0af49270b89dafbad20d44cc8.png","id":4052,"isUse":"0","key":"010","level":2,"name":"热销10","paixu":10,"pid":4019,"type":"010","userId":1614},{"dateAdd":"2017-10-23 00:59:29","icon":"https://cdn.it120.cc/apifactory/2017/10/20/9f1c2a82d914ad4f775aeba145e3e573.jpg","id":2933,"isUse":"0","key":"1","level":1,"name":"集成灶","paixu":1,"pid":0,"type":"1","userId":1614},{"dateAdd":"2017-11-06 09:43:26","icon":"","id":3575,"isUse":"0","key":"2","level":1,"name":"蒸箱烤箱","paixu":2,"pid":0,"type":"2","userId":1614},{"dateAdd":"2017-11-06 09:43:46","icon":"","id":3576,"isUse":"0","key":"3","level":1,"name":"水槽","paixu":3,"pid":0,"type":"3","userId":1614},{"dateAdd":"2017-11-07 09:19:29","icon":"","id":3607,"isUse":"0","key":"4","level":1,"name":"分类4","paixu":4,"pid":0,"type":"4","userId":1614},{"dateAdd":"2017-11-07 09:19:50","icon":"","id":3608,"isUse":"0","key":"5","level":1,"name":"分类5","paixu":5,"pid":0,"type":"5","userId":1614},{"dateAdd":"2017-11-28 14:12:18","icon":"","id":4467,"isUse":"0","key":"6","level":1,"name":"分类6","paixu":6,"pid":0,"type":"6","userId":1614},{"dateAdd":"2017-11-28 14:12:29","icon":"","id":4468,"isUse":"0","key":"7","level":1,"name":"分类7","paixu":7,"pid":0,"type":"7","userId":1614},{"dateAdd":"2017-11-28 14:12:40","icon":"","id":4469,"isUse":"0","key":"8","level":1,"name":"分类8","paixu":8,"pid":0,"type":"8","userId":1614},{"dateAdd":"2017-11-28 14:12:51","icon":"","id":4470,"isUse":"0","key":"9","level":1,"name":"分类9","paixu":9,"pid":0,"type":"9","userId":1614},{"dateAdd":"2017-11-28 14:13:05","icon":"","id":4471,"isUse":"0","key":"10","level":1,"name":"分类10","paixu":10,"pid":0,"type":"10","userId":1614}],"msg":"success"})


def get_value(request):
    return JsonResponse({"code":0,"data":{"creatAt":"2017-10-23 14:21:41","dateType":0,"id":944,"key":"mallName","remark":"","updateAt":"2017-10-23 14:21:41","userId":1614,"value":"小韩商城"},"msg":"success"})

def check_token(request):
    return JsonResponse({"code":200})

@csrf_exempt
def verify(request):
    if request.method == "POST":
        #print(request.POST)
        #初始化返回的字典
        data = {}

        #获取小程序数据
        code = request.POST.get('code','')
        print("333333333333333333333333333333333333333")
        print(request.POST.get('code'))
        encrypteddata = request.POST.get('encrypteddata','')
        iv = request.POST.get('iv','')
        #print(iv)

        #检查用户
        res = checkdata(code, encrypteddata, iv)
        #print('解码信息',res)
        print(res)
        #检查不通过
        errorinfo = res.get('error',None)
        if errorinfo:
            return JsonResponse(res)

        openid = res['openid']
        user = authenticate(username = openid, password = openid)
        #登录用户并保存cookie
        if user is not None and user.is_active:
            login(request, user)
            query_user = WechatUser.objects.get(openid=openid)
            query_user.cookie = res['cookie']
            query_user.save()

            #获取用户发送的信件
            data['status'] = '已登录'
            data['code'] = 0
        #新建用户
        else:
            wechatuser = WechatUser.objects.create(
                username=openid,
                password = password,
                openid = openid,
                cookie = res['cookie']
            )
            new_user = authenticate(username = openid, password = openid)
            login(request, new_user)
            data['status'] = '已创建并登录'
            data['code'] = 0

        data['info'] = res
        #print('最终返回信息', data)
        #data['device'] = checkqr(code,res['cookie'])
        return JsonResponse(data)
    data = {'error':'仅接受POST请1求'}
    return JsonResponse(data)

def register(request):
    return JsonResponse({"code":10000})

