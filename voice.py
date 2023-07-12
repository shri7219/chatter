import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/fshHXoV5bk6k3sEIAdnD/stream"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "d5e5db617c6fc73e79e9cb2b796cc435"
}

data = {
    "text": "",
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
