import requests
from lxml import etree
import re
import time
import pymysql

def get_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    cookies = {
        'cookie': 'jid=7f0000015a5b870f18d640320310e002; gr_user_id=bacc5f32-a9d0-4a72-8336-d6c0578c9e60; __utmz=177471546.1515947793.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; city=wh; __ozlvd1020=1515948006; signsrc_last=WHHPFL_5_0; signsrc=WHHQFL_1_6%7CWHHPFL_5_0; _va_ref=%5B%22%22%2C%22%22%2C1516025477%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2LTi5uxXb_LHGTxUUkv69IAW8BjWkhR8URsbyuGMU8p9c0Bpx3ZrXy2lJJvEors0%26wd%3D%26eqid%3Dfe85213e00120481000000025a5b870a%22%5D; _va_ses=*; gr_session_id_b9a11927f241f255=34f27400-7161-4063-b4f3-2483a9ce2fde; __utma=177471546.11025460.1515947793.1516022693.1516025478.6; __utmc=177471546; __utmt=1; jhu=ARRNOLiM9b8IBFZ4eyz%2FAVhfSHPmjP68DBpUe2Mq%2BxlUBwxi%2FoLt%2BlRZA253KfocTAcJY%2B2b%2BvMbBVF%2Fe32sTkMBXjW4yqu8WQxSeXl8%2Fx9OAgFgv5mtvV4%3D; index_tad_bighome=true; __utmv=177471546.|1=site-IP-420100=121.27.244.143=1^2=site-LOGIN-420100=yes=1; ordersrc_last=WHIndexFL_1_0; ordersrc=WHHPFL_5_0%7CWHIndexFL_1_0; source_last=WHIndexFL_1_0; source=WHHPFL_5_0%7CWHIndexFL_1_0; channel_src_last=pd_hunshasheying; channel_src=home_hbs%7Cpd_hunshasheying; gr_cs1_34f27400-7161-4063-b4f3-2483a9ce2fde=userId%3A15004640; _va_id=f6ef9d4f8c0a6c66.1515947792.6.1516025789.1516025477.; __utmb=177471546.16.8.1516025753418'}

    try:
        response = requests.get(url, headers=headers, cookies=cookies)
    except Exception as e:
        time.sleep(20)
        print("get page error, retrying")
        return get_page(url)
    content = etree.HTML(response.text)
    pages = int(re.findall("_p(\d+)" ,content.xpath("//li[@class='l']/a/@href")[0])[0])
    for page in range (1,pages + 1):
        url = 'https://wh.jiehun.com.cn/xiyanjiudian/storelists_p' +  str(page)
        get_links(url)


def get_links(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    cookies = {
        'cookie': 'jid=7f0000015a5b870f18d640320310e002; gr_user_id=bacc5f32-a9d0-4a72-8336-d6c0578c9e60; __utmz=177471546.1515947793.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; city=wh; __ozlvd1020=1515948006; signsrc_last=WHHPFL_5_0; signsrc=WHHQFL_1_6%7CWHHPFL_5_0; _va_ref=%5B%22%22%2C%22%22%2C1516025477%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2LTi5uxXb_LHGTxUUkv69IAW8BjWkhR8URsbyuGMU8p9c0Bpx3ZrXy2lJJvEors0%26wd%3D%26eqid%3Dfe85213e00120481000000025a5b870a%22%5D; _va_ses=*; gr_session_id_b9a11927f241f255=34f27400-7161-4063-b4f3-2483a9ce2fde; __utma=177471546.11025460.1515947793.1516022693.1516025478.6; __utmc=177471546; __utmt=1; jhu=ARRNOLiM9b8IBFZ4eyz%2FAVhfSHPmjP68DBpUe2Mq%2BxlUBwxi%2FoLt%2BlRZA253KfocTAcJY%2B2b%2BvMbBVF%2Fe32sTkMBXjW4yqu8WQxSeXl8%2Fx9OAgFgv5mtvV4%3D; index_tad_bighome=true; __utmv=177471546.|1=site-IP-420100=121.27.244.143=1^2=site-LOGIN-420100=yes=1; ordersrc_last=WHIndexFL_1_0; ordersrc=WHHPFL_5_0%7CWHIndexFL_1_0; source_last=WHIndexFL_1_0; source=WHHPFL_5_0%7CWHIndexFL_1_0; channel_src_last=pd_hunshasheying; channel_src=home_hbs%7Cpd_hunshasheying; gr_cs1_34f27400-7161-4063-b4f3-2483a9ce2fde=userId%3A15004640; _va_id=f6ef9d4f8c0a6c66.1515947792.6.1516025789.1516025477.; __utmb=177471546.16.8.1516025753418'}

    response = requests.get(url, headers=headers, cookies=cookies)
    ends = re.findall('<div class="bigpic g-f"><a href="(.*?)">', response.text)
    for end in ends:
        url = 'https://wh.jiehun.com.cn' + end
        parse_info(url)

def parse_info(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    cookies = {
        'cookie': 'jid=7f0000015a5b870f18d640320310e002; gr_user_id=bacc5f32-a9d0-4a72-8336-d6c0578c9e60; __utmz=177471546.1515947793.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; city=wh; __ozlvd1020=1515948006; signsrc_last=WHHPFL_5_0; signsrc=WHHQFL_1_6%7CWHHPFL_5_0; _va_ref=%5B%22%22%2C%22%22%2C1516025477%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2LTi5uxXb_LHGTxUUkv69IAW8BjWkhR8URsbyuGMU8p9c0Bpx3ZrXy2lJJvEors0%26wd%3D%26eqid%3Dfe85213e00120481000000025a5b870a%22%5D; _va_ses=*; gr_session_id_b9a11927f241f255=34f27400-7161-4063-b4f3-2483a9ce2fde; __utma=177471546.11025460.1515947793.1516022693.1516025478.6; __utmc=177471546; __utmt=1; jhu=ARRNOLiM9b8IBFZ4eyz%2FAVhfSHPmjP68DBpUe2Mq%2BxlUBwxi%2FoLt%2BlRZA253KfocTAcJY%2B2b%2BvMbBVF%2Fe32sTkMBXjW4yqu8WQxSeXl8%2Fx9OAgFgv5mtvV4%3D; index_tad_bighome=true; __utmv=177471546.|1=site-IP-420100=121.27.244.143=1^2=site-LOGIN-420100=yes=1; ordersrc_last=WHIndexFL_1_0; ordersrc=WHHPFL_5_0%7CWHIndexFL_1_0; source_last=WHIndexFL_1_0; source=WHHPFL_5_0%7CWHIndexFL_1_0; channel_src_last=pd_hunshasheying; channel_src=home_hbs%7Cpd_hunshasheying; gr_cs1_34f27400-7161-4063-b4f3-2483a9ce2fde=userId%3A15004640; _va_id=f6ef9d4f8c0a6c66.1515947792.6.1516025789.1516025477.; __utmb=177471546.16.8.1516025753418'}

    try:
        response = requests.get(url, headers=headers, cookies=cookies)
    except Exception as e:
        time.sleep(20)
        print("连接出错，正在重试")
        return  parse_info(url)

    content = etree.HTML(response.text)
    print(url)
    try:
        name = content.xpath("//div[@class='store_info']/h3/text()")[0].strip()
    except Exception as e:
        name = "no info"

    try:
        price = re.findall("(\d+\-?\d+)",content.xpath("//div[@class='store_info']/div/text()")[0].strip())[0]
    except Exception as e:
        price = ""

    try:
        type = re.findall("酒店类型.*?([\u4E00-\u9FA5]+)",content.xpath('//p[@class="leixing"]/span/text()')[0])[0]
    except Exception as e:
        type = ""

    try:
        storage = re.findall("容纳桌数.*?(\d+)",content.xpath('//p[@class="leixing"]/span/text()')[1])[0]
    except Exception as e:
        storage = ""

    try:
        halls = re.findall("(\d+)",content.xpath('//*[@id="jd_yanhuiting"]/div/div[1]/h3/text()')[0])[0]
    except Exception as e:
        halls = ''

    try:
        address = content.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/p[2]/span/text()')[0]
    except Exception as e:
        address = ""

    try:
        phone_num = re.findall("联系电话.*?(\d+\-\d+)",content.xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[1]/text()')[0])[0]
    except Exception as e:
        phone_num = ""

    try:
        good = re.findall("好评.*?(\d+)",content.xpath('//*[@id="jd_userdp"]/div[2]/div[2]/a[2]/text()')[0])[0]
    except Exception as e:
        good = '0'

    try:
        ok = re.findall("中评.*?(\d+)",content.xpath('//*[@id="jd_userdp"]/div[2]/div[2]/a[3]/text()')[0])[0]
    except Exception as e:
        ok = '0'

    try:
        bad =  re.findall("差评.*?(\d+)",content.xpath('//*[@id="jd_userdp"]/div[2]/div[2]/a[4]/text()')[0])[0]
    except Exception as e:
        bad = '0'

    info = [name,price,type,storage,halls,good,ok,bad,address,phone_num]
    print(info)
    write_to_database(info)

def write_to_database(info):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', port=3306, db='wuhan', charset='utf8')
    with conn.cursor() as cur:
        sql = '''INSERT INTO `hotel` (name,price,type,storage,halls,good,ok,bad,address,phone_num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cur.execute(sql, info)
        conn.commit()
        cur.close()
        conn.close()



def main():
    url = 'https://wh.jiehun.com.cn/xiyanjiudian/storelists'
    get_page(url)

if __name__ == '__main__':
    main()