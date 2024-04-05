import json
import os

def merge_json_files(folder_path):
    merged_data = []

    # 遍歷文件夾中的所有 JSON 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                merged_data.extend(data)

    return merged_data

def save_merged_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 設置文件夾路徑和輸出文件名
folder_path = "//Users/xuzhiwei/GDSC-ai-stock/summary_classcification/2020_summary"
output_file = "merged2020_data.json"

# 合併 JSON 文件
merged_data = merge_json_files(folder_path)

# 保存合併後的 JSON 數據到一個文件中
save_merged_json(merged_data, output_file)
