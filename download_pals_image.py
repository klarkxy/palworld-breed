WEB_URL = "https://palworld.caimogu.cc/pal.html"

def get_images():
    # 访问对应网页
    from selenium import webdriver
    driver = webdriver.Edge()
    driver.get(WEB_URL)
    # 等待页面加载完
    import time
    time.sleep(60)
    # 获取网页内容
    html = driver.page_source
    print(html)
    # 分析网页
    from bs4 import BeautifulSoup
    # document.querySelector("body > div.container > div.pal-list-container > div.list.frame-block > table > tbody > tr:nth-child(1)")
    soup = BeautifulSoup(html, 'html.parser')
    # 获取所有的tr
    trs = soup.select('body > div.container > div.pal-list-container > div.list.frame-block > table > tbody > tr')
    for tr in trs:
        # 第一列是编号
        no = tr.select('td:nth-child(1)')[0].text
        # 第二列是头像
        img = tr.select('td:nth-child(2) > img')[0]
        # 第三列是名字
        name = tr.select('td:nth-child(3)')[0].text
        # 下载头像
        import os
        if not os.path.exists('images'):
            os.mkdir('images')
        import urllib.request
        urllib.request.urlretrieve(img['src'], f'images/{no}.{name}.png')

if __name__ == '__main__':
    get_images()