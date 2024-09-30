from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import markdown2

app = Flask(__name__)

# Configure your API key
genai.configure(api_key="AIzaSyAgwpUfHVZEaByzp4iWLCqmet9Hx29vx8k")  # Replace with your actual API key

# Function to fetch HTML content from a URL
def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve the webpage. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Function to extract relevant information from HTML
def extract_information(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "No Title"
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    return title, paragraphs

# Function to generate content using the Gemini API
def generate_content(user_input, html_content):
    content_to_send = f"Title: {html_content[0]}\n\n"
    content_to_send += "Content:\n" + "\n".join(html_content[1])
    prompt = f"{content_to_send}\n\nUser Input: {user_input}\n\nResponse:"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Assume the response includes code blocks properly formatted
    response_text = response.text
    
    return response_text

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    if request.method == 'POST':
        url = request.form['url']
        user_input = request.form['comment']
        
        html_content = fetch_html(url)
        if isinstance(html_content, str):  # Check if it's a string (HTML or error message)
            extracted_info = extract_information(html_content)
            response_text = generate_content(user_input, extracted_info)

            # Convert the response text to markdown for rendering
            markdown_response = markdown2.markdown(response_text)
            return render_template('index.html', response=markdown_response)

    return render_template('index.html', response=response_text)

if __name__ == '__main__':
    app.run(debug=True)