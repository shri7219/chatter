import openai
from PyPDF2 import PdfReader
from flask import Flask, request
from main import getmessage

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