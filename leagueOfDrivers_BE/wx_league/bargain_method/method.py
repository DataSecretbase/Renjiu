import math


#@times 期望次数
#@change 期望变化值
def method_log(exp_times, cur_times,change):
    return math.log(cur_times+1,exp_times)*change
