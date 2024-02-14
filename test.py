# using speech to text using azure. Works fine. However, if there is a pause in the video the transcription doesn't cover rest of the audio.
 
# here is my code 
# import azure.cognitiveservices.speech as speechsdk

# def from_file():
#     speech_config = speechsdk.SpeechConfig(subscription="c4b8b0dec14940d59d08b6d4ae812389", region="westeurope")
#     audio_config = speechsdk.AudioConfig(filename="male.wav")
#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

#     result = speech_recognizer.recognize_once_async().get()
#     print(result.text)

# from_file()


import azure.cognitiveservices.speech as speechsdk
import threading

def from_file():
    speech_config = speechsdk.SpeechConfig(subscription="c4b8b0dec14940d59d08b6d4ae812389", region="westeurope")
    audio_config = speechsdk.AudioConfig(filename="repository\harvard.wav")
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

from_file()
