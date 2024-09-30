import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Configure your API key
genai.configure(api_key="AIzaSyAgwpUfHVZEaByzp4iWLCqmet9Hx29vx8k")  # Replace with your actual API key

# Function to fetch HTML content from a URL
def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to extract relevant information from HTML
def extract_information(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "No Title"
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    return title, paragraphs

# Function to generate content using the Gemini API
def generate_content(user_input, html_content):
    # Create a prompt based on user input and extracted HTML content
    content_to_send = f"Title: {html_content[0]}\n\n"
    content_to_send += "Content:\n" + "\n".join(html_content[1])
    prompt = f"{content_to_send}\n\nUser Input: {user_input}\n\nResponse:"

    # Create a GenerativeModel instance
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Call the Gemini API
    response = model.generate_content(prompt)
    return response.text

# Example usage
url = input("Enter the URL you want to scrape: ")  # User input for URL
user_input = input("Enter your comment or question: ")  # User input for comment

html_content = fetch_html(url)

if html_content:
    extracted_info = extract_information(html_content)
    
    # Generate content based on user input and HTML content
    response_text = generate_content(user_input, extracted_info)
    
    # Print the response from the Gemini API
    print(extracted_info)
