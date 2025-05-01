import os
import subprocess
from pathlib import Path
import openai
import customtkinter as ctk

# Hard-coded API Key
openai_api_key = YourAPIKEY
# Set the API key for OpenAI
openai.api_key = openai_api_key

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

# Function to handle user input and display it in the chat
def send_message():
    user_input = input_box.get()
    if user_input.strip():
        chat_display.configure(state="normal")
        chat_display.insert("end", f"You: {user_input}\n")
        chat_display.configure(state="disabled")
        input_box.delete(0, "end")

        # Add user's message to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Generate mood-boosting response from GPT-3.5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        # Extract the response
        help_response = response['choices'][0]['message']['content']
        print("Generated Response:", help_response)

        # Add the assistant's response to the conversation history
        conversation_history.append({
            "role": "assistant",
            "content": help_response
        })

        # Display bot response in the chat display
        chat_display.configure(state="normal")
        chat_display.insert("end", f"Bot: {help_response}\n")
        chat_display.configure(state="disabled")

        # TTS - Generate speech from the response
        text_to_speech(help_response, "fable", speech_file_path)

# Function to convert text to speech and play the audio
def text_to_speech(text, selected_voice, output_path):
    try:
        audio_response = openai.Audio.create(
            model="text-to-speech",
            voice=selected_voice,
            input=text  # Ensure 'input' is the correct parameter
        )

        # Read the audio data directly from the response
        audio_data = audio_response['data']

        # Save the audio data to a file
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_data)

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
        else:
            print("Unsupported OS for audio playback.")
    except Exception as e:
        print(f"Error playing audio: {e}")

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Create the main window
app = ctk.CTk()

# Set window size
app.geometry("500x600")

# Title label
title_label = ctk.CTkLabel(app, text="Boost your Mood.", font=("Roboto", 20))
title_label.pack(pady=20)

# Chat display area
chat_display = ctk.CTkTextbox(app, width=400, height=300, state="disabled", border_width=2, corner_radius=8)
chat_display.pack(pady=10)

# Input box for user message
input_box = ctk.CTkEntry(app, width=380, placeholder_text="Type your message here...", font=("Roboto", 14))
input_box.pack(pady=10)

# Send button
send_button = ctk.CTkButton(app, text="Send", command=send_message, font=("Roboto", 14))
send_button.pack(pady=10)

# Run the application
app.mainloop()
