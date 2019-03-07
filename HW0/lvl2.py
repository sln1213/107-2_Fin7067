
'''
以下程式取自 https://github.com/MiccWan/Political-News-Analysis/blob/master/crawler/liberty_times_crawler.ipynb
'''

from datetime import datetime, timedelta

'''
將預計搜集新聞之時間範圍，以天為單位，放在 dates 的list中
'''
start_date = "2018-07-01"
stop_date = "2018-12-31"

start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")

dates = list()
while start <= stop:
    dates.append(start.strftime('%Y%m%d'))
    start = start + timedelta(days=1)


import requests
from bs4 import BeautifulSoup as bs

'''
取得網頁資料·並進行處理，再放入 data 的list中
'''
def process_document(document, date):

	nodes = document.select('ul.list > li')
	data = list()

	for li in nodes:

		# 檢查是否為空元素
		if li.select_one('a') == None:
			continue

		# 取得新聞連結
		li_link = 'http://news.ltn.com.tw/' + li.select_one('a')['href']

		# 把網頁抓下來，並以'lxml'為解析器進行解析
		li_res = requests.get(li_link)
	    li_doc = bs(li_res.text, 'lxml')

	    # 取得日期
	    li_date = datetime.strptime(date, "%Y%m%d").strftime('%Y-%m-%d')

	    #取得新聞標題
	    li_title = li.select_one('p').get_text()

	    #取得所需的新聞內文
	    li_content = ""
	    for ele in li_doc.select('div.text > p'):
	        if not 'appE1121' in ele.get('class', []):
	            li_content += ele.get_text()

	    # 將新得的資料放入data list
	    data.append({
	        'date' : li_date,
	        'title': li_title,
	        'link' : li_link,
	        'content' : li_content,
	        'tags' : []
	    })
	return data

'''
開始爬蟲，並將資料放入 all_data 的list中
'''	
cnt = 0
all_data = list()
for date in dates:
    print('start crawling :', date)
    res = requests.get('https://news.ltn.com.tw/list/newspaper/politics/' + date)
    doc = bs(res.text, 'lxml')
    data = process_document(doc, date)
    all_data += data

import pickle

'''
將 all_data 存成PKL檔
'''
with open('data/liberty_times.pkl', 'wb') as f:
    pickle.dump(all_data, f)


import pandas as pd

'''
將 all_data 轉成 Pandas 中 DataFrame 的資料結構
'''
pd.DataFrame(all_data)[['date', 'title', 'link', 'content', 'tags']].head()
