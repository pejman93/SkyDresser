import sounddevice as sd
from scipy.io.wavfile import write
import assemblyai as aai
import os
from dotenv import load_dotenv
load_dotenv()
aai.settings.api_key = os.getenv("API_SOUND_KEY")


def record(duration=10, filename="weather_output.wav"):
    fs = 44100

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print(f"✅Saved as {filename}")
    return filename


def voice_to_text(filename):


    audio_file = filename
    # audio_file = "https://assembly.ai/wildfires.mp3"

    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)

    transcript = aai.Transcriber(config=config).transcribe(audio_file)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    # print(transcript.text) - for debugging only
    return transcript.text
