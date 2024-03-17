import azure.cognitiveservices.speech as speechsdk
import os
import threading

# Function to get the latest audio file from the repository folder
def get_latest_audio_file():
    repository_path = '/Users/d0342084/Documents/Git/SpeechToTextApp'
    audio_files = [os.path.join(repository_path, filename) for filename in os.listdir(repository_path) if filename.endswith('.wav')]
    if audio_files:
        return max(audio_files, key=os.path.getctime)
    return None

x = get_latest_audio_file()
print(x)



def get_transcription():
    # Perform speech-to-text recognition on the latest audio file
    latest_audio_file = get_latest_audio_file()  # Implement a function to get the latest audio file
    
    if latest_audio_file:
        print(latest_audio_file)
        speech_config = speechsdk.SpeechConfig(subscription="c4b8b0dec14940d59d08b6d4ae812389", region="westeurope")
        audio_config = speechsdk.AudioConfig(filename=latest_audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        all_text = []

        # This is called for each fragment of recognized speech
        def recognized(evt):
            all_text.append(evt.result.text)
            print(evt.result.text)  # Print each fragment as it's recognized

        # Handle potential recognition issues
        def session_stopped(evt):
            print("Session stopped: {}".format(evt))
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


get_transcription()