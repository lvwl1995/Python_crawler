import re
import time
import pymysql
from lxml import etree
import requests


def get_areas(url):
    print('get areas')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(url, headers = headers)
    content = etree.HTML(resposne.text)
    infos = content.xpath("//div[@data-role='ershoufang']/div[1]/a")
    for info in infos:
        area = info.xpath('./text()')[0]
        area_link = info.xpath('./@href')[0]
        get_area_house(area,area_link)

def get_area_house(area,area_link):
    print('get page')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    url  = 'https://wh.lianjia.com' + area_link
    response = requests.get(url, headers = headers)
    pages = int(re.findall("page-data=\'{\"totalPage\":(\d+),\"curPage\"", response.text)[0])
    print('total page is:', pages)
    for page in range(1,pages + 1):
        link = url + 'pg' + str(page)
        print(link)
        get_house_info(area, link)
        print('write work done')
        print('\n\n' + '*' * 60)

def get_house_info(area, link):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    time.sleep(8)
    try:
        print('get house_page info')
        response = requests.get(link, headers = headers)
        content = etree.HTML(response.text)
        selllists = content.xpath("//div[@class='info clear']")
        print('wirte to database')
        for sell in selllists:
            try:
                title = sell.xpath("./div[@class='title']/a/text()")[0]
            except Exception as e:
                title = "no info"
            try:
                xiaoqu = sell.xpath(".//div[@class='houseInfo']/a/text()")[0]
            except Exception as e :
                xiaoqu = "no info"
            detail = sell.xpath(".//div[@class='houseInfo']/text()")[0].split('|')
            try:
                room_type = detail[1]
            except Exception as e:
                room_type = "no info"
            try:
                room_square = re.findall("(.*?)[\u4E00-\u9FA5]+", detail[2])[0]
            except Exception as e:
                room_square = "no info"
            try:
                direction = detail[3].replace(" ", "")
            except Exception as e:
                direction = "no info"
            try:
                decorate = detail[4]
            except Exception as e:
                decorate = "no info"
            try:
                lift = detail[5]
            except Exception as e:
                lift = "no info"
            try:
                detail_area = sell.xpath(".//div[@class='positionInfo']/a/text()")[0]
            except Exception as e:
                detail_area = "no info"
            floor_info = sell.xpath(".//div[@class='positionInfo']/text()")[0]
            try:
                floor_type = re.findall("([\u4E00-\u9FA5]+)\(", floor_info)[0]
            except Exception as e:
                floor_type = "no info"
            try:
                floor_counts = re.findall("\(共(\d+)层\)", floor_info)[0]
            except Exception as e:
                floor_counts = "no info"
            try:
                built_year = re.findall("\)(\d+)", floor_info)[0]
            except Exception as e:
                built_year = "no info"
            try:
                price = sell.xpath(".//div[@class='priceInfo']//div[@class='totalPrice']/span/text()")[0]
            except Exception as e:
                price = "no info"
            try:
                unit_price = re.findall("(\d+)", sell.xpath(".//div[@class='priceInfo']//div[@class='unitPrice']/span/text()")[0])[0]
            except Exception as e:
                unit_price = "no info"
            info = [area, title, xiaoqu,detail_area, room_type,room_square,decorate,direction,lift,floor_type, floor_counts, built_year, price, unit_price]
            write_to_database(info)
    except Exception as e:
        time.sleep(20)
        print('retrying..')
        return get_house_info(area, link)

def write_to_database(info):
    conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'root', db = 'wuhan',port=3306, charset='utf8')
    with conn.cursor() as cur:
        sql = '''INSERT INTO `second_hand` (area, title, xiaoqu,detail_area, room_type,room_square,decorate,direction,lift,floor_type, floor_counts, built_year, price, unit_price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, info)
        conn.commit()
        cur.close()
        conn.close()


def main():
    url  = 'https://wh.lianjia.com/ershoufang/'
    get_areas(url)

if __name__ == '__main__':
    main()
