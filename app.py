# Import necessary libraries

from flask import Flask, request, render_template, send_file
import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import configparser
import threading
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv('.env')


# Load the configuration for Azure
config = configparser.ConfigParser()
config.read("config.ini")
azure_speech_key = config.get("azure", "speech_key")
azure_service_region = config.get("azure", "service_region")
azure_textanalytics_key = config.get("azure", "textanalytics_key")
azure_textanalytics_endpoint = config.get("azure", "textanalytics_endpoint")

# Set up the Text Analytics client
text_analytics_client = TextAnalyticsClient(endpoint=azure_textanalytics_endpoint, credential=AzureKeyCredential(azure_textanalytics_key))

app = Flask(__name__)

REPOSITORY_PATH = 'repository'

# Function to get the latest audio file from the repository folder
def get_latest_audio_file():
    repository_path = REPOSITORY_PATH
    audio_files = [os.path.join(repository_path, filename) for filename in os.listdir(repository_path) if filename.endswith('.wav')]
    if audio_files:
        return max(audio_files, key=os.path.getctime)
    return None

    
    
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/record', methods=['POST'])
def record_audio():
    
    # Retrieve the audio file from the request
    audio_data = request.files['audio']
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"audio_{current_time}.wav"
    file_path = os.path.join(REPOSITORY_PATH, file_name)

    # Save the raw audio data
    with open(file_path, 'wb') as f:
        f.write(audio_data.read())

    # Convert the audio to the correct WAV format
    raw_audio = AudioSegment.from_file(file_path)
    wav_audio = raw_audio.set_channels(1)
    wav_audio = wav_audio.set_frame_rate(16000)
    wav_audio = wav_audio.set_sample_width(2)  # 2 bytes for 16-bit samples
    wav_audio.export(file_path, format="wav")

    return f'Audio recorded and saved successfully.'


@app.route('/list_files')
def list_files():
    file_list = []
    repository_path = REPOSITORY_PATH

    # List all files in the 'repository' folder
    for filename in os.listdir(repository_path):
        if os.path.isfile(os.path.join(repository_path, filename)):
            file_list.append(filename)

    return render_template('file_list.html', files=file_list)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(REPOSITORY_PATH, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

# Add this route to your backend code
@app.route('/transcription')
def get_transcription():
    # Perform speech-to-text recognition on the latest audio file
    latest_audio_file = get_latest_audio_file()  # Implement a function to get the latest audio file
    if latest_audio_file:
        speech_config = speechsdk.SpeechConfig(subscription=azure_speech_key, region=azure_service_region)    
        audio_config = speechsdk.AudioConfig(filename=latest_audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        all_text = []

        # This is called for each fragment of recognized speech
        def recognized(evt):
            all_text.append(evt.result.text)

        # Handle potential recognition issues
        def session_stopped(evt):
            # Once the session has ended, print all the recognized text
            print("Full Transcribed Text: {}".format(" ".join(all_text)))
            # Signal the main thread to continue
            done.set()

        speech_recognizer.recognized.connect(recognized)
        speech_recognizer.session_stopped.connect(session_stopped)

        done = threading.Event()

        # Start continuous recognition
        speech_recognizer.start_continuous_recognition()
        # Wait for the recognition session to end
        done.wait()

        transcribed_text = " ".join(all_text)

        combined_results = []
        if transcribed_text:
            entities_result = text_analytics_client.recognize_entities([transcribed_text])
            seen_entities = set()  # To track seen entities

            cursor = 0
            for entity in entities_result[0].entities:
                # Create a unique identifier for each entity (text + offset)
                entity_id = f"{entity.text.lower()}_{entity.offset}"
                if entity_id not in seen_entities:
                    seen_entities.add(entity_id)  # Mark this entity as seen
                    before_entity = transcribed_text[cursor:entity.offset]
                    if before_entity:
                        combined_results.append({"text": before_entity, "type": "text"})
                    combined_results.append({"text": entity.text, "type": entity.category})
                    cursor = entity.offset + len(entity.text)

            # Add any remaining text after the last entity
            if cursor < len(transcribed_text):
                combined_results.append({"text": transcribed_text[cursor:], "type": "text"})

        return {"combined_results": combined_results}


if __name__ == '__main__':
    os.makedirs('repository', exist_ok=True)
    app.run(debug=True)

