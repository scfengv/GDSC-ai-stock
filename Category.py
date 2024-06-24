# -*- coding: utf-8 -*-
"""summary label

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14gsY6zxTSNc7M44MKnZBM2FTdVHTJ7_m
"""

import pandas as pd
import google.generativeai as genai

genai.configure(api_key = "AIzaSyA4EPjx6T6nlcunEWF2IMWFb6zgh3Lv2NM")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def generate_text(prompt):
    response = model.generate_content(prompt)
    return response.text

df = pd.read_csv("21-23earningscall_dataset.csv")

# 問句放在x後面
df["Generated_Text"] = df["Summary"].apply(lambda x: generate_text([x, "Please tell me which category the above content is most related to: Automotive, Energy Generation and Storage, Full Self-Driving"]))

output_csv_file_path = "21-23earningscall_final.csv"
df.to_csv(output_csv_file_path, index=False)





