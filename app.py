import openai

# Set up your OpenAI API credentials
openai.api_key = "YOUR_API_KEY"

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

# Example usage
user_message = "Hello, how can I help you today?"
chatbot_response = generate_chatbot_response(user_message)
print("Chatbot:", chatbot_response)
