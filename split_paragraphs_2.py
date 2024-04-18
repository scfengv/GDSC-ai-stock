import json

input_file = "/Users/xuzhiwei/GDSC-ai-stock/split/2020Q4_split.json"
output_file = "/Users/xuzhiwei/GDSC-ai-stock/split_paragraphs/2020Q4_split_paragraphs.json"


def split_text_averagely(text, max_words):
    chunks = []
    words = text.split()  # 使用split()方法将文本按空格分割成单词列表
    while len(words) > max_words:
        # 找到即将超过最大字数的位置
        index = max_words
        while index < len(words) and not words[index].endswith('.'):
            index -= 1

        # 若找到了句号，按照句号位置切割
        if index < len(words):
            chunk = ' '.join(words[:index + 1])
            chunks.append(chunk)
            words = words[index + 1:]
        '''
        else:  # 若未找到句号，按照默认位置切割
            chunk_size = max_words // 2
            chunk1 = ' '.join(words[:chunk_size])
            chunk2 = ' '.join(words[chunk_size:])
            chunks.append(chunk1)
            words = words[chunk_size:]
        '''
    # 处理剩余的文字
    if words:
        chunks.append(' '.join(words))
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

