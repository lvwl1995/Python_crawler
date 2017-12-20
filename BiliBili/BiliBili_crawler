import re
import time
import pymysql
import requests


def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    response = requests.get(url,headers = headers)
    html = response.text
    parse_content(html)

def parse_content(html):
    pattern = re.compile('.*?<d\sp=".*?(\d{10}).*?">(.*?)</d>',re.S)
    datas = re.findall(pattern, html)
    for data in datas:
        x = time.localtime(int(data[0]))
        send_date = time.strftime("%Y-%m-%d %H:%M:%S", x)
        comment = data[1]
        info = [send_date, comment]
        database(info)

def database(info):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db="bilibili", port=3306, charset='utf8')
    with conn.cursor() as cur:
        sql = '''INSERT INTO danmu (send_date, comment) VALUES (%s, %s)'''
        cur.execute(sql, info)
        conn.commit()
        cur.close()
        conn.close()


def main():
    for i in range(1481299200, 1513612800, 86400):
        url = 'https://comment.bilibili.com/dmroll,' + str(i) + ',11821166'
        get_page(url)



if __name__ == '__main__':
    main()
