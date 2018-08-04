from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import requests
# Create your views here.



def notice_list(request):
    return JsonResponse({"code":0,"data":{"totalRow":2,"totalPage":1,"dataList":[{"dateAdd":"2017-10-23 13:59:55","id":345,"isShow":true,"title":"天气又冷","userId":1614},{"dateAdd":"2017-10-23 13:59:44","id":344,"isShow":true,"title":"天气热","userId":1614}]},"msg":"success"})
