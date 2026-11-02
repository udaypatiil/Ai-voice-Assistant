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