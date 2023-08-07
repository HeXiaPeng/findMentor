#-*- coding = utf-8 -*-
import re                               # 正则表达式，进行文字匹配
import urllib.request, urllib.error     # 制定 url ，获取网页数据
from bs4 import BeautifulSoup           # 网页解析，获取数据
import xlwt                             # excel 操作

# 导师数量
lenMentor = 0
baseUrl = 'https://seee.sues.edu.cn'
savepath = '导师名单.xls'
# 获取导师页码
findAllPage = re.compile(r'<em class="all_pages">(.*?)</em>')
# 获取导师的链接
findMentorLink = re.compile(r'<a href="(.*?)"')

def getAllPage(url):
    html = askURL(url)
    allPage = re.findall(findAllPage, html)[0]
    return int(allPage)

# 获取导师链接
def getUrl():
    list = []
    global lenMentor, baseUrl
    allPage = getAllPage(baseUrl + r'/dsjj1/list1.psp')

    for i in range(0, allPage):
        html = askURL(baseUrl + r'/dsjj1/list' + str(i + 1) + r'.psp')
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('span', class_ = 'Article_Title'):
            lenMentor += 1
            item = str(item)
            mentorLink = re.findall(findMentorLink, item)[0]
            list.append(mentorLink)
    return list

def askURL(url):
    head = {    # 模拟浏览器头部信息，向豆瓣服务器发送消息
       'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    request = urllib.request.Request(url, headers = head)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html

def getData(urlList):
    dataList = []
    global baseUrl

    for item in urlList:
        url = baseUrl + item
        html = askURL(url)
        soup = BeautifulSoup(html, 'html.parser')
        data = [None for _ in range(7)]
        data[0] = url

        for item in soup.find_all('td'):
            tmp = str(item)
            key = item.text.replace(' ', '').replace(' ', '')

            if key == '姓名':
                mentor_name = item.find_next_sibling('td').text
                data[1] = mentor_name
            if key == '性别':
                mentor_sex = item.find_next_sibling('td').text
                data[2] = mentor_sex
            if key == '职称':
                mentor_position = item.find_next_sibling('td').text
                data[3] = mentor_position
            if key == '研究方向':
                mentor_way = item.find_next_sibling('td').text
                data[4] = mentor_way
            if key == '联系电话':
                mentor_number= item.find_next_sibling('td').text
                data[5] = mentor_number
            if key == '电子邮箱':
                mentor_email = item.find_next_sibling('td').text
                data[6] = mentor_email
        dataList.append(data)
        print(data)
    return dataList

def saveData(dataList):
    global savepath
    print('saving...')
    book = xlwt.Workbook(encoding='utf-8', style_compression=0 ) # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)  # 创建工作区
    col = ('链接', '导师姓名', '性别', '职称', '研究方向', '电话', '邮箱')
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(0, len(dataList)):
        data = dataList[i]
        print(data)
        for j in range(0, 7):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)
def main():

    # 1.爬取网页
    # 1.1 获取导师链接
    urlList = getUrl()
    # 1.2 获取导师信息
    dataList = getData(urlList)
    # print('dataList ==>', dataList)
    # 2. 保存数据
    saveData(dataList)

if __name__ == "__main__":
    main()
    print('爬取导师数量：', lenMentor)
    print('爬取完毕')
