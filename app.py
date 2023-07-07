import openai
from PyPDF2 import PdfReader
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, I am healthy!"


@app.route('/upload', methods=['POST'])
def upload():
    print('reached here')
    file = request.files['file']  # Access the uploaded file
    message = request.args.get('message')
    return getmessage(file, message)

# Set up your OpenAI API credentials
openai.api_key = "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"

# Function to extract text from a PDF file using a streaming approach
def extract_text_from_pdf(file):

    reader = PdfReader(file)

    num_pages = len(reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text += page.extract_text()
        
    return text

# Function to generate a chatbot response
def generate_chatbot_response(message, chat_log=[]):
    # Set the model and parameters
    model = "gpt-3.5-turbo"
    parameters = {
        "messages": [{"role": "system", "content": "You are a helpful assistant."}]
                   + [{"role": "user", "content": msg} for msg in chat_log + [message]],
        "max_tokens": 100,
    }

    # Generate the chatbot response
    response = openai.ChatCompletion.create(
        model=model,
        **parameters
    )

    return response.choices[0].message.content.strip()

# Example usage
# user_message = "what is plan name?"
# pdf_file_path = "docs/demo3.pdf"  # Replace with the path to your PDF file

# Process the PDF document in smaller chunks
chunk_size = 5  # Number of pages to process at a time

def getmessage(file, user_message):
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    print("pages:",num_pages)
    text = ''

    for start_page in range(0, 10, chunk_size):
        end_page = min(start_page + chunk_size, num_pages)
        page_range = range(start_page, end_page)

        # Extract text from the current chunk of pages
        chunk_text = ""
        for page_num in page_range:
            page = reader.pages[page_num]
            chunk_text += page.extract_text()

        # Process the chunk text in the chatbot
        chat_log = [chunk_text]  # Add the previously processed text as conversation history
        chatbot_response = generate_chatbot_response(user_message, chat_log)

        # Append the chatbot response to the overall text
        text += chatbot_response

    return text
