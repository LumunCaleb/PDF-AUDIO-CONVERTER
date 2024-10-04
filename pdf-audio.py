import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS
import os

# Function to convert PDF to audio and save it as an MP3 file using gTTS
def convert_pdf_to_audio(pdf_file, reading_speed=1.0, pages=None):
    pdf_reader = PdfReader(pdf_file)
    text = ""

    if pages is not None:
        selected_pages = extract_pages(pdf_reader, pages)
        for page in selected_pages:
            page_text = page.extract_text() if page.extract_text() else ""
            if page_text:
                text += page_text
            else:
                st.write("No text found on the selected page.")
    else:
        for page in pdf_reader.pages:
            page_text = page.extract_text() if page.extract_text() else ""
            if page_text:
                text += page_text

    # Debugging: Display the extracted text length and preview
    st.write("Extracted Text Length:", len(text))
    # st.write("Extracted Text Preview:", text[:500])  # Display a preview of the first 500 characters

    if not text.strip():  # Check if text is empty or just whitespace
        st.write("No text found in the PDF.")
        return None
    
    # Convert text to audio using gTTS and save directly to a file
    output_audio_file = "output.mp3"  # File name for the output audio
    try:
        tts = gTTS(text, lang='en', slow=False)
        tts.save(output_audio_file)  # Save the audio to a file

        st.write("Audio conversion successful.")
        return output_audio_file  # Return the file path for further use
    except Exception as e:
        st.write("Error during audio conversion:", e)
        return None

# Function to extract specific pages based on user input
def extract_pages(pdf_reader, page_selection):
    pages = []
    num_pages = len(pdf_reader.pages)
    
    # Parse the input to handle ranges and specific pages
    selections = page_selection.split(",")
    
    for sel in selections:
        sel = sel.strip()
        if "-" in sel:
            # Handle ranges like "1-3"
            try:
                start, end = map(int, sel.split("-"))
                if 1 <= start <= num_pages and 1 <= end <= num_pages and start <= end:
                    for i in range(start - 1, end):  # Zero-based index
                        pages.append(pdf_reader.pages[i])
                else:
                    st.write(f"Invalid range: {sel}")
            except ValueError:
                st.write(f"Invalid range format: {sel}")
        else:
            # Handle specific pages
            try:
                if sel.isdigit():
                    page_num = int(sel)
                    if 1 <= page_num <= num_pages:
                        pages.append(pdf_reader.pages[page_num - 1])  # Zero-based index
                    else:
                        st.write(f"Invalid page number: {sel}")
                else:
                    st.write(f"Invalid page number format: {sel}")
            except ValueError:
                st.write(f"Unable to parse page number: {sel}")

    return pages

# Streamlit App Interface
st.title("PDF to Audio Converter")
st.markdown("A Project by **YUSUF ABDUL** - NACEST/COM/HND22/780 (Departmet of Computer Science)")
# st.markdown("<u>text</u>", unsafe_allow_html=True)  Use this to underline text
st.markdown("*Supervisor:* Mr. Ike Innocent")

# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    st.write("File uploaded successfully.")
    
    # Voice selection
    voice_type = st.selectbox("Select Voice", ["Male", "Female"])
    
    # Reading speed
    reading_speed = st.slider("Select Reading Speed", 0.5, 2.0, 1.0, 0.1)
    
    # Page selection dropdown
    page_selection_option = st.selectbox("Select Pages", ["Entire Document", "Specific Pages"])
    
    # Handle specific page input based on the dropdown selection
    page_selection = None
    if page_selection_option == "Specific Pages":
        num_pages = len(PdfReader(uploaded_file).pages)
        st.write(f"This PDF has {num_pages} pages.")
        page_selection = st.text_input("Enter Pages (e.g., 1-3, 5, 7-9)", "")
    
    # Convert PDF to audio
    if st.button("Convert to Audio"):
        st.write("Converting...")
        if page_selection_option == "Entire Document":
            page_selection = None  # Process the entire document if this option is chosen
        audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, page_selection)
        
        if audio_path:
            st.write("Conversion complete.")
            
            # Allow the user to play the audio using Streamlit's audio component
            st.audio(audio_path, format='audio/mp3')
            
            # Allow the user to download the audio file
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.download_button(
                    label="Download Audio",
                    data=audio_bytes,
                    file_name="output.mp3",
                    mime="audio/mp3"
                )
        else:
            st.write("No text found in the PDF.")
else:
    st.write("Upload a PDF to get started.")
# import streamlit as st
# import pyttsx3
# from PyPDF2 import PdfReader
# from pydub import AudioSegment
# from pydub.playback import play
# import threading
# import os

# # Function to list available voices for TTS
# def list_voices():
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     voice_options = {}
#     for voice in voices:
#         voice_options[voice.name] = voice.id
#     return voice_options

# # Function to convert PDF to audio and save it as a temporary MP3 file
# def convert_pdf_to_audio(pdf_file, reading_speed=1.0, voice_type="Male", pages=None):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', int(150 * reading_speed))
    
#     voices = engine.getProperty('voices')
#     voice_mapping = {
#         "Male": voices[0].id,  # Default Microsoft David
#         "Female": voices[1].id,  # Default Microsoft Zira
#     }
    
#     selected_voice = voice_mapping.get(voice_type, voices[0].id)
#     engine.setProperty('voice', selected_voice)
    
#     pdf_reader = PdfReader(pdf_file)
#     text = ""
    
#     if pages is not None:
#         # Extract specific pages
#         selected_pages = extract_pages(pdf_reader, pages)
#         for page in selected_pages:
#             text += page.extract_text() if page.extract_text() else ""
#     else:
#         # Read all pages if no specific pages provided
#         for page in pdf_reader.pages:
#             text += page.extract_text() if page.extract_text() else ""
    
#     if not text:
#         return None
    
#     output_audio_file = "temp_audio.mp3"
#     engine.save_to_file(text, output_audio_file)
#     engine.runAndWait()
    
#     return output_audio_file

# # Function to extract specific pages based on user input
# def extract_pages(pdf_reader, page_selection):
#     pages = []
#     num_pages = len(pdf_reader.pages)
    
#     # Parse the input to handle ranges and specific pages
#     selections = page_selection.split(",")
#     pages = []

#     for sel in selections:
#         sel = sel.strip()

#         if "-" in sel:
#             # Handle ranges like "1-3"
#             try:
#                 start, end = map(int, sel.split("-"))
#                 if start > 0 and end <= num_pages and start <= end:
#                     pages.extend(pdf_reader.pages[start - 1:end])
#                 else:
#                     st.write(f"Invalid range: {sel}")
#             except ValueError:
#                 st.write(f"Invalid range format: {sel}")
#         else:
#             # Handle specific pages
#             try:
#                 if sel.isdigit():
#                     page_num = int(sel)
#                     if 0 < page_num <= num_pages:
#                         pages.append(pdf_reader.pages[page_num - 1])
#                     else:
#                         st.write(f"Invalid page number: {sel}")
#                 else:
#                     st.write(f"Invalid page number format: {sel}")
#             except ValueError:
#                 st.write(f"Unable to parse page number: {sel}")
    
#     return pages

# # Function to play audio in a separate thread
# def play_audio_thread(audio_path):
#     audio = AudioSegment.from_file(audio_path)
#     play(audio)

# # Streamlit App Interface
# st.title("PDF to Audio Converter")

# # Initialize session state for playback control
# if 'audio_playing' not in st.session_state:
#     st.session_state.audio_playing = False

# # Upload the PDF file
# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
# if uploaded_file is not None:
#     st.write("File uploaded successfully.")
    
#     # Voice selection
#     voice_options = list_voices()
#     voice_type = st.selectbox("Select Voice", list(voice_options.keys()))
    
#     # Reading speed
#     reading_speed = st.slider("Select Reading Speed", 0.5, 2.0, 1.0, 0.1)
    
#     # Page selection dropdown
#     page_selection_option = st.selectbox("Select Pages", ["Entire Document", "Specific Pages"])
    
#     # Handle specific page input based on the dropdown selection
#     page_selection = None
#     if page_selection_option == "Specific Pages":
#         num_pages = len(PdfReader(uploaded_file).pages)
#         st.write(f"This PDF has {num_pages} pages.")
#         page_selection = st.text_input("Enter Pages (e.g., 1-3, 5, 7-9)", "")
    
#     # Convert PDF to audio
#     if st.button("Convert to Audio"):
#         st.write("Converting...")
#         if page_selection_option == "Entire Document":
#             page_selection = None  # Process the entire document if this option is chosen
#         audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, voice_type, page_selection)
        
#         if audio_path:
#             st.write("Conversion complete.")
            
#             # Start playback in a background thread if not already playing
#             if not st.session_state.audio_playing:
#                 st.session_state.audio_playing = True
#                 threading.Thread(target=play_audio_thread, args=(audio_path,)).start()
#                 st.write("Playing audio...")

#             # Allow the user to download the audio file
#             with open(audio_path, 'rb') as audio_file:
#                 audio_bytes = audio_file.read()
#                 st.download_button(
#                     label="Download Audio",
#                     data=audio_bytes,
#                     file_name="output.mp3",
#                     mime="audio/mp3"
#                 )
#         else:
#             st.write("No text found in the PDF.")
# else:
#     st.write("Upload a PDF to get started.")


# import streamlit as st
# import pyttsx3
# from PyPDF2 import PdfReader
# import os
# from pydub import AudioSegment
# from pydub.playback import play
# import threading

# # Function to list available voices for TTS
# def list_voices():
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     voice_options = {}
#     for voice in voices:
#         voice_options[voice.name] = voice.id
#     return voice_options

# # Function to convert PDF to audio and save it as an MP3 file
# def convert_pdf_to_audio(pdf_file, reading_speed=1.0, voice_type="Male", pages=None):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', int(150 * reading_speed))
    
#     voices = engine.getProperty('voices')
#     voice_mapping = {
#         "Male": voices[0].id,  # Default Microsoft David
#         "Female": voices[1].id,  # Default Microsoft Zira
#     }
    
#     selected_voice = voice_mapping.get(voice_type, voices[0].id)
#     engine.setProperty('voice', selected_voice)
    
#     pdf_reader = PdfReader(pdf_file)
#     text = ""
    
#     if pages is not None:
#         # Extract specific pages
#         selected_pages = extract_pages(pdf_reader, pages)
#         for page in selected_pages:
#             text += page.extract_text() if page.extract_text() else ""
#     else:
#         # Read all pages if no specific pages provided
#         for page in pdf_reader.pages:
#             text += page.extract_text() if page.extract_text() else ""
    
#     if not text:
#         return None
    
#     output_audio_file = "temp_audio.mp3"
#     engine.save_to_file(text, output_audio_file)
#     engine.runAndWait()
    
#     return output_audio_file

# # Function to extract specific pages based on user input
# def extract_pages(pdf_reader, page_selection):
#     pages = []
#     num_pages = len(pdf_reader.pages)
    
#     # Parse the input to handle ranges and specific pages
#     selections = page_selection.split(",")
#     pages = []

#     for sel in selections:
#         sel = sel.strip()

#         if "-" in sel:
#             # Handle ranges like "1-3"
#             try:
#                 start, end = map(int, sel.split("-"))
#                 if start > 0 and end <= num_pages and start <= end:
#                     pages.extend(pdf_reader.pages[start - 1:end])
#                 else:
#                     st.write(f"Invalid range: {sel}")
#             except ValueError:
#                 st.write(f"Invalid range format: {sel}")
#         else:
#             # Handle specific pages
#             try:
#                 if sel.isdigit():
#                     page_num = int(sel)
#                     if 0 < page_num <= num_pages:
#                         pages.append(pdf_reader.pages[page_num - 1])
#                     else:
#                         st.write(f"Invalid page number: {sel}")
#                 else:
#                     st.write(f"Invalid page number format: {sel}")
#             except ValueError:
#                 st.write(f"Unable to parse page number: {sel}")
    
#     return pages

# # Function to play audio in a separate thread
# def play_audio(audio):
#     play(audio)

# # Streamlit App Interface
# st.title("PDF to Audio Converter")

# # Upload the PDF file
# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
# if uploaded_file is not None:
#     st.write("File uploaded successfully.")
    
#     # Voice selection
#     voice_options = list_voices()
#     voice_type = st.selectbox("Select Voice", list(voice_options.keys()))
    
#     # Reading speed
#     reading_speed = st.slider("Select Reading Speed", 0.5, 2.0, 1.0, 0.1)
    
#     # Page selection dropdown
#     page_selection_option = st.selectbox("Select Pages", ["Entire Document", "Specific Pages"])
    
#     # Handle specific page input based on the dropdown selection
#     page_selection = None
#     if page_selection_option == "Specific Pages":
#         num_pages = len(PdfReader(uploaded_file).pages)
#         st.write(f"This PDF has {num_pages} pages.")
#         page_selection = st.text_input("Enter Pages (e.g., 1-3, 5, 7-9)", "")
    
#     # Convert PDF to audio
#     if st.button("Convert to Audio"):
#         st.write("Converting...")
#         if page_selection_option == "Entire Document":
#             page_selection = None  # Process the entire document if this option is chosen
#         audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, voice_type, page_selection)
        
#         if audio_path:
#             st.write("Conversion complete.")
            
#             # Load audio using pydub for playback control
#             audio = AudioSegment.from_file(audio_path)
            
#             # Start playback in a background thread
#             if st.button("Play Audio"):
#                 threading.Thread(target=play_audio, args=(audio,)).start()
            
#             # Allow the user to download the audio file
#             with open(audio_path, 'rb') as audio_file:
#                 audio_bytes = audio_file.read()
#                 st.download_button(
#                     label="Download Audio",
#                     data=audio_bytes,
#                     file_name="output.mp3",
#                     mime="audio/mp3"
#                 )
#         else:
#             st.write("No text found in the PDF.")
# else:
#     st.write("Upload a PDF to get started.")



