import re
import json
import time
import random
import pymysql
import requests
from lxml import etree
from urllib.parse import urlencode
from requests.exceptions import RequestException

# 日志文件，记录已经写入的电影链接，用来检测爬虫写入断点，进行断点续写
def log(url):
    with open('database_record.txt', 'a') as f:
        f.write(url)


# 根据每页不同的请求信息，获取该页完整链接
def get_full_url():
    formdata = {
        'sort': 'T',
        'range': "m,n",
        'tags': '电影',
        'start': '0'
    }
    scores = [ '9,10', '8,9','7.6, 8','7,3,7.6','7,7.3','6.7, 7','6.5, 6.7','6,6.5','5,6', '4,5', '3,4','2,3']
    for score in scores:
        formdata['range'] = score
        for i in range(0, 9980, 20):
            start = str(i)
            formdata['range'] = score
            formdata['start'] = start
            print(formdata)
            url = 'http://movie.douban.com/j/new_search_subjects?' + urlencode(formdata)
            print(url)
            get_index_page(url)


# 根据每页完整链接获取该页中电影条目的详细信息链接
def get_index_page(url):
    cookie = {
        'Cookie': 'll="118092"; bid=S5M6I5PXpj8; ps=y; __utma=30149280.1057479541.1512968178.1512968178.1512968178.1; __utmc=30149280; __utmz=30149280.1512968178.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(None); __utmt=1; dbcl2="125320590:xDmmYhWhNsg"; ck=UE0G; __utmb=30149280.3.10.1512968178; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1512968629%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1347479279.1512968629.1512968629.1512968629.1; __utmb=223695111.0.10.1512968629; __utmc=223695111; __utmz=223695111.1512968629.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=5mCvcnYee9jnIMy6f3g4lsNEjDBjWoXI; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=2EDA87C514C29173312AC25A9A881EF5|c1de8a2ca73b3d5c98ec6ac396f6cde0; ap=1; _pk_id.100001.4cf6=a46ff7dcf8699618.1512968629.1.1512968661.1512968629.'}
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'}

    try:
        response = requests.get(url, headers=headers, cookies=cookie)
        if response.status_code == 200:
            html = json.loads(response.text)
            print('已获得html')  # 检测程序运行状况
            get_movie_url(html)
        return None
    except RequestException:
        return None


# 根据电影索引页面内容，获取该页电影的全部链接，每页包含20个。
def get_movie_url(html):
    datas = html.get('data')
    urls = []
    for data in datas:
        url = data.get('url')
        urls.append(url)
    print("以获取urls")
    get_movie_page(urls)


# 根据得到的电影链接获取电影详细信息页面
def get_movie_page(urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    cookie = {
        'Cookie': 'll="118092"; bid=S5M6I5PXpj8; ps=y; __utma=30149280.1057479541.1512968178.1512968178.1512968178.1; __utmc=30149280; __utmz=30149280.1512968178.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(None); __utmt=1; dbcl2="125320590:xDmmYhWhNsg"; ck=UE0G; __utmb=30149280.3.10.1512968178; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1512968629%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1347479279.1512968629.1512968629.1512968629.1; __utmb=223695111.0.10.1512968629; __utmc=223695111; __utmz=223695111.1512968629.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=5mCvcnYee9jnIMy6f3g4lsNEjDBjWoXI; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=2EDA87C514C29173312AC25A9A881EF5|c1de8a2ca73b3d5c98ec6ac396f6cde0; ap=1; _pk_id.100001.4cf6=a46ff7dcf8699618.1512968629.1.1512968661.1512968629.'}

    # 检测程序断点,检测遗漏的连接并补上。接着上次断开的那个网址继续下载
    with open('database_record.txt', 'r') as f:
        datas = f.readline()
    print('检查要下载文件是否已经在库中:')
    for url in urls:
        print("文件链接为url:", url)
        if url.strip('\n') in datas:
            print('该url已存在,检测下一个url...' + '\n')
            continue
        else:
            print('未检测到此条url对应的文件' + '\n' + '程序将继续往下执行')
            pass

            # 断点检测完毕，继续下载写入文件
            nap = random.uniform(2.2, 4.8)
            time.sleep(nap)
            response = requests.get(url, headers=headers, cookies=cookie)
            sec = response.elapsed.seconds
            print(response.status_code, sec)
            html = response.text
            print('得到html')  # 检测程序运行情况
            get_info(html, url)


# 根据获取的电影详细信息页面，获取我们想要的信息
def get_info(html, url):
    content = etree.HTML(html)
    print('开始写入')

    # 电影有不同程度的数据缺失，这里引入异常，防止程序意外退出
    try:
        titles = re.findall('.*?([\u4e00-\u9fa5]+).*?',content.xpath('//span[@property="v:itemreviewed"]/text()')[0])[0]
    except IndexError:
        titles = 'no info'

    try:
        tags = [','.join(content.xpath('//div[@class="tags-body"]/a/text()'))][0]
    except IndexError:
        tags = 'no info'

    try:
        region = re.findall('.*?<span\sclass="pl">.*?[\u4e00-\u9fa5]{4}\/[\u4e00-\u9fa5]{2}:</span>.*?([A-Za-z]+|[\u4e00-\u9fa5]+).*?<br/>',html)[0]
    except IndexError:
        region = 'no info'

    try:
        gerne = [','.join(content.xpath('//span[@property="v:genre"]/text()'))][0]
    except IndexError:
        gerne = 'no info'

    try:
        release_time = re.findall('^([0-9]{4}).*?', content.xpath('//span[@property="v:initialReleaseDate"]/text()')[0])[0]
    except IndexError:
        release_time = 0

    try:
        times = re.findall('.*?<span class="pl">[\u4e00-\u9fa5]{2}:</span>.*?(\d+).*?', html)[0]
    except IndexError:
        times = 0

    try:
        score = content.xpath('//strong[@property="v:average"]')[0].text
    except IndexError:
        score = 0.0

    try:
        score_numbers = content.xpath('//span[@property="v:votes"]')[0].text
    except IndexError:
        score_numbers = 0
    try:
        comments_num = re.findall('.*?([0-9]+).*?',content.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')[0])[0]
    except IndexError:
        comments_num= 0

    try:
        director = content.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
    except IndexError:
        director = 'no info'

    try:
        five_stars = content.xpath('//span[@class="rating_per"]')[0].text
    except IndexError:
        five_stars = 'no info'

    try:
        four_stars = content.xpath('//span[@class="rating_per"]')[1].text
    except IndexError:
        four_stars = 'no info'

    try:
        three_stars = content.xpath('//span[@class="rating_per"]')[2].text
    except IndexError:
        three_stars = 'no info'

    try:
        two_stars = content.xpath('//span[@class="rating_per"]')[3].text
    except IndexError:
        two_stars = 'no info'

    try:
        one_star = content.xpath('//span[@class="rating_per"]')[4].text
    except IndexError:
        one_star = 'no info'
	#将获得的信息写入本地数据库
    conn = pymysql.connect(host = '127.0.0.1',user = 'root',password = 'root',db = "movies",port = 3306,charset='utf8')
    data = [titles, release_time, region, director, times, tags, gerne,  score, score_numbers,comments_num, five_stars,four_stars, three_stars, two_stars, one_star]

    with conn.cursor() as cur:
        sql = '''INSERT INTO movie_info (titles, release_time, region, director,  times, tags, gerne, score, score_numbers,comments_num, five_stars,four_stars, three_stars, two_stars, one_star) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, data)
        # 提交
        conn.commit()
        cur.close()
        conn.close()
        log(url)  # 将已经写入的电影链接存入log文件备用
        print("此url已写入log文件" + '\n' + '-' * 60 + '\n\n\n')


# 主程序入口
def main():
    get_full_url()


if __name__ == '__main__':
    main()
