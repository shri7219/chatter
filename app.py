from flask import Flask, request
import requests
from main import getmessage, get_transcript, generate_video_from_text
from mongo_service import make_connection
import CONSTANTS

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, I am healthy!"


@app.route('/createAudioTranscript', methods=['POST'])
def transcript():
    print('reached here')
    planId = request.args.get('planId')
    return get_transcript(planId)

@app.route('/upload', methods=['POST'])
def upload():
    print('reached here')
    file = request.files['file']  # Access the uploaded file
    message = request.args.get('message')
    return getmessage(file, message)

@app.route('/video', methods=['POST'])
def video():
    text = request.get_json()['text']
    print(text)
    return generate_video_from_text(text)

@app.route('/result', methods = ['POST'])
def result():
    req = request.get_json()
    db = make_connection(CONSTANTS.QUESTION_MASTER_COLLECTION_NAME)
    questionMaster = db.find_one({'planId': req['planId']})
    headers = {
        'Content-Type': 'application/json'
    }
    if questionMaster:
        questions = questionMaster['questions']
    for question in questions:
        url = 'http://localhost:3000/api/chat'
        response = requests.post(url, json=question, headers=headers)

        if response.status_code == 200:
            response = response.json()
            answerDB = make_connection(CONSTANTS.ANSWER_MASTER_COLLECTION_NAME)
            answerDB.insert_one({'questionId': question['questionId'], 'question': question['question'], 'planId':req['planId'], 'answer':response.get('text')})
        else:
            print('Error:', response.text)
            
    return "true"

