import os
from Crypto.Cipher import AES
import base64
import codecs
import json
import time
import pymysql
import requests

def aesEncrypt(text, secKey):
	pad = 16 - len(text) % 16
	#print(type(text))
	#print(type(pad))
	#print(type(pad * chr(pad)))
	#text = text + str(pad * chr(pad))
#这里有转换type和str，上面的print是为了看清楚类型
	if isinstance(text,bytes):
		#print("type(text)=='bytes'")
		text=text.decode('utf-8')
		#print(type(text))
	text = text  + str(pad * chr(pad))
	encryptor = AES.new(secKey, 2, '0102030405060708')
	ciphertext = encryptor.encrypt(text)
	ciphertext = base64.b64encode(ciphertext)
	return ciphertext

def rsaEncrypt(text, pubKey, modulus):
	text = text[::-1]
#hex不是这么用	rs = int(text.encode('hex'), 16)**int(pubKey, 16)%int(modulus, 16)
	rs = int(codecs.encode(text.encode('utf-8'),'hex_codec'), 16)**int(pubKey, 16)%int(modulus, 16)
	return format(rs, 'x').zfill(256)

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'

def createSecretKey(size):
	return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


def post_data(start,end):
	print("正在写入前" + str(end * 10) + '条评论....')
	time.sleep(0.5)
	for i in range(start,end):
		# 一个i获取10个评论
		text = {
			'username': '',
			'password': '',
			'rememberLogin': 'true',
			'offset': i * 10
		}
		text = json.dumps(text)
		secKey = createSecretKey(16)
		encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
		encSecKey = rsaEncrypt(secKey, pubKey, modulus)
		payload = {
			'params': encText,
			'encSecKey': encSecKey
		}
		get_page(payload,start, end)
	start = end
	end += 10 #往下抓取，直到最后一页
	return post_data(start, end)


def get_page(payload, start, end):
	url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_186016?csrf_token=03eb22333046910c36968e61c054405d'
	headers = {'User-Agent':'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11'}
	try:
		response = requests.post(url, headers = headers, data = payload)
		#fp = codecs.open("test.json", "a", "utf-8")
		#fp.write(response.text + '\n')
		#parse(data)
		jsons = json.loads(response.text)
		hot = jsons.get("comments")
		test = jsons.get('more')
		print(response.text)

		if test == True:#检测是否有下一页，若有，程序往下执行
			for data in hot:
				nickname = data.get('user').get('nickname')
				likedcount = data.get('likedCount')
				content = data.get('content')
				timeinfo = int(data.get('time')/1000)
				sent_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timeinfo))
				info = [nickname, sent_time, content, likedcount]
				database(info)
		else:
			print("评论抓取完毕")
	except Exception as e:#防止意外退出，返回抓取程序重试
		time.sleep(20)
		print("重试请求")
		print(start, end)
		return post_data(start, end)

def database(info):
	con = pymysql.connect(host = 'localhost', user = 'root', password = 'root', db = 'netease', port = 3306, charset = 'utf8')
	with con.cursor() as cur:
		sql = '''INSERT INTO `comments` (nickname, sent_time, content, likedcount) VALUES (%s, %s, %s, %s)'''
		cur.execute(sql, info)
		con.commit()
		cur.close()


def main():
	post_data(start = 0, end =10)#设置起始于抓取范围，抓取出长度（程序执行一次，实现抓取评论100条）

if __name__ =='__main__':
	main()
