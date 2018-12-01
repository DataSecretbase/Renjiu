"""
province,city,district data
"""


"""
user
"""
USER_TYPE = [(0,"普通用户"),(1,"店主"),(2,"教练")]


"""
Logistics
"""

LogisticsValuationMethod = [(0,'顺丰快递方式')]




"""
payment
"""
PAYMENT_STATUS = [(0,"支付已完成"),(1,"待用户支付"),(2,"支付已关闭"),(3,"退款")]


"""
reputation
"""

REPUTATION_STR = [(0,'特别好评'),(1,'好评'),(2,'中评'),(3,'差评')]

"""
bargain
"""

BARGAIN_CALCULATE_METHOD = [(0,"line"),(1,"log")]

"""
exam
"""
EXAM_STATUS = [(0,"考试未报名"),
               (1,"考试已报名"),
               (2,"考试已经停止预约"),
               (3,"考试已经结束")]

EXAM_TYPE = [(0,"科目一"),
             (1,"科目二"),
             (2,"科目三"),
             (3,"科目四")]

"""
book_set
"""

BOOK_SET_TYPE = [(0,"默认设置"),(1,"特定设置")]

ORDER_TYPE = [(0,"直销订单"),(1,"分销订单")]