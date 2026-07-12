import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

keywords = ["AI 發展", "生成式 AI", "量子運算", "人工智慧", "大型語言模型", "大數據分析","晶片產業"]
# 排除這些關鍵詞彙
exclude_list = ["颱風", "氣象", "豪雨", "地震", "北捷", "捷運", "運輸", "停班", "停課"]
file_name = f'technology.xlsx'
# 用來存放所有爬到的資料
all_data = []

# 使用迴圈去讀取 keywords 列表
for k in keywords:
 for page in range(1):
    # 用 b 參數來換頁 (page 0 b=0, page 1 b=11...)
    b_value = page * 10 + 1
    url = f'https://tw.news.yahoo.com/search?p={k}&b={b_value}'

      # 用user-Agent來判斷是否為真人，如果是機器人爬蟲會把你踢掉
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.find_all("h3")

    # 解析資料
    for a in articles:

        # Yahoo的標題在h3下的 a 連結文字
        title = a.text.strip() if a else "無標題"
        link = a.find('a')['href'] if a.find('a') else "無連結"

        if any(bad_word in title for bad_word in exclude_list):
            continue

        print(f"標題:{title}  連結:{link}")
        all_data.append({"標題": title, "連結": link})

    # 避免爬太快被鎖
    time.sleep(5)


new_df = pd.DataFrame(all_data)

# 如果檔案存在，讀取舊資料並合併
if os.path.exists(file_name):
    old_df = pd.read_excel(file_name)
    df_final = pd.concat([old_df, new_df], ignore_index=True)
    # 合併後去重，保留最新的一筆
    df_final = pd.concat([old_df, new_df]).drop_duplicates(subset=['標題'], keep='last')
    print(f"合併成功！目前共有 {len(df_final)} 筆資料")
else:
    df_final = new_df
    print(f"建立新檔案，共 {len(df_final)} 筆資料")

# excel存檔
df_final.to_excel(file_name, index=False)
print(f"檔案已儲存為 {file_name}")