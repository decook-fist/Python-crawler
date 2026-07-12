# 輔仁大學理工轉學考作品：跨平台科技趨勢與資安保護網路爬蟲

## 📝 作品簡介
本專案為一套自動化網路爬蟲系統，旨在針對主流網路社群與新聞媒體進行焦點監測。系統會自動針對「詐騙、個資、釣魚」等資安關鍵字進行跨平台搜集，並自動去重、清理資料，最終匯出為 Excel 報表以利數據分析。

本系統共包含三個核心爬蟲模組：
1. **PTT 社群爬蟲**：抓取 PTT 看板文章之標題、人氣與發文日期。
2. **Yahoo 新聞爬蟲**：監測科技時事與資安新聞趨勢。
3. **自由時報爬蟲**：追蹤即時時事與重大資安事件報導。

---

## 📊 執行成果展示

### 1. PTT 爬蟲執行結果
> 💡 教授您好，這是 PTT 資安保護程式實際執行的畫面：
![PTT成果截圖](demo_ptt.png.png)

### 2. Yahoo 新聞爬蟲執行結果
> 💡 教授您好，這是 Yahoo 新聞爬蟲實際執行的畫面：
![Yahoo成果截圖](demo_yahoo.png.png)

### 3. 自由時報爬蟲執行結果
> 💡 教授您好，這是自由時報爬蟲實際執行的畫面：
![自由時報成果截圖](demo_liberty.png.png)

---

## 💻 核心原始碼 (Source Code)
> 💡 教授您好，以下為本專案之核心爬蟲模組原始碼。為了方便您審閱，已設計為可折疊式選單，您可以直接點擊展開查看完整程式碼：

<details>
<summary>📦 點擊展開：PTT 社群爬蟲程式碼 (scraper_ptt.py)</summary>
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



<details>
<summary>📦 點擊展開：Yahoo 新聞爬蟲程式碼 (scraper_yahoo.py)</summary>
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

keywords = ["AI 發展", "生成式 AI", "人工智慧", "LLM大型語言模型", "晶片產業"]
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

  articles = soup.find_all("h3", class_="Stream__title")

  # 如果Yahoo抓不到，就退回抓所有h3文字，但規定標題必須包含關鍵字
  if not articles:
      all_h3 = soup.find_all("h3")
      articles = [a for a in all_h3 if k.split()[0] in a.text]

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
    # 合併後去重，保留最新的一筆
    df_final = pd.concat([old_df, new_df]).drop_duplicates(subset=['標題'], keep='last')
    print(f"合併成功！目前共有 {len(df_final)} 筆資料")
else:
    df_final = new_df
    print(f"建立新檔案，共 {len(df_final)} 筆資料")

# excel存檔
df_final.to_excel(file_name, index=False)
print(f"檔案已儲存為 {file_name}")



<details>
<summary>📦 點擊展開：自由時報爬蟲程式碼 (scraper_liberty.py)</summary>
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
