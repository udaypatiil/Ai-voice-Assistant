import sounddevice as sd
import soundfile as sf
import tempfile
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Audio configuration
SAMPLE_RATE = 16000
MAX_DURATION = 30
SAMPLES = SAMPLE_RATE * MAX_DURATION

# Initialize OpenAI client
client = openai.OpenAI()

def record_audio():
    input("Press Enter to start recording...")
    input("Recording... Press Enter to stop")

    audio_data = sd.rec(SAMPLES, SAMPLE_RATE, channels=1, dtype='float64')
    input()
    sd.stop()
    print("Recording stopped")

    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(tmp.name, audio_data, SAMPLE_RATE)

    print(f"Recording {tmp.name} saved successfully")
    return tmp.name

def transcribe(audio_path):
    with open(audio_path, 'rb') as file:
        output = client.audio.transcriptions.create(
            model='whisper-1',
            file=file,
            response_format='text'
        )
    return output

def think(text):
    response = client.responses.create(
        model='gpt-5-nano',
        instructions='you are a helpful voice assistant keep responses short and conversational',
        input=text
    )
    return response.output_text

def spack(text):
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        input=text,
        voice='nova'
    ) as response:
        response.stream_to_file('response.mp3')

    data, sr = sf.read('response.mp3')
    sd.play(data, sr)
    sd.wait()
    os.remove('response.mp3')

    # Run AI voice assistant
    audio = record_audio()
    output = transcribe(audio)
    response = think(output)
    spack(response)
