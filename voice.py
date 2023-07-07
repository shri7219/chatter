import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/DmbDXRnsDgyeMuXM9ZQN/stream"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "KEY"
}

data = {
    "text": "Welcome to ManipalCigna Health Insurance! Today, we have an interesting story to share with you. Meet Aari, a 35-year-old woman who recently encountered an unfortunate accident. Let's imagine how having ManipalCigna ProHealth Prime, our comprehensive health insurance plan, could have covered her medical expenses",

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
