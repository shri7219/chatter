import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/OkAVXWGnT75RtBZ4GbXS/stream"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "d060d080ed281f180151801279ba2552"
}

data = {
    "text": "Once upon a time, in a bustling city, there lived a young woman named Ari. She was 25 years old, full of life, and had big dreams for her future. But one day, her world came crashing down when she was struck by excruciating pain throughout her body. Worried and desperate for relief, Ari rushed to the hospital.",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    },
    "skip_on_failure": True

}

response = requests.post(url, json=data, headers=headers, stream=True)

with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
