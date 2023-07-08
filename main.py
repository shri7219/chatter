import openai
import subprocess
import requests
from flask import send_file
from PyPDF2 import PdfReader
import openai
import torchvision.transforms as T
from PIL import Image
import cv2
import io
import json
import numpy as np

# Set up your OpenAI API credentials
openai.api_key = ""
chunk_size = 5  # Number of pages to process at a time

def getmessage(file, message):
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
        chatbot_response = generate_chatbot_response(message, chat_log)

        # Append the chatbot response to the overall text
        text += chatbot_response

    return text

# Function to extract text from a PDF file using a streaming approach
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
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


def generate_chat_response(messages):
    # Calculate the number of tokens in the chat log
    total_tokens = sum([len(message['role']) + len(message['content']) for message in messages])
    
    # Determine the maximum allowed tokens for the model
    max_tokens = 4096 - total_tokens

    # Truncate or omit messages to fit within the token limit
    trimmed_messages = []
    token_count = 0

    for message in messages:
        role = message['role']
        content = message['content']

        # Calculate the number of tokens in the current message
        message_tokens = len(role) + len(content)

        if token_count + message_tokens <= max_tokens:
            trimmed_messages.append(message)
            token_count += message_tokens
        else:
            break

    # Generate the chat response
    response = openai.Completion.create(
        engine="text-davinci-003",
        messages=trimmed_messages,
        max_tokens=100,  # Adjust as needed
        temperature=0.7,
        n=1,
        stop=None
    )

    return response.choices[0].message['content']


def generate_images(prompt, n, size):
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai.api_key  # Replace YOUR_API_KEY with your actual OpenAI API key
    }
    data = {
        'prompt': prompt,
        'n': n,
        'size': size
    }

    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    if response.status_code == 200:
        images = response.json().get("data")
        return images
    else:
        print('Error:', response.text)
        return None

def generate_video_from_text(text):
    frames = []
    text = text[:300]
    # Step 1: Generate a video script using the OpenAI API
    images = generate_images(text, 10, "1024x1024")
    for image in images:
        image_data = requests.get(image.get("url")).content
        image = Image.open(io.BytesIO(image_data))
        frames.append(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

    output_video = 'output_video.mp4'

    # Create a video writer
    height, width, _ = frames[0].shape
    video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    # Write the image to the video
    for frame in frames:
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()

    return send_file(output_video, mimetype="video/mp4", as_attachment=True)


# Example usage
# user_message = "what is plan name?"
# pdf_file_path = "docs/demo3.pdf"  # Replace with the path to your PDF file

# # Process the PDF document in smaller chunks
# text = ""
# with open(pdf_file_path, 'rb') as file:
#     reader = PdfReader(file)
#     num_pages = len(reader.pages)
#     print("pages:",num_pages)

#     for start_page in range(0, 10, chunk_size):
#         end_page = min(start_page + chunk_size, num_pages)
#         page_range = range(start_page, end_page)

#         # Extract text from the current chunk of pages
#         chunk_text = ""
#         for page_num in page_range:
#             page = reader.pages[page_num]
#             chunk_text += page.extract_text()

#         # Process the chunk text in the chatbot
#         chat_log = [chunk_text]  # Add the previously processed text as conversation history
#         print("text:", chat_log)
#         chatbot_response = generate_chatbot_response(user_message, chat_log)

#         # Append the chatbot response to the overall text
#         text += chatbot_response

# print("Chatbot response:", text)
