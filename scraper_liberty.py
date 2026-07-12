import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

keywords = ["防詐宣導", "資安防禦", "網路犯罪", "個資保護", "金融資安監控", "資安漏洞", "數位發展", "詐騙", "個資"]
file_name = f'technology.xlsx'
all_data = []


for k in keywords:
   for page in range(1,3):
    url = f'https://search.ltn.com.tw/list?keyword={k}&page={page}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'}

    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    # 自由時報的搜尋結果都在 ul.list 裡面的 li 標籤裡面
    articles = soup.select('ul.list > li')

    for a in articles:

        title_tag = a.select_one('a.tit')
        if title_tag:
         title = title_tag.text.strip()
         link = title_tag['href']
         if k not in title:
          continue
         print(f"標題: {title}, 連結: {link}")
         all_data.append({"標題": title, "連結": link})


    # 避免爬太快被鎖
    time.sleep(3)

new_df = pd.DataFrame(all_data)
if os.path.exists(file_name):
    old_df = pd.read_excel(file_name)
    df_final = pd.concat([old_df, new_df]).drop_duplicates(subset=['標題'], keep='last')
else:
    df_final = new_df

df_final.to_excel(file_name, index=False)
print(f"完成！共 {len(df_final)} 筆，檔案已儲存為 {file_name}")