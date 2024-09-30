import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

genai.configure(api_key="AIzaSyAgwpUfHVZEaByzp4iWLCqmet9Hx29vx8k")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)