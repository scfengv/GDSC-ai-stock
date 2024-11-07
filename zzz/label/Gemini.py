#pip install google-generativeai


import google.generativeai as genai

genai.configure(api_key = "AIzaSyCo9ob8lzjhJLZNEF05_tYYRF_pgW2Tlec")

# Set up the model
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

model = genai.GenerativeModel(model_name = "gemini-1.0-pro",
                              generation_config = generation_config,
                              safety_settings = safety_settings)

prompt_parts = [
  "In the last 24 hours at Gigafactory managed to achieve a sustained rate of over 3,000 packs per day. If extrapolated outward would be a rate of around 5,000 cars per week. \"The vast majority of the Tesla production system is automated,\" Musk says. \"We did go too far in the automation front and automated some pretty silly things\" \"We are seeing ways to achieve improved volume with dramatically less CapEx,\" he says."
  "what is last paragraph talking about? automobile, fsd, financial, energy"
]

response = model.generate_content(prompt_parts)
print(response.text)