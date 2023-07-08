import openai

<<<<<<< Updated upstream
# Set up your OpenAI API credentials
openai.api_key = "YOUR_API_KEY"
=======
from main import get_transcript

app = Flask(__name__)
>>>>>>> Stashed changes

# Define a function to generate a chatbot response
def generate_chatbot_response(message):
    # Set the model and parameters
    model = "gpt-3.5-turbo"
    parameters = {
        "temperature": 0.7,
        "max_tokens": 50,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    # Generate the chatbot response
    response = openai.Completion.create(
        engine=model,
        prompt=message,
        **parameters
    )

    return response.choices[0].text.strip()

<<<<<<< Updated upstream
# Example usage
user_message = "Hello, how can I help you today?"
chatbot_response = generate_chatbot_response(user_message)
print("Chatbot:", chatbot_response)
=======
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
>>>>>>> Stashed changes
