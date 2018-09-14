from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(WechatUser)
admin.site.register(Goods)
admin.site.register(DriverSchool)
admin.site.register(Attachment)
admin.site.register(Category)
admin.site.register(Icon)
admin.site.register(Coupons)
admin.site.register(Order)
admin.site.register(Shipper)
admin.site.register(OrderGoods)
admin.site.register(Logistics)
admin.site.register(Book)
admin.site.register(Bargain)
admin.site.register(Payment)
admin.site.register(GoodsReputation)
admin.site.register(BargainUser)
admin.site.register(BargainFriend)
admin.site.register(UserExam)
admin.site.register(CoachDriverSchool)

@admin.register(BookSet)
class BookSetAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'coach_driver_school',
                    'num_student',
                    'book_date_start',
                    'book_date_end',
                    'cur_book',
                    'status',
                    'set_type')

    list_per_page = 50

    ordering = ('-book_date_start',)

    list_editable = ['num_student','book_date_start','book_date_end']

    fk_fields = ('coach_driver_school')


admin.site.register(Address)
