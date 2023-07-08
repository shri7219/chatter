import time

import openai
from PyPDF2 import PdfReader

# Set up your OpenAI API credentials
openai.api_key = "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"
chunk_size = 8  # Number of pages to process at a time

CONDENSE_PROMPT = 'Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.Chat History:{chat_history}Follow Up Input: {question}Standalone question:`;const QA_PROMPT = `You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.If you dont know the answer, just say you dont know. DO NOT try to make up an answer.If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.{context}Question: {question} Helpful answer in markdown:'

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
        "max_tokens": 100,
        "temperature": 0.2
    }

    # Generate the chatbot response
    response = openai.ChatCompletion.create(
        model=model,
        **parameters
    )

    return response.choices[0].message.content.strip()

def get_transcript(planId):
    input = 'Create a fictional story for female name Aari age 35 who has some accident and if she have  health insurance plan with benefits given in context.  these things would have covered in it. create audio transcript that will explain plan benefit to user pointwise. use upto 10 points to promote the plan.'
    text = "In-patient Hospitalization: The plan covers the cost of room rent during hospitalization. For a sum insured of 3 lacs, the room rent is 1% of the sum insured. For a sum insured of 5 lacs and above, a single private A/C room is provided. ICU expenses are covered up to the sum insured.Treatment for Specific Ailments/Procedures: The plan covers the cost of surgeries for hernia, hysterectomy, benign prostate hypertrophy, and surgical treatment of renal system stones. The coverage amount varies based on the sum insured. Convalescence Benefit: If the insured person is hospitalized for at least 10 consecutive days for any one illness or accident, a lump sum amount will be paid as per the sum insured opted. Wellness Program: If the insured person has been suffering from conditions such as asthma, diabetes, hypertension, dyslipidemia, or obesity, they can be a part of the wellness program. The program includes health risk assessment, baseline assessment (medical tests), coaching by experts, and improvement assessment (medical tests). The program is conducted by ManipalCigna along with its network partners. Domestic Second Opinion: This benefit provides access to a second opinion from a panel of doctors for 36 listed critical illnesses. Tele Consultation: The plan offers unlimited tele-consultation in a policy year. Cumulative Bonus: A bonus of 10% per claim-free year is provided, subject to a maximum of up to 100% of the sum insured. In case of a claim, the accumulated cumulative bonus gets reduced by 10% of the sum insured."
    chat_log = [text]
    return generate_chatbot_response(input, chat_log)

