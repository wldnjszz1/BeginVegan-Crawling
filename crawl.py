import ssl
import urllib.request
import json
import cx_Oracle
import time

conn = cx_Oracle.connect('/@localhost:1521/xe',encoding="UTF-8", nencoding="UTF-8")
cursor = conn.cursor()

query = urllib.parse.quote_plus("채식")  # 비건 or 채식
display = 30
start = 1  # 1~30, 31~60, 61~90 ...
sort = urllib.parse.quote("comment")  # comment(리뷰 순) or random(유사도 순)
nextval = 1

for i in range(1,8):

    print("start : "+str(start))

    client_key = ''
    client_secret = ''

    naver_url = 'https://openapi.naver.com/v1/search/local.json?query=' + str(query) + '&display=' + str(
        display) + '&start=' + str(start) + '&sort=' + str(sort)

    request = urllib.request.Request(naver_url)
    request.add_header("X-Naver-Client-Id", client_key)
    request.add_header("X-Naver-Client-Secret", client_secret)

    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen(request)

    rescode = response.getcode()
    print(rescode)

    if rescode == 200:
        response_body = response.read()
        data = json.loads(response_body)
        for i in range(1, 30):
            print('item length :  '+str(len(data['items'])))
            print(i)
            print(data['items'][i]['title'])
            print(data['items'][i]['link'])
            print(data['items'][i]['category'])
            print(data['items'][i]['telephone'])
            print(data['items'][i]['address'])
            print(data['items'][i]['roadAddress'])
            print(data['items'][i]['mapx'])
            print(data['items'][i]['mapy'])
            print('=============================================')
            sql_insert = 'insert into VEGANINFOS VALUES(:id, :title, :link, :category, :telephone, :address, :roadAddress, :mapx, :mapy)'
            cursor.execute(sql_insert, id=nextval, title=data['items'][i]['title'], link=data['items'][i]['link'], category=data['items'][i]['category'], telephone=data['items'][i]['telephone'], address=data['items'][i]['address'], roadAddress=data['items'][i]['roadAddress'], mapx=data['items'][i]['mapx'], mapy=data['items'][i]['mapy'])
            nextval = nextval + 1
        start = start + display
        conn.commit()
    else:
        print("Error Code:" + rescode)


