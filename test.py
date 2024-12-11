import os
from gtts import gTTS
import pygame
import time
import sounddevice as sd
import numpy as np
import wave
from openai import OpenAI

# Initialize OpenAI API with your key
client = OpenAI(
    api_key="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"
)

messages = [{"role": "system", "content": "You are a helpful assistant."}]

app_commands = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "start chrome",
    "VS code": "code",
}

def record_audio(duration=5, fs=16000):
    print("Recording... Please speak into the microphone.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to finish
    return np.array(audio)

def save_as_wav_file(audio_data, filename="output.wav", fs=16000):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(fs)
        wav_file.writeframes(audio_data.tobytes())
    return filename

def transcribe_audio(file_path):
    with open(file_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1"
        )
    return response.text

def open_app(command):
    if command in app_commands:
        os.system(app_commands[command])
        return f"Opening {command.capitalize()}..."
    else:
        return "Sorry, I can't open that application."

while True:
    # Record user speech
    audio_data = record_audio()
    wav_filename = save_as_wav_file(audio_data)

    # Transcribe the audio
    try:
        message = transcribe_audio(wav_filename)
    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
        continue

    if message.lower() == "exit":
        print("Exiting...")
        break

    print("You: ", message)

    # Check if the user wants to open an app
    if message.lower() in app_commands:
        response = open_app(message.lower())
        print("Titan: ", response)  # Respond to app opening
    elif "can i type" in message.lower():
        # Allow typing input
        typed_query = input("You can now type your question: ")
        messages.append({"role": "user", "content": typed_query})

        # Get the response for the typed query
        response = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo").choices[0].message.content
        print("Titan: ", response)  # Respond to the typed query
    else:
        # If no app command or typing request, proceed with normal AI conversation
        messages.append({"role": "user", "content": message})
        chat = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
        response = chat.choices[0].message.content
        print("Titan: ", response)  # Respond to the spoken message

    # Convert response to speech using gTTS
    response_file = os.path.join(os.getcwd(), f"response_{int(time.time())}.mp3")
    try:
        tts = gTTS(response, lang='en')
        tts.save(response_file)
        print(f"MP3 file created successfully: {response_file}")
    except Exception as e:
        print(f"Failed to save MP3 file: {e}")
        continue

    # Play the response
    pygame.mixer.init()
    pygame.mixer.music.load(response_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    os.remove(response_file)
    os.remove(wav_filename)
