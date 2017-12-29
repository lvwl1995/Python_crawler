import requests
from lxml import etree

#获取包含图片链接的页面
def get_one_page(url):
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    response = requests.get(url, headers = headers)
    html = response.text
    get_img_link(html)

#从返回的页面中抽取图片链接
def get_img_link(html):
    content = etree.HTML(html)
    link_lists = content.xpath('//div[@class="cover"]/a/img/@src')
    download_img(link_lists)

#通过抽取的图片链接下载图片
def download_img(link_lists):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    for link in link_lists:
        file_name = link[-14:]
        response = requests.get(link, headers = headers, stream = True)
        content = response.content
        with open('D:/LearnPython/python_crawler/BeiGuoZhiLian/pictures/' + file_name, 'wb') as f:
            f.write(content)

#主程序入口
def main(url):

    get_one_page(url)

if __name__ == '__main__':
    id = str(input('请输入作品id：'))
    n = int(input("请输入起始页码数："))
    m = int(input("请输入结束页码数："))
    for i in range(n, m + 1):
        url = 'https://movie.douban.com/subject/' + id + '/photos?type=S&start=' + str(
            (i - 1) * 30) + '&sortby=like&size=a&subtype=a'
        print('正在下载第' + str(i) + '页\n' + '-' * 10)
        main(url)
        print('已完成下载第' + str(i) + '页\n' + '=' * 20)
    print('全部下载完成啦!')
