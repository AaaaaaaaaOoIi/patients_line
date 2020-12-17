from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options, executable_path='/app/.chromedriver/bin/chromedriver')

# ブラウザでアクセスする
driver.get("https://www.pref.kanagawa.jp/osirase/1369/")

time.sleep(5)

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")
print(soup)

patients = soup.find('span', class_='DataView-DataInfo-summary').contents[0]
patients = patients.strip()
print(patients)
pre_day = soup.find('small', class_='DataView-DataInfo-date').contents[0]
print(pre_day)



# LINE Notifyのアクセス（自分が発行したトークンへ変更）
line_notify_token = 'hcH904pGAtXqsiAnlS2HtOzvtqb1BYE0xvZ1UeWnFFB'
# LINE NotifyのAPIアドレス（このままでOK）
line_notify_api = 'https://notify-api.line.me/api/notify'

# 　送りたいメッセージ内容
message = """
昨日の神奈川県の新型コロナウィルス感染者数です。
新規：{new_patients}人
{pre}

https://www.pref.kanagawa.jp/osirase/1369/""".format(new_patients=str(patients), pre=str(pre_day))


payload = {'message': message}
headers = {'Authorization': 'Bearer ' + line_notify_token}
line_notify = requests.post(line_notify_api, data=payload, headers=headers)
