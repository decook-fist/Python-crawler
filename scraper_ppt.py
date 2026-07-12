import requests    # requests 套件 安裝 pip install
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

user_keyword = ["詐騙", "個資", "釣魚", "網址", "連結", "被盜", "簡訊", "求救", "帳號", "資安", "防詐"]
file_name = f'technology.xlsx'
all_data = []

# 新增頁碼迴圈
for page in range(1, 3):
 # 使用迴圈去讀取 keywords 列表
 for k in user_keyword:
  url = f'https://www.ptt.cc/bbs/Tech_Job/search?q={k}&page={page}'

    # 用user-Agent來判斷是否為真人，如果是機器人爬蟲會把你踢掉
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'}
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text,"html.parser")  # 用html的解析器，解析 response.text產生的 html
  articles = soup.find_all("div",class_="r-ent")

   # 列表
  data_list = []
  for a in articles:
    title = a.find("div",class_= "title")  # 找title 它的元素名稱是div

    # 如果有title，讓title變成一個標題
    if title and title.a:
      title = title.a.text
    else:
      title = "沒有標題"

    popular = a.find("div",class_="nrec")
    if popular and popular.span:
         popular = popular.span.text
    else:
         popular = "NO"

    date = a.find("div",class_="date")
    if date:
        date = date.text
    else:
        date = "NO"
    print(f"標題:{title} 人氣:{popular}  日期:{date}")
    all_data.append({"標題": title, "人氣": popular, "日期": date})

  # 避免爬太快被鎖
  time.sleep(1)

new_df = pd.DataFrame(all_data)

# 如果檔案存在，讀取舊資料且合併
if os.path.exists(file_name):
    old_df = pd.read_excel(file_name)
    df_final = pd.concat([old_df, new_df], ignore_index=True)
    # 去除標題重複的資料
    df_final = df_final.drop_duplicates(subset=['標題'], keep='first')
    print(f"合併成功！目前共有 {len(df_final)} 筆資料")
 # 如果檔案不存在，使用新資料
else:
    df_final = new_df
    print(f"建立新檔案，共 {len(df_final)} 筆資料")

    # excel存檔
df_final.to_excel(file_name, index=False)
print(f"檔案已儲存為 {file_name}")

#if response.status_code == 200:   # 透過if-else判斷網址是否抓到網頁
#     with open('output.html', 'w',encoding='utf-8') as f:
#      f.write(response.text)     # 檔案寫入HTML資料
#      print("寫入正確")
#else:
#      print("沒有抓到網頁")