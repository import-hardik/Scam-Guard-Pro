import google.generativeai as genai

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
        system_instruction="Act as a cybersecurity officer. Your task is to analyze the provided text and determine if it contains a scam. Reply with either 'Scam' or 'Not Scam.'",
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
        ]
    )

    # Send the input text and get the response
    response = chat_session.send_message(input_text)

    # Return the model's response text
    return response.text

# Example of using the function
api_key = "YOUR_API_KEY_HERE"  # Insert your API key here
input_text = "Congratulations! You've been selected for an exclusive offer to receive a $1,000 gift card."
output = check_for_scam("Api key", input_text)
print(output)
