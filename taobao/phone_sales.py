# -*- coding: UTF-8 -*-
import time
import re
import pymysql
import json
from urllib.parse import urlencode
import requests
from urllib3.exceptions import ReadTimeoutError

def get_mode_link(url):
#首先获得所有品牌对应的value值,组合成品牌页面链接
    cookies = {'cookie': 't=359a7e91db5703918a7df2665c5bf62b; cna=bP60Eg2cS1kCAXkb9L01Ca65; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=5934149081693019334; uc3=nk2=tbh9N9f5pw%3D%3D&id2=UU6lRDiHJNXzlQ%3D%3D&vt3=F8dBzLbWAC6%2BM5L4d2g%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu716E%5Cu6D77lwl; tracknick=%5Cu716E%5Cu6D77lwl; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=6_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=f7aede696e5248a89f92c64bade0a4ad_1513920502585; _m_h5_tk_enc=5b1e939666d8cba41b0f6c7d31ec11a6; swfstore=151068; cookie2=250d7cd944d6e6957d645cb10b092b5e; v=0; _tb_token_=ff37713f37e8f; uc1=cookie14=UoTdf1DO8qiM0g%3D%3D; JSESSIONID=09E7282D493498E5D076E7F925CF9131; isg=AgkJZBdSt4cEL0tjButzcxruGDWj_v3sY1jAiat-hfAv8ikE86YNWPeoSGA_'}
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    band_response = requests.get(url, headers = headers,cookies = cookies)
    data = re.findall('g_page_config =\s(.*?),{"text":"尺寸"',band_response.text)[0]
    values = re.findall(',"value":"(.*?)","trace', data)
    for value in values[:11]:
        url = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&ppath=' + str(value)
        get_shop_lists(url)


def get_shop_lists(url):
    # 根据品牌页面链接，进入品牌页面，获取每个品牌的所有机型的商店列表链接
    cookies = {
        'cookie': 't=359a7e91db5703918a7df2665c5bf62b; cna=bP60Eg2cS1kCAXkb9L01Ca65; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=5934149081693019334; uc3=nk2=tbh9N9f5pw%3D%3D&id2=UU6lRDiHJNXzlQ%3D%3D&vt3=F8dBzLbWAC6%2BM5L4d2g%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu716E%5Cu6D77lwl; tracknick=%5Cu716E%5Cu6D77lwl; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=6_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=f7aede696e5248a89f92c64bade0a4ad_1513920502585; _m_h5_tk_enc=5b1e939666d8cba41b0f6c7d31ec11a6; swfstore=151068; cookie2=250d7cd944d6e6957d645cb10b092b5e; v=0; _tb_token_=ff37713f37e8f; uc1=cookie14=UoTdf1DO8qiM0g%3D%3D; JSESSIONID=09E7282D493498E5D076E7F925CF9131; isg=AgkJZBdSt4cEL0tjButzcxruGDWj_v3sY1jAiat-hfAv8ikE86YNWPeoSGA_'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    shop_response = requests.get(url, headers=headers, cookies=cookies)
    data = re.findall('"pager":{"status":.*?},"grid":(.*?),"header":', shop_response.text)[0]
    shop_lists = re.findall('"num":"\d+"},"url":"\/\/(.*?grid)","tag_info', data)
    shop_links = []
    for shop_list in shop_lists:
        # 获得的链接为unicode编码，无法正常访问，需要转码
        shop_link = "http://" + shop_list.encode('utf-8').decode('unicode_escape')
        shop_links.append(shop_link)
    get_page_link(shop_links)


def get_page_link(shop_links):
    for shop_link in shop_links:
        for i in range(13):
            pager = i * 44
            data = {'bcoffset': 4,
                    'p4ppushleft': '6,48',
                    's': pager
                    }
            page_link = shop_link + "&" + urlencode(data)
            get_ids(page_link)


def get_ids(page_link):
    cookies = {
        'cookie': 't=359a7e91db5703918a7df2665c5bf62b; cna=bP60Eg2cS1kCAXkb9L01Ca65; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=5934149081693019334; uc3=nk2=tbh9N9f5pw%3D%3D&id2=UU6lRDiHJNXzlQ%3D%3D&vt3=F8dBzLbWAC6%2BM5L4d2g%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu716E%5Cu6D77lwl; tracknick=%5Cu716E%5Cu6D77lwl; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=6_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=f7aede696e5248a89f92c64bade0a4ad_1513920502585; _m_h5_tk_enc=5b1e939666d8cba41b0f6c7d31ec11a6; swfstore=151068; cookie2=250d7cd944d6e6957d645cb10b092b5e; v=0; _tb_token_=ff37713f37e8f; uc1=cookie14=UoTdf1DO8qiM0g%3D%3D; JSESSIONID=09E7282D493498E5D076E7F925CF9131; isg=AgkJZBdSt4cEL0tjButzcxruGDWj_v3sY1jAiat-hfAv8ikE86YNWPeoSGA_'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    try:
        page_response = requests.get(page_link, headers=headers, cookies=cookies, timeout=10)
        try:
            infos = re.findall('"mods":({"feedback".*?}}}),"mainInfo"', page_response.text)[0]
            sales_info = json.loads(infos)
            shop_infos = sales_info['itemlist']['data']['auctions']
            n = 0
            band = re.findall('([\u4E00-\u9FA5]+)\s',sales_info['spuhead']['data']['spuTitle'])[0]
            print(band)
            model = sales_info['spuhead']['data']['spuTitle']
            for shop_info in shop_infos:
                n += 1
                nickname = shop_info['nick']
                price = shop_info['view_price']
                try:
                    comments = str(shop_info['comment_count'])
                except Exception as e:
                    comments = "无数据"
                itemid = shop_info['nid']
                sellerid = shop_info['user_id']
                info = [band, model,  nickname]
                get_comments_pages(itemid, sellerid,info)
            print("第" + str(n) +"家店铺评论写入完毕，继续下一家")
            print(n)
            print("该页数据入库完毕，继续写入下一页" + "--" * 60 + "\n\n\n")
        except ReadTimeoutError:
            print("重试请求")
            time.sleep(10)
            return get_ids(page_link)
    except Exception as e:
        print("该页面无数据，继续下一页")

def get_comments_pages(itemid, sellerid, info):
    cookies = {
        'cookie': 't=359a7e91db5703918a7df2665c5bf62b; cna=bP60Eg2cS1kCAXkb9L01Ca65; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=5934149081693019334; uc3=nk2=tbh9N9f5pw%3D%3D&id2=UU6lRDiHJNXzlQ%3D%3D&vt3=F8dBzLbWAC6%2BM5L4d2g%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu716E%5Cu6D77lwl; tracknick=%5Cu716E%5Cu6D77lwl; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=6_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=f7aede696e5248a89f92c64bade0a4ad_1513920502585; _m_h5_tk_enc=5b1e939666d8cba41b0f6c7d31ec11a6; swfstore=151068; cookie2=250d7cd944d6e6957d645cb10b092b5e; v=0; _tb_token_=ff37713f37e8f; uc1=cookie14=UoTdf1DO8qiM0g%3D%3D; JSESSIONID=09E7282D493498E5D076E7F925CF9131; isg=AgkJZBdSt4cEL0tjButzcxruGDWj_v3sY1jAiat-hfAv8ikE86YNWPeoSGA_'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=' + str(itemid) + '&sellerId=' + str(sellerid) + '&currentPage=1'
    response = requests.get(url, headers = headers, cookies = cookies)
    pages = int(re.findall('"lastPage":(\d+),"page"', response.text)[0])
    print(pages)
    for page in range(1, pages + 1):
        print("开始写入第" + str(page) + "页评论")
        get_comments(page,itemid, sellerid,info)

def get_comments(page,itemid, sellerid,info):
    cookies = {
        'cookie': 't=359a7e91db5703918a7df2665c5bf62b; cna=bP60Eg2cS1kCAXkb9L01Ca65; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; miid=5934149081693019334; uc3=nk2=tbh9N9f5pw%3D%3D&id2=UU6lRDiHJNXzlQ%3D%3D&vt3=F8dBzLbWAC6%2BM5L4d2g%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu716E%5Cu6D77lwl; tracknick=%5Cu716E%5Cu6D77lwl; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=6_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=f7aede696e5248a89f92c64bade0a4ad_1513920502585; _m_h5_tk_enc=5b1e939666d8cba41b0f6c7d31ec11a6; swfstore=151068; cookie2=250d7cd944d6e6957d645cb10b092b5e; v=0; _tb_token_=ff37713f37e8f; uc1=cookie14=UoTdf1DO8qiM0g%3D%3D; JSESSIONID=09E7282D493498E5D076E7F925CF9131; isg=AgkJZBdSt4cEL0tjButzcxruGDWj_v3sY1jAiat-hfAv8ikE86YNWPeoSGA_'}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    comment_url ='https://rate.tmall.com/list_detail_rate.htm?itemId=' + str(itemid) + '&sellerId=' + str(sellerid) + '&currentPage=' + str(page)
    try:
        response = requests.get(comment_url, headers = headers, cookies = cookies)
        print(response.status_code)
        jsons = re.findall('"rateDetail":({.*?"tags":""})', response.text)[0]
        comment_lists = json.loads(jsons)['rateList']
        for comment in comment_lists:
            plat = comment['cmsSource']
            color = re.findall('机身颜色:([\u4E00-\u9FA5]+);',comment['auctionSku'])[0]
            storage = re.findall('存储容量:(\w+)', comment['auctionSku'])[0]
            ratedate = comment['rateDate']
            content = comment['rateContent']
            detail_infos = [plat, info[0],info[1],info[2], color, str(storage), ratedate, content]
            write_to_database(detail_infos)
        print("第" + str(page) +"页评论写入完毕，继续下一页" + '\n\n' + '*' * 60)
    except Exception as e:
        print("重试写入第" + str(page) + "页")
        print('*' * 60 + '\n\n')
        time.sleep(5)
        return get_comments(page,itemid, sellerid,info)
def write_to_database(detail_infos):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db="taobao", port=3306, charset='utf8')
    with conn.cursor() as cur:
        sql = '''INSERT INTO `detail_info` (plat, band, model,nickname, color, storage, ratedate, content) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, detail_infos)
        conn.commit()
        cur.close()
        conn.close()


def main():
#程序入口
    url = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&ppath='
    print("任务开始")
    get_mode_link(url)

if __name__ == '__main__':
    main()
