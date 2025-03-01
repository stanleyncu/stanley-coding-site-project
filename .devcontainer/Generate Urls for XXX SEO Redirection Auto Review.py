from google.colab import files
import pandas as pd
import os

# 清除之前上傳的檔案
for filename in os.listdir():
  if filename.endswith(('.xlsx', '.csv')):  # 刪除 .xlsx 和 .csv 檔案
    os.remove(filename)
    print(f"已刪除檔案: {filename}")

uploaded = files.upload()

# 讀取 'SEO domain' 工作表
df_seo = pd.read_excel('SEO domain.xlsx', sheet_name='SEO domain')

# 讀取 'Old domain' 工作表
df_old = pd.read_excel('SEO domain.xlsx', sheet_name='Old domain')
df_old = df_old.rename(columns={'Old Domain': 'Old domain'})

# 建立一個空的 list 來存放所有 URL
all_urls = []

# 處理 'SEO domain' 工作表
for index, row in df_seo.iterrows():
  for i in range(1, 10):  # 迴圈處理 Url Path 1 到 Url Path 9
    try:
      if i in (3, 6, 9):  # Url Path 3, 6, 9 的網址格式不同
        url = f"https://account.{row['Latest domain']}/{row[f'Url Path {i}']}"
      else:
        url = f"https://www.{row['Latest domain']}{row[f'Url Path {i}']}"
      all_urls.append(url)
      print(f"SEO domain URL: {url}")  # 加入 print(url)
    except KeyError:
      print(f"找不到欄位 'Url Path {i}'，跳過此 URL (SEO domain)")

# 處理 'Old domain' 工作表
for index, row in df_old.iterrows():
  # 先將 row['Old domain'] 轉換為字串
  if "na" in str(row['Old domain']).strip().lower():  # 如果 Old domain 的值包含 "NA" 或 "na" 就跳過
    continue

  for i in range(1, 4):  # 迴圈處理 Url Path 1 到 Url Path 9
    try:
      if i == 3:  # Url Path 3 的網址格式不同
        url = f"https://account.{row['Old domain']}/{row[f'Url Path {i}']}"
      else:
        url = f"https://www.{row['Old domain']}{row[f'Url Path {i}']}"
      all_urls.append(url)
      print(f"Old domain URL: {url}")  # 加入 print(url)
    except KeyError:
      print(f"找不到欄位 'Url Path {i}'，跳過此 URL (Old domain)")

# 建立一個 DataFrame，將所有 URL 放在同一欄位
df_urls = pd.DataFrame(all_urls, columns=['URL'])

# 將 DataFrame 儲存成 CSV 檔案
df_urls.to_csv('urls.csv', index=False)

# 提供 CSV 檔案下載
files.download('urls.csv')
