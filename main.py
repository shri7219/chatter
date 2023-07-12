import subprocess

import openai
from PyPDF2 import PdfReader
from flask import send_file

import CONSTANTS
from mongo_service import make_connection

# Set up your OpenAI API credentials
openai.api_key = "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"
chunk_size = 8  # Number of pages to process at a time

CONDENSE_PROMPT = 'Given the following conversation and a follow up question, You are a helpful AI assistant. ' \
                  'Check what I have described in context and generate scenario based on that.'


def getmessage(file, message):
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    print("pages:", num_pages)
    text = ''
    # cnt = 0
    for start_page in range(0, num_pages, chunk_size):
        end_page = min(start_page + chunk_size, num_pages)
        page_range = range(start_page, end_page)

        # Extract text from the current chunk of pages
        chunk_text = ""
        for page_num in page_range:
            page = reader.pages[page_num]
            chunk_text += page.extract_text()

        result = chunk_text.replace('\t', ' ')
        result = result.replace('\n', ' ')
        # Process the chunk text in the chatbot
        chat_log = [result]  # Add the previously processed text as conversation history
        print("text:", chat_log)
        # if cnt == 2:
        #     time.sleep(1)
        #     print("sleep ended:", cnt)
        chatbot_response = generate_chatbot_response(message, chat_log)
        # cnt = cnt + 1

        # Append the chatbot response to the overall text
        text += chatbot_response

    return text


# Function to generate a chatbot response
def generate_chatbot_response(message, chat_log=[]):
    # Set the model and parameters
    model = "gpt-3.5-turbo-16k"
    parameters = {
        "messages": [{"role": "system", "content": CONDENSE_PROMPT}]
                    + [{"role": "user", "content": msg} for msg in chat_log + [message]],
        "max_tokens": 1000,
        "temperature": 0.2
    }

    # Generate the chatbot response
    response = openai.ChatCompletion.create(
        model=model,
        **parameters
    )

    return response.choices[0].message.content.strip()


def get_transcript(planId):
    answerDB = make_connection(CONSTANTS.ANSWER_MASTER_COLLECTION_NAME)
    records = answerDB.find({"planId": planId})
    text = ''
    for record in records:
        text += record["answer"]
    text.replace('\n', ' ')
    chat_log = [text]

    input = 'There is a fictional character named “Ari” who is a 25 year old female. One day Ari feels severe pain and has to rush to the hospital. The doctors find out that she has a huge kidney stone which needs attention and she has to get admitted in the hospital for 3 days. Given the above mentioned scenario and the benefits of her health insurance plan mentioned in the context, generate a fictional story of Ari to demonstrate how her health plan helped her with various expenses. This fictional story should be helpful in convincing people to buy health insurance. '
    print("answers:", chat_log)
    response = generate_chatbot_response(input, chat_log)
    saveDb = make_connection(CONSTANTS.AUDIO_TRANSCRIPPT_COLLECTION_NAME)
    saveDb.update_one({"planId": planId}, {'$set': {"response": response, "planId": planId}})
    return response


def generate_video_from_text(text):
    # frames = []
    # text = text[:300]
    # Step 1: Generate a video script using the OpenAI API
    # images = generate_images(text, 10, "1024x1024")
    # for image in images:
    #     image_data = requests.get(image.get("url")).content
    #     image = Image.open(io.BytesIO(image_data))
    #     frames.append(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

    # Create a video writer
    # height, width, _ = frames[0].shape
    # video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    # Write the image to the video
    # for frame in frames:
    #     video_writer.write(frame)

    # # Release the video writer
    # video_writer.release()

    output_video = 'talk.mp4'
    output_file = 'output_with_audio.mp4'
    audio_file = 'output.mp3'

    command = f'ffmpeg -i {output_video} -i {audio_file} -c:v copy -c:a aac -strict experimental {output_file}'
    subprocess.call(command, shell=True)

    return send_file(output_file, mimetype="video/mp4", as_attachment=True)
