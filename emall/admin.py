from django.contrib import admin
from .models import *
# Register your models here.

#Goods admin
admin.site.register(Goods)
admin.site.register(Category)
admin.site.register(Preferential)
admin.site.register(GoodsReputation)


#Order admin
admin.site.register(DeliverWizard)
admin.site.register(Order)
admin.site.register(OrderGoods)
admin.site.register(Shipper)
admin.site.register(Logistics)

#Coupons admin
admin.site.register(Coupons)
admin.site.register(CouponsUser)
admin.site.register(Bargain)
admin.site.register(BargainUser)
admin.site.register(BargainFriend)
