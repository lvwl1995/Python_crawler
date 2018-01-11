import requests
import time
import re
import pymysql
from lxml import etree

# get areas
def get_areas(url):
    print('start grabing areas')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(url, headers=headers)
    content = etree.HTML(resposne.text)
    areas = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/text()")
    areas_link = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/@href")
    for i in range(9,len(areas)):
        area = areas[i]
        area_link = areas_link[i]
        link = 'https://wh.lianjia.com' + area_link
        print('start grabing pages')
        get_pages(area, link)

def get_pages(area,area_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(area_link, headers=headers)
    pages =  int(re.findall("page-data=\'{\"totalPage\":(\d+),\"curPage\"", resposne.text)[0])
    print('this area has ' + str(pages) + ' pages')
    for page in range(42,pages+1):
        url = 'https://wh.lianjia.com/zufang/jiangan/pg' + str(page)
        print('start grabing the ' + str(page) +' page`s info')
        get_house_info(area,url)

def get_house_info(area, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    time.sleep(2)
    try:
        resposne = requests.get(url, headers=headers)
        content = etree.HTML(resposne.text)
        for i in range(30):
            title = content.xpath("//div[@class='where']/a/span/text()")[i]
            room_type = content.xpath("//div[@class='where']/span[1]/span/text()")[i]
            square = re.findall("(\d+)",content.xpath("//div[@class='where']/span[2]/text()")[i])[0]
            position = content.xpath("//div[@class='where']/span[3]/text()")[i].replace(" ", "")
            detail_place = re.findall("([\u4E00-\u9FA5]+)租房", content.xpath("//div[@class='other']/div/a/text()")[i])[0]
            floor =re.findall("([\u4E00-\u9FA5]+)\(", content.xpath("//div[@class='other']/div/text()[1]")[i])[0]
            total_floor = re.findall("(\d+)",content.xpath("//div[@class='other']/div/text()[1]")[i])[0]
            try:
                house_year = re.findall("(\d+)",content.xpath("//div[@class='other']/div/text()[2]")[i])[0]
            except Exception as e:
                house_year = ""
            others = content.xpath("//div[@class='left agency']/div")[i]
            try:
                tags =re.findall("(.*?)随时看房",others.xpath("string(.)"))[0]
            except Exception as e:
                tags = "no tags"
            price = content.xpath("//div[@class='col-3']/div/span/text()")[i]
            info = [area,title, detail_place,room_type, square,position, floor, total_floor, house_year,price,tags]
            print('start writing into database!')
            write_to_database(info)
            print('writing work has done!continue the next page')
    except Exception as e:
        print( 'ooops! connecting error, retrying.....')
        time.sleep(20)
        return get_house_info(area, url)

def write_to_database(info):
    conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'root', db = 'wuhan', port = 3306,charset = 'utf8')
    with conn.cursor() as cur:
        sql = '''INSERT INTO `rent_info`(area,title, detail_place,room_type, square,position, floor, total_floor, house_year,price,tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, info)
        conn.commit()
        cur.close()
        conn.close()
    print()


def main():
    print('start!')
    url = 'https://wh.lianjia.com/zufang'
    get_areas(url)


if __name__ == '__main__':
    main()
