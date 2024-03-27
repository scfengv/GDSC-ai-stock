import json

input_file = "2019Q4_split.json"
output_file = "2019Q4_split_paragraphs.json"


def split_text_averagely(text, max_words):
    chunks = []
    words = text.split()  # 使用split()方法将文本按空格分割成单词列表
    while len(words) > max_words:
        chunk_size = max_words // 2
        chunk1 = ' '.join(words[:chunk_size])  # 使用join()方法将单词列表拼接成字符串
        chunk2 = ' '.join(words[chunk_size:])
        chunks.append(chunk1)
        words = words[chunk_size:]
    return chunks


with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

max_words_per_chunk = 400
output_data = []

for item in data:
    paragraph = ""
    for key, value in item.items():
        if key.startswith("paragraph"):
            paragraph = value
            if len(paragraph.split()) > max_words_per_chunk:

                chunks = split_text_averagely(paragraph, max_words_per_chunk)
                for idx, chunk in enumerate(chunks):
                    output_data.append({"paragraph": chunk})
            else:
                output_data.append({"paragraph": paragraph})

# 将处理后的数据写入输出文件
with open(output_file, "w") as file:
    json.dump(output_data, file, indent=4)

print("finish", output_file)