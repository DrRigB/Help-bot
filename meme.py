import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import openai
from openai import OpenAI

# API Key
load_dotenv('ApiKey.env')
openai_api_key = os.getenv("YOUR_API_KEY_HERE")

client = OpenAI(api_key=openai_api_key)

# Speech file for audio
speech_file_path = Path(__file__).parent / "mood_booster.mp3"

# Initialize conversation messages
conversation_history = [
    {
        "role": "system",
        "content": """
        You are a very kind, practically a saint. You are a therapist and boost the moods of all who come for your aid.
        Try to tell jokes to help lighten the mood. Give good advice based on the situation to really help them out.
        Remember they might be about to do something drastic, so calm them down as much as you can. If they seem like they are going to harm themselves or others,
        give them the national helpline number (988) You can either call or text this number."""
    }
]

# Keep the conversation going
while True:
    # Get user input
    user_input = input("Enter text here: ")
    if user_input.lower() == "exit":
        print("Exiting the conversation.")
        break  # Exit the loop if user types 'exit'
    
    # Add user's message to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Generate mood-boosting response from GPT-3.5
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Ensure you're using a supported model
        messages=conversation_history
    )

    # Extract the response
    help_response = response.choices[0].message.content
    print("Generated Response:", help_response)

    # Add the assistant's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": help_response
    })

    # TTS - Generate speech from the response
    def text_to_speech(text, selected_voice, output_path):
        try:
            # Generate speech using the provided client
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice=selected_voice,
                input=text  # Ensure 'input' is the correct parameter
            )

            print("Audio Response:", audio_response)  # Print the audio response to inspect its structure

            # Read the audio data directly from the response
            audio_data = audio_response.content  # Use .content to get the binary data

            # Save the audio data to a file
            with open(output_path, "wb") as audio_file:
                audio_file.write(audio_data)  # Use the audio_data variable here

            print(f"Speech saved to {output_path}")

            # Play the audio file
            play_audio(output_path)
        except Exception as e:
            print(f"Error generating speech: {e}")

    # Function to play the audio file
    def play_audio(file_path):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS or Linux
                subprocess.run(['open', file_path])  # macOS
                # subprocess.run(['xdg-open', file_path])  # Linux
            else:
                print("Unsupported OS for audio playback.")
        except Exception as e:
            print(f"Error playing audio: {e}")

    # Select the voice you want to use (make sure this is defined)
    selected_voice = "fable"  # Replace with your actual voice choice

    # Generate and play the response audio
    text_to_speech(help_response, selected_voice, speech_file_path)
