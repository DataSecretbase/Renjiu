from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, login,authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view


from django.core.mail import send_mail
from django.conf import settings
from .serializers import CouponsSerializer

from .bargain_method import method

from rest_framework import generics
from rest_framework import viewsets
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .checkuser import checkdata
import json
import re
import requests

import datetime

from . import config
from wechatpy.pay import WeChatPay
# Create your views here.


def serializers_json(seri, use_natural=False):
    ser_ = serializers.serialize("json", seri, use_natural_foreign_keys=use_natural)
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
        comment += "<p><img src='{0}' style='' title='{1}'/></p>".format(x["fields"]["icon"],
                                                                         x["fields"]["display_pic"])
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
    check_cookie(request.POST.get("token"))
    return JsonResponse({"token":200})

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
        print(res['cookie'])
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
                cookie = res['cookie'],
                avatar = Icon.objects.get(name = '用户头像')
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
    token = request.POST.get('token','')
    address_id = request.POST.get('id','')
    provinceId = request.POST.get('provinceId','')
    cityId = request.POST.get('cityId','')
    districtId = request.POST.get('districtId','')
    linkMan = request.POST.get('linkMan','')
    address_text = request.POST.get('address','')
    mobile = request.POST.get('mobile','')
    code = request.POST.get('code','')
    isDefault = request.POST.get('isDefault','')
    user = check_user(token)
    if user == {}:
        return JsonResponse({'error':'用户会话信息失败,请重新登录'})
    address = Address.objects.filter(id = address_id)
    if len(address) != 1 or address_id == 0:
        Address.objects.create(province_id = provinceId,
                               city_id = cityId,
                               district_id = districtId,
                               link_man = linkMan,
                               address = address_text,
                               mobile = mobile,
                               code = code,
                               is_default = False,
                               owner_type = 0,
                               owner_id = user.id )
        return JsonResponse({'code':0})
    else:
        address = Address.objects.get(id = address_id)
        address.province_id = provinceId
        address.city_id = cityId
        address.district_id = districtId
        address.link_man = linkMan
        address.address = address_text
        address.mobile = mobile
        address.code = code
        address.save()
        return JsonResponse({'code':0})


def check_user(token):
    try:
        user = Token.objects.get(key = token)
        return user.user
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
        token = request.POST.get('token')
        address_id = request.POST.get('id')
        user = check_user(token)
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
        print(request.POST)
        token = request.POST.get('token')
        user = check_user(token)
        default = request.POST.get('default')
        if user == {}:
            return JsonResponse({'error':'用户会话信息失败,请重新登录'})
        else:
            print(user.id)
            address = check_address(owner_id = user.id)
            if default == 'true':
                address = check_address(owner_id = user.id, is_default = True)
            if address == {}:
                return JsonResponse({"code":100}) #code 100 没有查询结果
            else:
                ser_ = serializers.serialize("json", address)
                ser_ = json.loads(ser_)
                return JsonResponse({"code":0,"data":ser_})

@csrf_exempt
def address_update(request):
    if request.method =="POST":
        token = request.POST.get('token')
        user = check_user(token)
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
                    address.is_default = False
                    if address.id == address_id:
                        address.is_default = True
                    address.save()
                return JsonResponse({"code":0,"data":"选择成功"})




@csrf_exempt
def address_delete(request):
    if request.method =="POST":
        token = request.POST.get('token')
        user = check_user(token)
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
    goods_list = Goods.objects.filter(**filter_kwargs)
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
    if request.method == 'GET':
        good_id = request.GET.get("id")
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
    return JsonResponse({"code":0,
                         "data":{"basicInfo" : json_basicInfo,
                                 "category" : json_category,
                                 "pics" : json_pics,
                                 "content":image_comment(json_pics)}
                       })

class CouponsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Coupons to be viewed or edited.
    """
    queryset = Coupons.objects.all().filter(is_active = True).order_by('-id')
    serializer_class = CouponsSerializer


@csrf_exempt
def coupons(request):
    if request.method == 'POST':
        goods_id = request.POST.get('refId')
        goods_id = int(goods_id) if isinstance(goods_id,(str)) else goods_id
        if goods_id is None:
            coupons = Coupons.objects.filter(coupons_type = 1)
        else:
            if goods_id != None:
                try:
                    coupons = Coupons.objects.filter(goods_id = goods_id)
                
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
        token = request.POST.get('token')
        user = check_user(token)
        coupons_query = Coupons.objects.get(id = coupons_id)
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        else:
            try:
                coupons = Coupons_users.objects.create(coupons_id = coupons_query, 
                        user_id = user,
                        date_end_days = Coupons.objects.get(id = coupons_id).date_end_days)
            except ObjectDoesNotExist:
                return JsonResponse({"code":20001})
            return JsonResponse({"code":0})

@csrf_exempt
def coupons_my(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        user = check_user(token)
        goodsListId = request.POST.get('goodsListId')
        basicInfo = {"coupons_id":[]}
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        else:
            coupons_query = Coupons_users.objects.filter(user_id = user.id,date_end_days__lte=datetime.date.today())
            for info in coupons_query:
                basicInfo['coupons_id'].append(info.coupons_id)
            coupons_list = []
            if goodsListId is None:
                for coupons_id in basicInfo['coupons_id']:
                    coupons_list.append(Coupons.objects.filter(id = coupons_id)[0])
            else:
                for coupons_id in basicInfo['coupons_id']:
                    coupons_query = Coupons.objects.get(id = coupons_id)
                    for good in goodsListId:
                        print(coupons_query.goods_id.id)
                        print(good)
                        if coupons_query.goods_id.id == good:
                            coupons_list.append(Coupons.objects.filter(id = coupons_id)[0])
                            break
            data = serializers_json(coupons_list)
            return JsonResponse({"code":0,"data":data})

@csrf_exempt
def order_list(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        status = request.POST.get('status')
        status = int(status) if isinstance(status,(str)) else status
        user = check_user(token)
        print(user)
        basicInfo = {"order_id":[]}
        if user == {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        else:
            orders_query = Order.objects.filter(wechat_user_id = user.id)
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
        token = request.POST.get('token')
        orderId = request.POST.get('orderId')
        orderId = int(orderId) if isinstance(orderId,(str)) else orderId
        user = check_user(token)
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
        goods_query = Goods.objects.filter(id = id)
        data = serializers_json(goods_query)
        return JsonResponse({"code":0,"data":data})

@csrf_exempt
def order_create(request):
    if request.method == "POST":
        token = request.POST.get('token')
        remark = request.POST.get('remark')
        goodsJsonStr = request.POST.get('goodsJsonStr')
        payOnDelivery = request.POST.get('payOnDelivery')
        couponId = request.POST.get('couponId')
        caculate = request.POST.get('caculate')
        
        user = check_user(token)
        if user == {}:
            return JsonResponse({"code":0,"msg":"请重新登录"})
        #检查优惠券信息
        try:
            coupons_query = Coupons_users.objects.get(coupons_id = couponId,
                                      user_id = user.id,
                                      date_end_days__lte=datetime.date.today())
            min_price = coupons_query.min_price
        except ObjectDoesNotExist:
            couponId = 0
            min_price = 0
        order = Order.objects.create(wechat_user_id = user,
                                     status = 0,
                                     remark = remark,
                                     coupons_id = couponId,
                                     )
        goods_list = json.loads(goodsJsonStr)
        amountTotle = []
        for good in goods_list:
            goodsId = Goods.objects.get(id = good['goodsId'])
            amountTotle.append(goodsId.original_price)
            ordergoods = OrderGoods.objects.create(order_id = order.id,
                                                   goods_id = goodsId.id,
                                                   name = goodsId.name,
                                                   display_pic = goodsId.pic,
                                                   property_str = "-",
                                                   price = goodsId.original_price,
                                                   amount = 1,
                                                   total = goodsId.original_price)
        order.goods_price = sum(amountTotle)-min_price
        order.number_goods = len(amountTotle)
        order.save()
        return JsonResponse({"code":0,
                             "data":{"isNeedLogistics":0,
                                     "amountTotle":sum(amountTotle),
                                     "amountLogistics":0}
                           })
        

@csrf_exempt
def order_detail(request):
    if request.method == "POST":
        token = request.POST.get('token')
        orderId = request.POST.get('id')
        orderId = int(orderId) if isinstance(orderId, (str)) else orderId
        user = check_user(token)
        if user == {}:
            return JsonResponse({"code":400,"msg":"请重新登录"})
        order_obj = Order.objects.filter(wechat_user_id = user.id, id = orderId )
        ser_ = serializers_json(order_obj)
        return JsonResponse({"code":0,"data":ser_})

def get_user_info(js_code):
    """
    使用 临时登录凭证code 获取 session_key 和 openid 等
    支付部分仅需 openid，如需其他用户信息请按微信官方开发文档自行解密
    """
    req_params = {
        'appid': config.APPINFO["appid"],
        'secret': config.APPINFO["secret"],
        'js_code': js_code,
        'grant_type': 'authorization_code',
    }
    user_info = requests.get('https://api.weixin.qq.com/sns/jscode2session', 
                              params=req_params, timeout=3, verify=False)
    return user_info.json()




@csrf_exempt
def order_pay(request):
    if request.method == "POST":
        token = request.POST.get('token')
        order_id = request.POST.get('order_id')
        openid = get_user_info(code)['openid']
        user = check_user(token)
        if user == {}:
            return JsonResponse({"code":0,"msg":"请重新登录"})
        pay = WeChatPay(config.APPINFO['appid'], settings.WECHAT['MERCHANT_KEY'], settings.WECHAT['MCH_ID'])
        order = pay.order.create(
            trade_type = config.WECHAT['TRADE_TYPE'],     # 交易类型，小程序取值：JSAPI
            body = config.WECHAT['BODY'],                 # 商品描述，商品简单描述
            total_fee = config.WECHAT['TOTAL_FEE'],       # 标价金额，订单总金额，单位为分
            notify_url = config.WECHAT['NOTIFY_URL'],    
            user_id = openid                          
        )
        wxpay_params = pay.jsapi.get_jsapi_params(order['prepay_id'])
        order = Order.objects.get(id = order_id)
        order.status = 5
        order.save()
        return JsonResponse({"code":0,"data":"wxpay_params"})

@api_view(['GET', 'POST'])
def wxpayNotify(request):
    _xml = request.body
    #拿到微信发送的xml请求 即微信支付后的回调内容
    xml = str(_xml, encoding="utf-8")
    print("xml", xml)
    return_dict = {}
    tree = et.fromstring(xml)
    #xml 解析
    return_code = tree.find("return_code").text
    try:
        if return_code == 'FAIL':
            # 官方发出错误
            return_dict['message'] = '支付失败'
            #return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
        elif return_code == 'SUCCESS':
        #拿到自己这次支付的 out_trade_no 
            _out_trade_no = tree.find("out_trade_no").text
                #这里省略了 拿到订单号后的操作 看自己的业务需求
    except Exception as e:
        pass
    finally:
        return HttpResponse(return_dict, status=status.HTTP_200_OK)




def datein(request):

    if request.method == 'GET':
        data = {}
        token = request.GET.get('token')
        datetime = request.GET.get('date')
        user = check_user(token)
        if user == "{}":
            return JsonResponse({code:500,err:"请重新登录"})

        datetime = json.loads(datetime)
        try:
            book_query = Book.objects.get(id = datetime['pk'])
        except ObjectDoseNotExist:
            return JsonResponse({'code':400,'msg':'该预约记录未找到'})            

        book_query.status = datetime['fields']['status']
        book_query.save()
        data['exist'] = 'existed'
             # 添加日志记录
                #new_log = Log.objects.create(
                #    owner=profile,
                #    type='0',
                #    device=device
                #)


        return JsonResponse(data)


    data = {'error': '仅接受GET请求'}
    return JsonResponse(data)
 
# 索引数据库
def checkqr(request):
    # pass
    if request.method == 'GET':
        data = {}
        token = request.GET.get("token")
        print(token)
        # 验证用户
        user = check_user(token)
        if user == {}:
            data = {'error': '用户错误'}
            return JsonResponse(data)
        book_query = Book.objects.filter(coach = user.id)
        book_ser = serializers_json(book_query,True) 

        return JsonResponse({"code":0,"data":book_ser})


    data = {'error': '仅接受POST请求'}
    return JsonResponse({"code":500,"msg":data})



@csrf_exempt
def school_detail(request):
    if request.method == 'POST':
        id = request.POST.get('bookid')
        school_query = DriverSchool.objects.filter(id = id)
        school_ser = serializers_json(school_query)
        return JsonResponse({"code":0,"data":school_ser})
    data = {"code":500,"msg":"仅接受POST请求"}
    return JsonResponse(data)

def send_email(request):
    msg='<a href="哈哈哈" target="_blank">点击激活</a>'
    send_mail('标题','内容',settings.EMAIL_FROM,
              ['2175666031@qq.com'],
              html_message = msg,
              fail_silently=False)
    return HttpResponse('ok')

def goods_reputation(request):
    goods_id = request.GET.get('goodsId')
    goods_id = int(goods_id) if isinstance(goods_id,(str)) else goods_id
    reputation_query = GoodsReputation.objects.filter(goods_id = goods_id)
    reputation_ser = serializers_json(reputation_query, use_natural = True)
    return JsonResponse({"code":0,"data":reputation_ser})

def bargain_add(request):
    bargain_id = request.GET.get('kjid')
    bargain_id = int(bargain_id) if isinstance(bargain_id,(str)) else bargain_id
    token = request.GET.get('token')
    joiner = request.GET.get('joinerUser')
    joiner = int(joiner) if isinstance(joiner,(str)) else joiner
    user = check_user(token)
    if user == {}:
        return JsonResponse({"code":500,"msg":"请重新登录"})
    try:
        bargain_query = Bargain.objects.get(id = bargain_id)
    except ObjectDoesNotExist:
        return JsonResponse({"code":500,"msg":"活动已经过期"})
    try:
        bargainFriend_query = BargainFriend.objects.get(bargain_friend_id = user.id)
    except ObjectDoesNotExist:
        BargainFriend.objects.create(bargain_friend_id = user,
                                     rank = bargain_query.times + 1,
                                     bargain_user_id = BargainUser.objects.get(bargain_id = bargain_id,
                                                                              user_id = joiner))
        bargain_query.times +=1
        bargain_query.save()
        return JsonResponse({"code":0,"data":"砍价成功"})
    return JsonResponse({"code":500,"msg":"你已经砍过一次了"})
 
def bargain_detail(request):
    goods_id = request.GET.get('goods_id')
    goods_id = int(goods_id) if isinstance(goods_id,(str)) else goods_id
    kjid = request.GET.get('kjid')
    kjid = int(kjid) if isinstance(kjid,(str)) else kjid
    token = request.GET.get('token')
    joiner = request.GET.get('joiner')
    bargain_query = Bargain.objects.filter(goods_id = goods_id)
    if kjid is not None: 
        bargain_query = Bargain.objects.filter(id = kjid)
    print(bargain_query.values(), goods_id)
    user = check_user(token)
    if user == {}:
        return JsonResponse({"code":500,"msg":"请重新登录"})
    joiner = int(joiner) if isinstance(joiner,(str)) else joiner
    print(joiner)
    if joiner is None and goods_id is None:
        print("joiner未参加")
        
        BargainUser.objects.create(bargain_id = bargain_query[0],user_id = user)
        joiner = user.id
    print(joiner, goods_id)
    if joiner is None and goods_id is not None:
        bargainUser_query = BargainUser.objects.filter(bargain_id = bargain_query.values()[0]['id'],
                                                       user_id = user.id)
        if len(bargainUser_query) == 0:
            BargainUser.objects.create(bargain_id = bargain_query[0],user_id = user)
        joiner = user.id
    try:
        joiner = WechatUser.objects.get(id = joiner)
    except ObjectDoesNotExist:
        return JsonResponse({"code":405,"msg":"该用户不存在"})
    bargain_json = serializers_json(bargain_query)
    print(bargain_query.values())
    bargainUser_query = BargainUser.objects.filter(bargain_id = bargain_query.values()[0]['id'],
                                                   user_id = joiner.id)
    bargainUser_json = serializers_json(bargainUser_query)

    bargainFriend_query = BargainFriend.objects.filter(bargain_user_id = bargainUser_query.values()[0]['id'])
    bargainFriend_json = serializers_json(bargainFriend_query,use_natural = True)
    for bargain in bargain_json:
        bargain['fields']['price'] = method.method_log(cur_times = bargain['fields']['times'],
                                                       exp_times = bargain['fields']['expected_times'],
                                                       change = bargain['fields']['expected_price'])
    return JsonResponse({"code":0,
                         "data":{"bargain":bargain_json,
                                 "bargainUser":bargainUser_json,
                                 "bargainUserName":bargainUser_query[0].user_id.name,
                                 "bargainFriend":bargainFriend_json}
                       })


def is_enrol(request):
    token = request.GET.get("token")
    user = check_user(token)
    if user is {}:
        return JsonResponse({"code":500,"msg":"请重新登录"})
    userExam_query = UserExam.objects.filter(user_id = user.id,exam_status = 1)
    if len(userExam_query) ==0:
        return JsonResponse({"code":500,"msg":"你暂时没有需要进行的预约教学，如果还未报名，请报名"})
    return JsonResponse({"code":0})


def coach_list(request):
    token = request.GET.get("token")
    user = check_user(token)
    if user is {}:
        return JsonResponse({"code":500,"msg":"请重新登录"})
    userExam_query = UserExam.objects.filter(user_id = user.id,exam_status = 1)
    print(userExam_query.values()[0]['train_ground_id'])
    train_ground = userExam_query.values()[0]['train_ground_id']
    coachDriverSchool_query = CoachDriverSchool.objects.filter(train_ground = train_ground)
    coachDriverSchool_json = serializers_json(coachDriverSchool_query, use_natural = True)
    for coachDriverSchool in coachDriverSchool_json:
        print(coachDriverSchool)
        book_query = Book.objects.filter(coach = coachDriverSchool["fields"]["coach"]["id"])
        book_json = serializers_json(book_query,use_natural = True)
        bookSet_query = BookSet.objects.filter(coach_driver_school = coachDriverSchool["pk"],
                                            status = 1)
        bookSet_json = serializers_json(bookSet_query)
        bookSet_list = []
        for bookSet in bookSet_json:
            bookSet_list.append({"startTime":bookSet["fields"]["book_date_start"].replace("T"," "),
                            "endTime":bookSet["fields"]["book_date_end"].replace("T"," "),
                            "status":bookSet["fields"]["status"]})
        coachDriverSchool['book_list'] = book_json
        coachDriverSchool['bookSet_list'] = bookSet_list
    return JsonResponse({"code":0,"data":coachDriverSchool_json})

def book_add(request):
    startTimeText = request.GET.get('startTimeText')
    startTime_datetime = datetime.datetime.strptime(startTimeText, "%Y-%m-%d %H:%M:%S")
    endTimeText = request.GET.get('endTimeText')
    endTime_datetime = datetime.datetime.strptime(endTimeText, "%Y-%m-%d %H:%M:%S")
    token = request.GET.get('token')
    coach_id = request.GET.get('coach_id')
    coach_id = int(coach_id) if isinstance(coach_id,(str)) else coach_id
    train_ground = request.GET.get('train_ground')
    user = check_user(token)
    if user is {}:
        return JsonResponse({"code":500,"msg":"请重新登录"})
    try:
        coachDriverSchool_query = CoachDriverSchool.objects.get(coach = coach_id,
                                                                train_ground = DriverSchool.objects.get(name = train_ground))
    except ObjectDoesNotExist:
        return JsonResponse({"code":500,"msg":"预约信息有误"})
    try:
        bookSet_query = BookSet.objects.get(coach_driver_school = coachDriverSchool_query.id,
                                            book_date_start = startTime_datetime,
                                            book_date_end = endTime_datetime)
    except ObjectDoesNotExist:
        bookSet_query = BookSet.objects.create(coach_driver_school = coachDriverSchool_query, num_student = 3, book_date_start = startTime_datetime, book_date_end = endTime_datetime, set_type = 1)
    if bookSet_query.cur_book == bookSet_query.num_student:
        return JsonResponse({"code":500,"msg":"当前预约已满,请换一个时间段"})
    coach_query = WechatUser.objects.get(id = coach_id)
    book_create = Book.objects.create(coach = coach_query,
                                      user = user,
                                      train_ground = DriverSchool.objects.get(name = train_ground),
                                      book_time_start = startTime_datetime,
                                      book_time_end = endTime_datetime,
                                      status = 0)
    bookSet_query.cur_book +=1
    bookSet_query.save()
    return JsonResponse({"code":0,"data":"预约成功"})

def topic_get(request):
    if request.method == "POST":
        page = request.POST.get("page")
        pageSize = request.POST.get("pageSize")
        topic_id = request.POST.get('topicId')
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

def booksets_add(request):
    if request.method == 'GET':
        token = request.GET.get("token")
        set_type = request.GET.get("type")
        date = request.GET.get("date")
        user = check_user(token)
        if user is {}:
            return JsonResponse({'code':500,"msg":"请重新登录"})
        if set_type == "default":
            book_set_query = BookSet.objects.filter(coach_driver_school = \
                                                    CoachDriverSchool.objects.filter(coach = user.id)[0].id,
                                                    set_type = 0)
            if len(book_set_query) == 0:
                book_set_query = BookSet.objects.create(coach_driver_school =\
                                                        CoachDriverSchool.objects.get(coach = user.id),
                                                        num_student = 3,
                                                        set_type = 0)
                book_set_id = book_set_query.id
            else:
                book_set_id = book_set_query[0].id
                option = [{"value":x,"title":"%d:00" % x} for x in range(7,22)]
                return JsonResponse({"code":0,"data":{"option":option,"book_set_id":book_set_id}})
        elif set_type == "custom":
            book_set_query = BookSet.objects.filter(coach_driver_school = \
                                                    CoachDriverSchool.objects.filter(coach = user.id)[0].id,
                                                    set_type = 1)
            if len(book_set_query) == 0:
                book_set_query = BookSet.objects.create(coach_driver_school =\
                                                        CoachDriverSchool.objects.get(coach = user.id),
                                                        num_student = 3,
                                                        set_type = 0)
                book_set_id = book_set_query.id
            else:
                book_set_id = book_set_query[0].id
                option = [{"value":x,"title":"%d:00" % x} for x in range(7,22)]
                return JsonResponse({"code":0,"data":{"option":option,"book_set_id":book_set_id}})
       

def booksets_all(request):
    if request.method == 'GET':
        token = request.GET.get("token")
        set_type = request.GET.get("set_type")
        date = request.GET.get("date")
        user = check_user(token)
        if user is {}:
            return JsonResponse({'code':500,"msg":"请重新登录"})
        if set_type == "default":
            book_set_query = BookSet.objects.filter(coach_driver_school = \
                                                    CoachDriverSchool.objects.filter(coach = user.id)[0].id,
                                                    set_type = 0)
            if len(book_set_query) == 0:
                book_set_query = BookSet.objects.create(coach_driver_school =\
                                                        CoachDriverSchool.objects.filter(coach = user.id),
                                                        num_student = 3,
                                                        set_type = 0)
                book_set_id = book_set_query.id
            else:
                book_set_id = [x.id for x in book_set_query]
                option = [{"value":x,"title":"%d:00" % x} for x in range(7,22)]
                return JsonResponse({"code":0,"data":{"option":option,"book_set_id":book_set_id}})
            
        elif set_type == 'custom':
            book_set_query = BookSet.objects.filter(coach_driver_school = \
                                                    CoachDriverSchool.objects.filter(coach = user.id)[0].id,
                                                    set_type = 1)
            if len(book_set_query) == 0:
                book_set_query = BookSet.objects.filter(coach_driver_school =\
                                                        CoachDriverSchool.objects.filter(coach = user.id)[0].id,
                                                        set_type = 0,
                                                        book_date_start = date)
                book_set_id = book_set_query[0].id
            else:
                coustom_set_id = [x.id for x in book_set_query]
                option = [{"value":x,"title":"%d:00" % x} for x in range(7,22)]
                return JsonResponse({"code":0,"data":{"option":option,"book_set_id":custom_set_id}})
 

def booksets_update(request):
    if request.method == 'GET':
        token = request.GET.get("token")
        set_id = request.GET.get("set_id")
        set_id = int(set_id) if isinstance(set_id,(str)) else set_id
        date_start = request.GET.get("date_start")
        date_end = request.GET.get("date_end")
        student_num = request.GET.get("student_num")
        student_num = int(student_num) if isinstance(student_num,(str)) else student_num
        user = check_user(token)
        if user is {}:
            return JsonResponse({"code":"500","msg":"请重新登录"})
        book_set_query = BookSet.objects.get(id = set_id)
        if student_num is not None and student_num <= book_set_query.num_student:
            book_set_query.num_student = student_num
        if date_start is not None:
            book_set_query.book_date_start = date_start
        if date_end is not None:
            book_set_query.book_date_end = date_end
        return JsonResponse({"code":0})


def forum_add(request):
    if request.method == 'GET':
        token = request.GET.get("token")
        title = request.GET.get("title")
        content = request.GET.get("content")
        topic = request.GET.get("topic")
        user = check_user(token)
        if user is {}:
            return JsonResponse({"code":500,"msg":"请重新登录"})
        forum_query = Forum.objects.create(user_id = user,
                                           title = title, 
                                           content = content, 
                                           topic = Topic.objects.get(name = title))
        return JsonResponse({"code":0,"msg":"帖子发表成功"})

