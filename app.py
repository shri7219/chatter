import openai
from flask import request, Flask

from main import get_transcript, getmessage

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    print('reached here')
    file = request.files['file']  # Access the uploaded file
    message = request.args.get('message')
    return getmessage(file, message)

@app.route('/createAudioTranscript', methods=['POST'])
def transcript():
    print('reached here')
    planId = request.args.get('planId')
    return get_transcript(planId)


app.run()
