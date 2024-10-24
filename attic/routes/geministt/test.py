# -*- coding: utf-8 -*-
import base64

import requests
from google.cloud import speech


def transcribe_audio_from_url(url):
    # Instantiates a client
    client = speech.SpeechClient()

    # Fetch audio content from URL
    response = requests.get(url)
    audio_content = base64.b64encode(response.content).decode("utf-8")

    # Transcribe speech
    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code="en-GB",
        model="default",
        audio_channel_count=1,
        enable_word_confidence=True,
        enable_word_time_offsets=True,
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))


# Example usage
url = "https://example.com/path/to/your/audio_file.wav"
transcribe_audio_from_url(url)
