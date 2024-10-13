from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
import speech_recognition as sr
import sys
from gtts import gTTS
import pyttsx3

app = Flask(__name__)

# Function to count words in the transcribed text
def count_words(text):
    api_key = "YOUR_API_KEY_HERE"  # Insert your API key here
    input_text = text
    output = check_for_scam("API_KEY_HERE", input_text)
    return output

def check_for_scam(api_key, input_text):
    # Configure the API with the provided key
    genai.configure(api_key=api_key)

    # Define the model's generation configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the model with the specified parameters
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Act as a cybersecurity officer. Your task is to analyze the provided text and determine if it contains a scam. Reply with either 'Scam' or 'Not Scam.this is for an application to detect spam messages so ou only get text to analize as input, also tell some context about the scam do not use text decoration'",
    )

    # Start a chat session with predefined history for context
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Hi Sarah,I hope you're doing well! I wanted to remind you about our meeting scheduled for this Thursday at 2 PM in the conference room. We'll be discussing the upcoming project deadlines and strategies for the next quarter. If you have any questions or need to reschedule, please let me know. Looking forward to seeing you!Best,John",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Not Scam \n",
                ],
            },
                        {
                "role": "user",
                "parts": [
                    "kya aap mujhe ₹100 bhej sakte hain",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Scam \n",
                ],
            },
        ]
    )

    # Send the input text and get the response
    response = chat_session.send_message(input_text)

    # Return the model's response text
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/word-count', methods=['POST'])
def word_count():
    data = request.get_json()
    transcript = data.get('transcript', "")
    word_count = count_words(transcript)
    return jsonify({'word_count': word_count})

if __name__ == '__main__':
    app.run(debug=True)
