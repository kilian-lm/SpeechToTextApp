import requests

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
api_key = 'AIzaSyCR_CtEnbULJygX5wQhlXlC67hvH7F503k'

# Specify the coordinates of the location you want to check (Dublin, Ireland coordinates)
latitude = 53.349805
longitude = -6.26031

# Create a function to get the road speed limit
def get_road_speed_limit(latitude, longitude, api_key):
    # Create the Google Maps Geocoding API URL
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    # Send a request to the Geocoding API to get the address
    response = requests.get(geocoding_url)
    geocoding_data = response.json()

    # Check if the request was successful
    if response.status_code == 200 and geocoding_data['status'] == 'OK':
        # Extract the address
        address = geocoding_data['results'][0]['formatted_address']
        print('Address:', address)

        # Now, you can make a request to get the speed limit using the address
        # You may need to use a different API or service to obtain the speed limit data
        # Google Maps API may not provide speed limit data directly for all regions

        # Example: You can use the OpenStreetMap (OSM) API to get speed limit data
        osm_url = f'https://api.openstreetmap.org/api/0.6/way?format=json&lat={latitude}&lon={longitude}'
        osm_response = requests.get(osm_url)
        osm_data = osm_response.json()
        
        # Extract the speed limit (if available) from OSM data
        if 'tag' in osm_data and 'maxspeed' in osm_data['tag']:
            speed_limit = osm_data['tag']['maxspeed']
            print('Speed Limit:', speed_limit)
        else:
            print('Speed limit data not available for this location.')

    else:
        print('Geocoding API request failed.')

# Call the function with the specified coordinates
get_road_speed_limit(latitude, longitude, api_key)


# import openai
# openai.api_key = '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' # Hang KPMG account Fourth API
# GPT_3_5 = "gpt-3.5-turbo"
# # GPT_4 = "gpt-4-0613"
 
 
# def get_completion_GPT3_5(prompt, model=GPT_3_5):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(model=model,messages=messages,temperature=0,)
#     return response.choices[0].message["content"]

# prompt = "Write a new shakespear poem"

# content = get_completion_GPT3_5(prompt)
# print(content)


# #Note: The openai-python library support for Azure OpenAI is in preview.
# import os
# import openai
# def get_completion_azure_OpenAI_GPT_35_Turbo_16k(prompt):
#     openai.api_type = "azure"
#     openai.api_base = "https://excelpoc.openai.azure.com/"
#     openai.api_version = "2023-07-01-preview"
#     openai.api_key = "1a5fef0752624a7a97bfdc68cc363caf"
#     response = openai.ChatCompletion.create(
#       engine="gpt-35-turbo-16k",
#       messages = [{"role": "user", "content": prompt}],
#       temperature=0.7,
#       max_tokens=15288,
#       top_p=0.95,
#       frequency_penalty=0,
#       presence_penalty=0,
#       stop=None)
#     return response.choices[0].message.content


# prompt = "Write a new shakespear poem"

# content = get_completion_azure_OpenAI_GPT_35_Turbo_16k(prompt)

# print(content)


# from flask import Flask, request, render_template, send_file
# import os
# import azure.cognitiveservices.speech as speechsdk
# from datetime import datetime
# from azure.ai.textanalytics import TextAnalyticsClient
# from azure.core.credentials import AzureKeyCredential
# import configparser
# import threading
# from pydub import AudioSegment

# # Load the configuration for Azure
# config = configparser.ConfigParser()
# config.read("config.ini")
# azure_speech_key = config.get("azure", "speech_key")
# azure_service_region = config.get("azure", "service_region")
# azure_textanalytics_key = config.get("azure", "textanalytics_key")
# azure_textanalytics_endpoint = config.get("azure", "textanalytics_endpoint")

# # Set up the Text Analytics client
# text_analytics_client = TextAnalyticsClient(endpoint=azure_textanalytics_endpoint, credential=AzureKeyCredential(azure_textanalytics_key))
# transcribed_text = "I am testing my recording with transcriptions and entities and. This is 11:00. Near Phoenix Park in Dublin and I will be coding now."
# #I am testing (Skill) my recording (Skill) with transcriptions and entities and. This is 11:00 (DateTime). Near Phoenix Park (Location) in Dublin (Location)Dublin (Location)Dublin (Location) and I will be coding (Skill) now (DateTime).
# entities_result = text_analytics_client.recognize_entities([transcribed_text])

# print(entities_result)