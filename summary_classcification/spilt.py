import PyPDF2
import json
import os
import re

#去頭
def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            # Extract text from page and remove footer
            page_text = page.extract_text()
            page_text = re.sub(r'WWW\.SPCAPITALIQ\.COM.*?All Rights reserved\.', '', page_text, flags=re.DOTALL)
            text += page_text
    # Remove text before first "Presentation"
    text = text.split('Operator', 1)[-1]
    return text

#切割
def split_text_by_operator(text):
    paragraphs = text.split('Martin Viecha - Tesla, Inc. - Senior Director for IR')
    # Remove leading and trailing whitespace from each paragraph
    paragraphs = [p.strip() for p in paragraphs]
    # Remove empty paragraphs
    paragraphs = [p for p in paragraphs if p]
    # Add numbering to paragraphs
    numbered_paragraphs = [{"paragraph" + str(i+1): p} for i, p in enumerate(paragraphs)]
    return numbered_paragraphs

def main():
    pdf_path = "/Users/xuzhiwei/GDSC-ai-stock/summary_classcification/2020/Q4 2020 Tesla Inc Earnings Call Transcript.pdf"
    filename = os.path.basename(pdf_path)
    text = pdf_to_text(pdf_path)
    paragraphs = split_text_by_operator(text)
    # Add a dictionary containing the filename at the beginning of the list
    paragraphs.insert(0, {"filename": filename})
    with open("2020Q4_split.json", "w") as f:
        json.dump(paragraphs, f, indent=4)

if __name__ == "__main__":
    main()