#coding=utf-8
__author__ = 'tianqianwen'
import re
import sys
sys.path.append('/root/mini_ximi/test')





def read():
	with open("/root/Renjiu/mini_ximi/test/log_2018-07-12.txt") as f:
		line = f.readline()
		line += f.readline()
		lists = re.findall(r'[[](.*?)[]]',line.replace('\n',''))
	gpslists = lists[1].split(',')
	msg = {
		'time':lists[0],
		'gpsformat':gpslists[0],
		'utc':gpslists[1],
		'N':gpslists[2],
		'E':gpslists[4],
		'qualityFactor':gpslists[6], #质量因子：(0=没有定位，1=实时GPS，2=差分GPS)：1=实时GPS；
		'numAvaiSatel':gpslists[7], #可使用的卫星数：(0～8)：可使用的卫星数=07；
		'horPreciFactor':gpslists[8], #水平精度因子：(1.0～99.9)；水平精度因子=1.4;
		'anteElevation':gpslists[9], #天线高程：(海平面，－9999.9～99999.9，单位：m)；天线高程=76.2m);
		'heightSeaLevel':gpslists[11], #大地椭球面相对海平面的高度：(－999.9～9999.9，单位：m):－7.0m;
		'difGPSDataAge':gpslists[12], #差分GPS数据年龄，实时GPS时无：无;   
		'checkSum':gpslists[13], #差分GPS数据年龄，实时GPS时无：无
	}
	return msg

if __name__ == '__main__':
	read()
