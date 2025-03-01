import pandas as pd
import re
from google.colab import files
import os

# 清除之前上傳的檔案
for filename in os.listdir():
  if filename.endswith(('.xlsx', '.csv')):  # 刪除 .xlsx 和 .csv 檔案
    os.remove(filename)
    print(f"已刪除檔案: {filename}")

# 上傳檔案功能
def upload_files():
    print("請上傳檔案")
    uploaded = files.upload()
    return list(uploaded.keys())

# 提取根域名
def extract_root_domain(url):
    match = re.match(r'^https?://(?:www\.)?(?:[^/]+\.)?([^./]+\.[^./]+)', str(url))
    print(f"Extracting root domain from URL: {url} -> {match.group(1) if match else 'None'}")  # 調試打印
    return match.group(1) if match else None

# 提取國家代碼
def extract_country_code(address):
    match = re.search(r'-([A-Z]{2})', str(address))
    return match.group(1) if match else None

# 主程式
def main():
    uploaded_files = upload_files()

    # Latest 和 Old domain 的初始化放在最前面
    seo_domain_file = "SEO domain.xlsx"
    seo_latest_domain_sheet = pd.read_excel(seo_domain_file, sheet_name="SEO domain")
    latest_domain_dict = {row['Country code']: row['Latest domain'] for _, row in seo_latest_domain_sheet.iterrows()}
    print(f"Loaded latest_domain_dict: {latest_domain_dict}")  # 打印 Latest domain 字典

    seo_old_domain_sheet = pd.read_excel(seo_domain_file, sheet_name="Old domain")
    old_domain_dict = {}
    for _, row in seo_old_domain_sheet.iterrows():
        country = row['Country code']
        domain = row['Old domain']
        if pd.notnull(country) and pd.notnull(domain):
            if country not in old_domain_dict:
                old_domain_dict[country] = []
            old_domain_dict[country].append(domain)
    print(f"Loaded old_domain_dict: {old_domain_dict}")  # 打印 Old domain 資訊

    all_reports = []

    for file in uploaded_files:
        if file.startswith("hreflang") or file.startswith("SEO domain"):
            print(f"忽略檢查檔案: {file}")
            continue

        if file.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        else:
            print(f"不支援的檔案格式: {file}")
            continue

        # 提取 Address 和 Country Code
        sample_address = df["Address"].dropna().iloc[0] if "Address" in df.columns and not df["Address"].isnull().all() else None
        country_code = extract_country_code(sample_address) if sample_address else "Unknown"
        print(f"Address: {sample_address}, Extracted Country Code: {country_code}")

        # 執行檢查條件
        report = check_conditions(df, file, latest_domain_dict, old_domain_dict)
        all_reports.extend(report)

    # 生成檢查報告
    if all_reports:
        report_df = pd.DataFrame(all_reports)
        report_df.to_csv("check_report.csv", index=False)
        print("檢查完成，已生成報告: check_report.csv")
        files.download("check_report.csv")
    else:
        print("無有效檢查結果，未生成報告。")

# 檢查條件執行
def check_conditions(df, filename, latest_domain_dict, old_domain_dict):
    report = []

    for index, row in df.iterrows():
        entry = {
            "Filename": filename,
            "Row": index + 1,
            "Address": row.get("Address", ""),
            "Status Code": row.get("Status Code", ""),
            "Status Code Result": "PASS",
            "Redirect URL": row.get("Redirect URL", ""),
            "Redirect URL Result": "PASS",
            "Canonical Link Element 1": row.get("Canonical Link Element 1", ""),
            "Canonical Link Element 1 Result": "PASS",
            "Indexability Status": row.get("Indexability Status", ""),
            "Indexability Status Result": "PASS",
            #"Hreflang Result": "通過",
            "Abnormal": []
        }
        # 檢查 Status Code
        status_code = row.get("Status Code", "")
        address_root = extract_root_domain(row.get("Address", ""))
        country_code = extract_country_code(row.get("Address", ""))
        old_domains_for_country = old_domain_dict.get(country_code, "")
        latest_domain_for_country = latest_domain_dict.get(country_code, "")

        # 打印測試 Status Code
        print(f"Row {index + 1}: Address: {row.get('Address', '')}, Status Code: {status_code}")

        # **執行 Status Code 檢查**
        # 檢查邏輯為公司機密，隱藏避免爭議及法律問題

        # **新增：提取 Redirect URL 的根域名和國家代碼**
        redirect_url = row.get("Redirect URL", "")
        redirect_root = extract_root_domain(redirect_url) if redirect_url else None
        redirect_country_code = extract_country_code(redirect_url) if redirect_url else None

        # **打印測試 Redirect URL**
        print(f"Row {index + 1}: Redirect URL: {redirect_url}, "
              f"Extracted Root: {redirect_root}, Extracted Country Code: {redirect_country_code}")

        # **檢查 Redirect URL**
        # 檢查邏輯為公司機密，隱藏避免爭議及法律問題


        # 提取 Canonical Link Element 1 的根域名和國家代碼
        canonical_link_element = row.get("Canonical Link Element 1", "")
        canonical_root = extract_root_domain(canonical_link_element) if canonical_link_element else None
        canonical_country_code = extract_country_code(canonical_link_element) if canonical_link_element else None

        # 打印測試 Canonical Link Element 1
        print(f"Row {index + 1}: Canonical Link Element 1: {canonical_link_element}, "
              f"Extracted Root: {canonical_root}, Extracted Country Code: {canonical_country_code}")

        # 檢查 Canonical Link Element 1
        # 檢查邏輯為公司機密，隱藏避免爭議及法律問題

        # **檢查 Indexability Status**
        # 檢查邏輯為公司機密，隱藏避免爭議及法律問題

        # **打印測試 Indexability Status**
        print(f"Row {index + 1}: Indexability Status: {indexability_status}, Result: {entry['Indexability Status Result']}")


        # 其他檢查邏輯保留
        report.append(entry)

    return report



# 執行程式
if __name__ == "__main__":
    main()
