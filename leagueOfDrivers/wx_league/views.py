from django.shortcuts import render
from django.http import JsonResponse
from .models import *
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

