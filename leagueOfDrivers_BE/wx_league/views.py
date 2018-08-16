from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .serializers import CouponsSerializer

from rest_framework import generics
from rest_framework import viewsets
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .checkuser import checkdata
import json
import re
import requests
# Create your views here.


def serializers_json(seri):
    ser_ = serializers.serialize("json", seri)
    json_ = json.loads(ser_)
    return json_

def url_image(query_set):
    iconList = []
    for icon in query_set:
        iconList.append({"id":id,"icon":icon.display_pic})
    ser_ = serializers_json(query_set)
    for x in range(len(ser_)):
        try:
            ser_[x]["fields"]["icon"] = "https://qgdxsw.com:8000"+iconList[x]["icon"].url
        except AttributeError:
            ser_[x]["fields"]["icon"] = "https://qgdxsw.com:8000"+iconList[x]["icon"].display_pic.url
    return ser_

def image_comment(image_json):
    comment = "<p>2222222222222222222</p>"
    for x in image_json:
        comment += "<p><img src='{0}' style='' title='{1}'/></p>".format(x["fields"]["icon"],x["fields"]["display_pic"])
    return comment

def index_imageList(request):
    pics_query = Attachment.objects.filter(owner_id = 5)
    pic_json = url_image(pics_query)
    return JsonResponse({"code":0,"data":{"pics":pic_json}}) 


def notice_list(request):
    return JsonResponse({"code":0,"data":{"totalRow":2,"totalPage":1,"dataList":[{"dateAdd":"2017-10-23 13:59:55","id":345,"isShow":"0","title":"天气又冷","userId":1614},{"dateAdd":"2017-10-23 13:59:44","id":344,"isShow":"0","title":"天气热","userId":1614}]},"msg":"success"})


def discounts_coupons(request):
    return JsonResponse({"code":0,"data":[{"dateAdd":"2017-11-14 11:04:41","dateEndDays":30,"dateEndType":1,"dateStartType":1,"id":546,"moneyHreshold":300.00,"moneyMax":30.00,"moneyMin":30.00,"name":"满减优惠券","needScore":0,"needSignedContinuous":0,"numberGit":1,"numberGitNumber":1,"numberLeft":2999,"numberPersonMax":1,"numberTotle":3000,"numberUsed":1,"status":0,"statusStr":"正常","type":"1"},{"dateAdd":"2017-11-14 11:03:48","dateEndDays":30,"dateEndType":1,"dateStartType":1,"id":545,"moneyHreshold":200.00,"moneyMax":20.00,"moneyMin":20.00,"name":"满减优惠券","needScore":0,"needSignedContinuous":0,"numberGit":1,"numberGitNumber":1,"numberLeft":2999,"numberPersonMax":1,"numberTotle":3000,"numberUsed":1,"status":0,"statusStr":"正常","type":"1"},{"dateAdd":"2017-11-14 11:02:31","dateEndDays":30,"dateEndType":1,"dateStartType":1,"id":544,"moneyHreshold":100.00,"moneyMax":10.00,"moneyMin":10.00,"name":"满减优惠券","needScore":0,"needSignedContinuous":0,"numberGit":1,"numberGitNumber":1,"numberLeft":2999,"numberPersonMax":1,"numberTotle":3000,"numberUsed":1,"status":0,"statusStr":"正常","type":"1"}],"msg":"success"})


def discounts_fetch(request):
    return JsonResponse()



def banner_list(request):
    return JsonResponse({"code":0,"data":[{"businessId":1222,"dateAdd":"2017-11-13 15:57:24","dateUpdate":"2017-11-21 10:24:56","id":2296,"linkUrl":"pages/shop-cart/index","paixu":1,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/20/56fc0ace26a05bbd6b46d4dcd77b736a.jpg","remark":"","status":0,"statusStr":"显示","title":"lkllk","type":"0","userId":1614},{"businessId":23334,"dateAdd":"2017-11-13 15:57:51","dateUpdate":"2017-11-17 10:47:58","id":2297,"linkUrl":"","paixu":2,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/17/4eed2ccae3178578326f3adcd60a7b06.jpg","remark":"","status":0,"statusStr":"显示","title":"23434","type":"0","userId":1614},{"businessId":3,"dateAdd":"2017-11-13 15:58:22","dateUpdate":"2017-11-17 10:48:06","id":2298,"linkUrl":"","paixu":3,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/17/21a4c81f728d81ae2de9793f86ae333b.jpg","remark":"","status":0,"statusStr":"显示","title":"3","type":"0","userId":1614},{"businessId":4,"dateAdd":"2017-11-13 15:58:36","dateUpdate":"2017-11-17 10:48:32","id":2299,"linkUrl":"","paixu":4,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/17/4779e9615165f4de8ba115a598ed584c.jpg","remark":"","status":0,"statusStr":"显示","title":"4","type":"0","userId":1614},{"businessId":5,"dateAdd":"2017-11-21 10:26:03","dateUpdate":"2017-11-21 10:26:11","id":2477,"linkUrl":"","paixu":5,"picUrl":"https://cdn.it120.cc/apifactory/2017/11/20/43dc0b79b3ee8cd540c7f473d36f1c36.jpg","remark":"","status":0,"statusStr":"显示","title":"5","type":"0","userId":1614}],"msg":"success"})



def check_cookies(request):
    check_cookie(request.POST.get("cookei"))
    return JsonResponse({"code":200})

@csrf_exempt
def verify(request):
    if request.method == "POST":
        #初始化返回的字典
        data = {}

        #获取小程序数据
        code = request.POST.get('code','')
        encrypteddata = request.POST.get('encrypteddata','')
        iv = request.POST.get('iv','')

        #检查用户
        res = checkdata(code, encrypteddata, iv)
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
            passwd = make_password(openid)
            wechatuser = WechatUser.objects.create(
                username = openid,
                password = passwd,
                openid = openid,
                cookie = res['cookie']
            )
            new_user = authenticate(username = openid, password = openid)
            login(request, new_user)
            data['status'] = '已创建并登录'
            data['code'] = 0

        data['info'] = res
        #data['device'] = checkqr(code,res['cookie'])
        return JsonResponse(data)
    data = {'error':'仅接受POST请1求'}
    return JsonResponse(data)

def register(request):
    return JsonResponse({"code":10000})


@csrf_exempt
def address(request):
    data = {}
    cookie = request.POST.get('cookie','')
    address_id = request.POST.get('id','')
    provinceId = request.POST.get('provinceId','')
    cityId = request.POST.get('cityId','')
    districtId = request.POST.get('districtId','')
    linkMan = request.POST.get('linkMan','')
    address_text = request.POST.get('address','')
    mobile = request.POST.get('mobile','')
    code = request.POST.get('code','')
    isDefault = request.POST.get('isDefault','')
    user = check_user(cookie)
    if user == {}:
        return JsonResponse({'error':'用户会话信息失败,请重新登录'})
    address = Address.objects.filter(id = address_id)
    if len(address) != 1 or address_id == 0:
        Address.objects.create(province_id = provinceId, city_id = cityId, district_id = districtId, linkMan = linkMan, address = address_text, mobile = mobile, code = code,isDefault = False, owner_type = 0, owner_id = user.id )
        return JsonResponse({'code':0})
    else:
        address = Address.objects.get(id = address_id)
        address.province_id = provinceId
        address.city_id = cityId
        address.district_id = districtId
        address.linkMan = linkMan
        address.address = address_text
        address.mobile = mobile
        address.code = code
        address.save()
        return JsonResponse({'code':0})


def check_user(cookie):
    try:
        user = WechatUser.objects.get(cookie = cookie)
        return user
    except ObjectDoesNotExist:
        user = {}
   
def check_address(**filter_kwargs):
    address = Address.objects.filter(**filter_kwargs)
    if len(address) !=0:
        return address
    else:
        address = {}
        return address
@csrf_exempt 
def address_detail(request):
    if request.method =="POST":
        cookie = request.POST.get('cookie')
        address_id = request.POST.get('id')
        user = check_user(cookie)
        if user == {}:
            return JsonResponse({'error':'用户会话信息失败,请重新登录'})
        else:
            address = check_address(id = address_id)
            if address == {}:
                return JsonResponse({"code":100}) #code 100 没有查询结果
            else:
                ser_ = serializers.serialize("json", address)
                ser_ = json.loads(ser_)
                return JsonResponse({"code":0,"data":ser_})

@csrf_exempt
def address_list(request):
    if request.method =="POST":
        cookie = request.POST.get('cookie')
        user = check_user(cookie)
        default = request.POST.get('default')
        if user == {}:
            return JsonResponse({'error':'用户会话信息失败,请重新登录'})
        else:
            address = check_address(owner_id = user.id)
            if default == 'true':
                address = check_address(owner_id = user.id, isDefault = True)
            if address == {}:
                return JsonResponse({"code":100}) #code 100 没有查询结果
            else:
                ser_ = serializers.serialize("json", address)
                ser_ = json.loads(ser_)
                return JsonResponse({"code":0,"data":ser_})

@csrf_exempt
def address_update(request):
    if request.method =="POST":
        cookie = request.POST.get('cookie')
        user = check_user(cookie)
        address_id = request.POST.get('id')
        address_id = int(address_id) if isinstance(address_id,(str)) else address_id
        if user == {}:
            return JsonResponse({'error':'用户会话信息失败,请重新登录'})
        else:
            address_query = check_address(owner_id = user.id)
            if address_query == {}:
                return JsonResponse({"code":100}) #code 100 没有查询结果
            else:
                for address in address_query:
                    address.isDefault = False
                    if address.id == address_id:
                        address.isDefault = True
                    address.save()
                return JsonResponse({"code":0,"data":"选择成功"})




@csrf_exempt
def address_delete(request):
    if request.method =="POST":
        cookie = request.POST.get('cookie')
        user = check_user(cookie)
        address_id = request.POST.get('id')
        if user == {}:
            return JsonResponse({'error':'用户会话信息失败,请重新登录'})
        else:
            address = check_address(id = address_id,owner_id = user.id)
            if address == {}:
                return JsonResponse({"code":100}) #code 100 没有查询结果
            else:
                address.delete()
                return JsonResponse({"code":0,"data":"删除成功"})

def check_goods(page = 0, pageSize = 0, **filter_kwargs):
    goods_list = goods.objects.filter(**filter_kwargs)
    if len(goods_list) == 0:
        return {}
    else:
        if page == 0 and pageSize == 0:
            return goods_list
        paginator = Paginator(goods_list, pageSize)
        try:
            goods_page = paginator.page(page)
        except PageNotAnInteger:
            goods_page = paginator.page(1)
        except EmptyPage:
            goods_page = paginator.page(paginator.num_pagesi)
        return goods_page

@csrf_exempt
def goods_list(request):
    if request.method == "POST":
        page = request.POST.get("page")
        pageSize = request.POST.get("pageSize")
        category_id = request.POST.get('categoryId')
        data_all = request.POST.get("all")
        iconList = []
        if data_all == "true":
            category = Category.objects.all()
            for icon in category:
                iconList.append({"id":id,"icon":icon.icon.display_pic})
            ser_ = serializers_json(category)
            for x in range(len(ser_)):
                ser_[x]["fields"]["icon"] = "https://qgdxsw.com:8000"+iconList[x]["icon"].url
            return JsonResponse({"code":0, "data":ser_})
        category_goods = check_goods(int(page),int(pageSize),category_id = int(category_id))
        if category_goods == {}:
            return JsonResponse({"code":400}) #code 100 没有查询结果
        else:
            for icon in category_goods:
                iconList.append({"id":id,"pic":icon.pic.display_pic})
            ser_ = serializers_json(category_goods)
            for x in range(len(ser_)):
                ser_[x]["fields"]["pic"] = "https://qgdxsw.com:8000"+iconList[x]["pic"].url
            return JsonResponse({"code":0,"data":ser_})

@csrf_exempt
def goods_detail(request):
    if request.method == 'POST':
        good_id = request.POST.get("id")
        basicInfo = {"category_id":[],"goods_id":[]}
        basicInfo_query = check_goods(id = int(good_id))
        if basicInfo_query == {}:
            return JsonResponse({"code":400}) 
        for info in basicInfo_query:
            basicInfo['category_id'].append(info.category_id.id)
            basicInfo['goods_id'].append(info.id)
        category_query = Category.objects.filter(id = basicInfo['category_id'][0])
        pics_query = Attachment.objects.filter(owner_id = basicInfo['goods_id'][0])
        json_pics = url_image(pics_query)
        json_category = serializers_json(category_query)
        json_basicInfo = serializers_json(basicInfo_query)
        return JsonResponse({"code":0,"data":{"basicInfo" : json_basicInfo, "category" : json_category, "pics" : json_pics, "content":image_comment(json_pics)}})


class CouponsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Coupons to be viewed or edited.
    """
    queryset = Coupons.objects.all().filter(is_active = True).order_by('-id')
    serializer_class = CouponsSerializer


@csrf_exempt
def coupons(request):
    if request.method == 'POST':
        coupons_id = request.POST.get('refId')
        coupons_id = int(coupons_id) if isinstance(coupons_id,(str)) else coupons_id
        type_coupons = request.POST.get('type')
        if type_coupons == '1':
            coupons = Coupons.objects.filter(coupons_type = 1)
        else:
            if coupons_id != None:
                try:
                    coupons = Coupons.objects.filter(id = coupons_id)
                
                except TypeError:
                    return JsonResponse({"code":0,"error":"优惠券id类型错误"})
            else:
                coupons = Coupons.objects.filter(coupons_type = 1)
        data = serializers_json(coupons)
        return JsonResponse({"code":0,"data":data})
    else:
        return JsonResponse({"code":500,"error":"请使用POST方式请求"})

@csrf_exempt
def coupons_fetch(request):
    if request.method == "POST":
        coupons_id = request.POST.get('id')
        coupons_id = int(coupons_id) if isinstance(coupons_id,(str)) else coupons_id
        cookie = request.POST.get('cookie')
        user = check_user(cookie)
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        else:
            try:
                coupons = Coupons_users.objects.create(coupons_id = coupons_id, user_id = user.id)
            except ObjectDoesNotExist:
                return JsonResponse({"code":20001})
            return JsonResponse({"code":0})

@csrf_exempt
def coupons_my(request):
    if request.method == 'POST':
        cookie = request.POST.get('cookie')
        user = check_user(cookie)
        basicInfo = {"coupons_id":[]}
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        else:
            coupons_query = Coupons_users.objects.filter(user_id = user.id)
            for info in coupons_query:
                basicInfo['coupons_id'].append(info.coupons_id)
            coupons_list = []
            for coupons_id in basicInfo['coupons_id']:
                coupons_list.append(Coupons.objects.filter(id = coupons_id)[0])
            data = serializers_json(coupons_list)
            return JsonResponse({"code":0,"data":data})

@csrf_exempt
def order_list(request):
    if request.method == 'POST':
        cookie = request.POST.get('cookie')
        status = request.POST.get('status')
        status = int(status) if isinstance(status,(str)) else status
        user = check_user(cookie)
        basicInfo = {"order_id":[]}
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        else:
            orders_query = Order.objects.filter(wechat_user_id = user.id, status = status)
            for orders in orders_query:
                basicInfo["order_id"].append(orders.id)
            for order_id in basicInfo["order_id"]:
                OrderGoods_query = OrderGoods.objects.filter(order_id = order_id)
        data = {}
        try:
            data["goodsMap"] = url_image(OrderGoods_query)
            data["orderList"] = serializers_json(orders_query)
        except UnboundLocalError:
            return JsonResponse({"code":400,"msg":"没有订单"})    
        return JsonResponse({"code":0,"data":data})

@csrf_exempt
def order_close(request):
    if request.method == "POST":
        cookie = request.POST.get('cookie')
        orderId = request.POST.get('orderId')
        orderId = int(orderId) if isinstance(orderId,(str)) else orderId
        user = check_user(cookie)
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})       
        order = Order.objects.get(wechat_user_id = user.id, id = orderId)
        order.status = 5
        order.save()
        return JsonResponse({"code":0,"msg":"删除订单"})

@csrf_exempt
def goods_price(request):
    if request.method == "POST":
        id = request.POST.get("id")
        goods_query = goods.objects.filter(id = id)
        data = serializers_json(goods_query)
        return JsonResponse({"code":0,"data":data})

@csrf_exempt
def order_create(request):
    if request.method == "POST":
        cookie = request.POST.get('cookie')
        remark = request.POST.get('remark')
        goodsJsonStr = request.POST.get('goodsJsonStr')
        payOnDelivery = request.POST.get('payOnDelivery')
        user = check_user(cookie)
        if user == {}:
            return JsonResponse({"code":0,"msg":"请重新登录"})
        order = Order.objects.create(wechat_user_id = user,\
                                     status = 0,\
                                     remark = remark,\
                                     logistics_id = Logistics.objects.get(id = 1)
                                     )
        goods_list = json.loads(goodsJsonStr)
        amountTotle = []
        for good in goods_list:
            goodsId = goods.objects.get(id = good['goodsId'])
            amountTotle.append(goodsId.minPrice)
            ordergoods = OrderGoods.objects.create(order_id = order.id,\
                                                   goods_id = goodsId.id,\
                                                   name = goodsId.name,\
                                                   display_pic = goodsId.pic,\
                                                   property_str = "-",\
                                                   price = goodsId.minPrice,\
                                                   amount = 1,\
                                                   total = goodsId.minPrice)
        order.goods_price = sum(amountTotle)
        order.number_goods = len(amountTotle)
        order.save()
        return JsonResponse({"code":0,"data":{"isNeedLogistics":1,"amountTotle":sum(amountTotle),"amountLogistics":5}})
        

@csrf_exempt
def order_detail(request):
    if request.method == "POST":
        cookie = request.POST.get('cookie')
        orderId = request.POST.get('id')
        orderId = int(orderId) if isinstance(orderId, (str)) else orderId
        user = check_user(cookie)
        if user == {}:
            return JsonResponse({"code":400,"msg":"请重新登录"})
        order_obj = Order.objects.filter(wechat_user_id = user.id, id = orderId )
        ser_ = serializers_json(order_obj)
        return JsonResponse({"code":0,"data":ser_})

def order_pay(request):
    if request.method == "POST":
        cookie = request.POST.get('cookie')
        remark = request.POST.get('remark')
        goodsJsonStr = request.POST.get('goodsJsonStr')
        payOnDelivery = request.POST.get('payOnDelivery')
        user = check_user(cookie)
        if user == {}:
            return JsonResponse({"code":0,"msg":"请重新登录"})
        order = Order.objects.create(wechat_user_id = user,\
                                     status = 0,\
                                     remark = remark,\
                                     logistics_id = Logistics.objects.get(id = 1)
                                     )
        goods_list = json.loads(goodsJsonStr)
 
