import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS

# Authentication function
def authenticate():
    credentials = {
        "Yusuf Abdul": {"name": "Yusuf Abdul", "password": "1234"},
        "Solomon Lange": {"name": "Solomon Lange", "password": "5678"}
    }

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        # Validate credentials
        if username in credentials and password == credentials[username]["password"]:
            st.session_state['authenticated'] = True
            st.session_state['username'] = credentials[username]['name']
            st.success(f"Welcome, {credentials[username]['name']}!")  # Display success message
            st.session_state['show_upload'] = True  # Set the flag to show the upload interface
        else:
            st.error("Invalid username or password. Please try again.")

# PDF Upload Interface function
def pdf_upload_interface():
    st.title(f"Welcome, {st.session_state['username']}!")
    st.markdown("A Project by **YUSUF ABDUL** - NACEST/COM/HND22/780")
    st.write("(Department of Computer Science)")
    st.markdown("*Supervisor:* Mr. Ike Innocent")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file:
        st.write("File uploaded successfully.")
        
        # Voice selection
        voice_type = st.selectbox("Select Voice", ["Male", "Female"])

        # Reading speed
        reading_speed = st.slider("Select Reading Speed", 0.5, 2.0, 1.0, 0.1)

        # Page selection dropdown
        page_selection_option = st.selectbox("Select Pages", ["Entire Document", "Specific Pages"])

        page_selection = None
        if page_selection_option == "Specific Pages":
            num_pages = len(PdfReader(uploaded_file).pages)
            st.write(f"This PDF has {num_pages} pages.")
            page_selection = st.text_input("Enter Pages (e.g., 1-3, 5, 7-9)", "")

        # Convert PDF to audio
        if st.button("Convert to Audio"):
            if page_selection_option == "Entire Document":
                page_selection = None

            # Simulated function call to convert PDF to audio
            # audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, page_selection)
            # Assuming success
            audio_path = "output.mp3"
            
            if audio_path:
                st.audio(audio_path, format='audio/mp3')
                with open(audio_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                    st.download_button(
                        label="Download Audio",
                        data=audio_bytes,
                        file_name="output.mp3",
                        mime="audio/mp3"
                    )
            else:
                st.error("No text found in the PDF.")
    else:
        st.write("Upload a PDF to get started.")

# Main logic
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Step 1: Authentication
if not st.session_state['authenticated']:
    st.title("Login Page")
    authenticate()
else:
    # Step 2: Show the PDF upload interface only if authenticated
    if st.session_state.get('show_upload', False):
        pdf_upload_interface()


# import streamlit as st
# from PyPDF2 import PdfReader
# from gtts import gTTS
# import os

# # Authentication function
# def authenticate():
#     credentials = {
#         "Yusuf Abdul": {"name": "Yusuf Abdul", "password": "1234"},
#         "Solomon Lange": {"name": "Solomon Lange", "password": "5678"}
#     }

#     username = st.text_input("Enter Username")
#     password = st.text_input("Enter Password", type="password")

#     if st.button("Login"):
#         if username in credentials and password == credentials[username]["password"]:
#             st.session_state['authenticated'] = True
#             st.session_state['username'] = credentials[username]['name']
#             st.success(f"Welcome, {credentials[username]['name']}!")
#         else:
#             st.error("Invalid username or password. Please try again.")

# # Function to convert PDF to audio and save it as an MP3 file using gTTS
# def convert_pdf_to_audio(pdf_file, reading_speed=1.0, pages=None):
#     pdf_reader = PdfReader(pdf_file)
#     text = ""

#     if pages:
#         selected_pages = extract_pages(pdf_reader, pages)
#         for page in selected_pages:
#             text += page.extract_text() or ""
#     else:
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""

#     if not text.strip():
#         st.error("No text found in the PDF.")
#         return None
    
#     output_audio_file = "output.mp3"
#     try:
#         tts = gTTS(text, lang='en', slow=False)
#         tts.save(output_audio_file)
#         return output_audio_file
#     except Exception as e:
#         st.error(f"Error during audio conversion: {e}")
#         return None

# # Extract specific pages from the PDF
# def extract_pages(pdf_reader, page_selection):
#     pages = []
#     num_pages = len(pdf_reader.pages)
    
#     selections = page_selection.split(",")

#     for sel in selections:
#         sel = sel.strip()
#         if "-" in sel:
#             start, end = map(int, sel.split("-"))
#             pages.extend(pdf_reader.pages[start-1:end])
#         else:
#             page_num = int(sel)
#             pages.append(pdf_reader.pages[page_num - 1])

#     return pages

# # Main application
# if 'authenticated' not in st.session_state:
#     st.session_state['authenticated'] = False

# if not st.session_state['authenticated']:
#     st.title("Login Page")
#     authenticate()
# else:
#     st.title(f"Welcome, {st.session_state['username']}!")
#     st.markdown("A Project by **YUSUF ABDUL** - NACEST/COM/HND22/780")
#     st.write("(Department of Computer Science)")
#     st.markdown("*Supervisor:* Mr. Ike Innocent")

#     # Upload the PDF file
#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
#     if uploaded_file:
#         st.write("File uploaded successfully.")

#         # Voice selection
#         voice_type = st.selectbox("Select Voice", ["Male", "Female"])

#         # Reading speed
#         reading_speed = st.slider("Select Reading Speed", 0.5, 2.0, 1.0, 0.1)

#         # Page selection dropdown
#         page_selection_option = st.selectbox("Select Pages", ["Entire Document", "Specific Pages"])

#         page_selection = None
#         if page_selection_option == "Specific Pages":
#             num_pages = len(PdfReader(uploaded_file).pages)
#             st.write(f"This PDF has {num_pages} pages.")
#             page_selection = st.text_input("Enter Pages (e.g., 1-3, 5, 7-9)", "")

#         # Convert PDF to audio
#         if st.button("Convert to Audio"):
#             if page_selection_option == "Entire Document":
#                 page_selection = None

#             audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, page_selection)

#             if audio_path:
#                 st.audio(audio_path, format='audio/mp3')
#                 with open(audio_path, 'rb') as audio_file:
#                     audio_bytes = audio_file.read()
#                     st.download_button(
#                         label="Download Audio",
#                         data=audio_bytes,
#                         file_name="output.mp3",
#                         mime="audio/mp3"
#                     )
#             else:
#                 st.error("No text found in the PDF.")
#     else:
#         st.write("Upload a PDF to get started.")



# import streamlit as st
# from PyPDF2 import PdfReader
# from gtts import gTTS
# import os

# # Authentication function
# def authenticate():
#     # Predefined credentials
#     credentials = {
#         "SSID1": {"name": "Yusuf Abdul", "password": "1234"},
#         "SSID2": {"name": "Solomon Lange", "password": "5678"}
#     }

#     # Prompt for SSID and password
#     ssid = st.text_input("Enter SSID")
#     password = st.text_input("Enter Password", type="password")

#     # Button to submit credentials
#     if st.button("Login"):
#         # Check if SSID exists
#         if ssid in credentials:
#             # Verify the password
#             if password == credentials[ssid]["password"]:
#                 st.success(f"Welcome, {credentials[ssid]['name']}!")
#                 return True
#             else:
#                 st.error("Incorrect password. Please try again.")
#                 return False
#         else:
#             st.error("Invalid SSID. Please try again.")
#             return False

#     # Return False if no attempt to log in is made yet
#     return False

# # Function to convert PDF to audio and save it as an MP3 file using gTTS
# def convert_pdf_to_audio(pdf_file, reading_speed=1.0, pages=None):
#     pdf_reader = PdfReader(pdf_file)
#     text = ""

#     if pages is not None:
#         selected_pages = extract_pages(pdf_reader, pages)
#         for page in selected_pages:
#             page_text = page.extract_text() if page.extract_text() else ""
#             if page_text:
#                 text += page_text
#             else:
#                 st.write("No text found on the selected page.")
#     else:
#         for page in pdf_reader.pages:
#             page_text = page.extract_text() if page.extract_text() else ""
#             if page_text:
#                 text += page_text

#     # Debugging: Display the extracted text length and preview
#     st.write("Extracted Text Length:", len(text))

#     if not text.strip():  # Check if text is empty or just whitespace
#         st.write("No text found in the PDF.")
#         return None
    
#     # Convert text to audio using gTTS and save directly to a file
#     output_audio_file = "output.mp3"  # File name for the output audio
#     try:
#         tts = gTTS(text, lang='en', slow=False)
#         tts.save(output_audio_file)  # Save the audio to a file

#         st.write("Audio conversion successful.")
#         return output_audio_file  # Return the file path for further use
#     except Exception as e:
#         st.write("Error during audio conversion:", e)
#         return None

# # Function to extract specific pages based on user input
# def extract_pages(pdf_reader, page_selection):
#     pages = []
#     num_pages = len(pdf_reader.pages)
    
#     # Parse the input to handle ranges and specific pages
#     selections = page_selection.split(",")
    
#     for sel in selections:
#         sel = sel.strip()
#         if "-" in sel:
#             # Handle ranges like "1-3"
#             try:
#                 start, end = map(int, sel.split("-"))
#                 if 1 <= start <= num_pages and 1 <= end <= num_pages and start <= end:
#                     for i in range(start - 1, end):  # Zero-based index
#                         pages.append(pdf_reader.pages[i])
#                 else:
#                     st.write(f"Invalid range: {sel}")
#             except ValueError:
#                 st.write(f"Invalid range format: {sel}")
#         else:
#             # Handle specific pages
#             try:
#                 if sel.isdigit():
#                     page_num = int(sel)
#                     if 1 <= page_num <= num_pages:
#                         pages.append(pdf_reader.pages[page_num - 1])  # Zero-based index
#                     else:
#                         st.write(f"Invalid page number: {sel}")
#                 else:
#                     st.write(f"Invalid page number format: {sel}")
#             except ValueError:
#                 st.write(f"Unable to parse page number: {sel}")

#     return pages

# # Streamlit App Interface
# st.title("PDF to Audio Converter")
# st.markdown("A Project by **YUSUF ABDUL** - NACEST/COM/HND22/780")
# st.write("(Department of Computer Science)")
# st.markdown("*Supervisor:* Mr. Ike Innocent")

# # Authentication step
# if authenticate():
#     # Upload the PDF file
#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
#     if uploaded_file is not None:
#         st.write("File uploaded successfully.")
        
#         # Voice selection
#         voice_type = st.selectbox("Select Voice", ["Male", "Female"])
        
#         # Reading speed
#         reading_speed = st.slider("Select Reading Speed", 0.5, 2.0, 1.0, 0.1)
        
#         # Page selection dropdown
#         page_selection_option = st.selectbox("Select Pages", ["Entire Document", "Specific Pages"])
        
#         # Handle specific page input based on the dropdown selection
#         page_selection = None
#         if page_selection_option == "Specific Pages":
#             num_pages = len(PdfReader(uploaded_file).pages)
#             st.write(f"This PDF has {num_pages} pages.")
#             page_selection = st.text_input("Enter Pages (e.g., 1-3, 5, 7-9)", "")
        
#         # Convert PDF to audio
#         if st.button("Convert to Audio"):
#             st.write("Converting...")
#             if page_selection_option == "Entire Document":
#                 page_selection = None  # Process the entire document if this option is chosen
#             audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, page_selection)
            
#             if audio_path:
#                 st.write("Conversion complete.")
                
#                 # Allow the user to play the audio using Streamlit's audio component
#                 st.audio(audio_path, format='audio/mp3')
                
#                 # Allow the user to download the audio file
#                 with open(audio_path, 'rb') as audio_file:
#                     audio_bytes = audio_file.read()
#                     st.download_button(
#                         label="Download Audio",
#                         data=audio_bytes,
#                         file_name="output.mp3",
#                         mime="audio/mp3"
#                     )
#             else:
#                 st.write("No text found in the PDF.")
#     else:
#         st.write("Upload a PDF to get started.")
# else:
#     st.write("Authentication required to access the tool.")



# import streamlit as st
# from PyPDF2 import PdfReader
# from gtts import gTTS
# import os

# # Function to convert PDF to audio and save it as an MP3 file using gTTS
# def convert_pdf_to_audio(pdf_file, reading_speed=1.0, pages=None):
#     pdf_reader = PdfReader(pdf_file)
#     text = ""

#     if pages is not None:
#         selected_pages = extract_pages(pdf_reader, pages)
#         for page in selected_pages:
#             page_text = page.extract_text() if page.extract_text() else ""
#             if page_text:
#                 text += page_text
#             else:
#                 st.write("No text found on the selected page.")
#     else:
#         for page in pdf_reader.pages:
#             page_text = page.extract_text() if page.extract_text() else ""
#             if page_text:
#                 text += page_text

#     # Debugging: Display the extracted text length and preview
#     st.write("Extracted Text Length:", len(text))
#     # st.write("Extracted Text Preview:", text[:500])  # Display a preview of the first 500 characters

#     if not text.strip():  # Check if text is empty or just whitespace
#         st.write("No text found in the PDF.")
#         return None
    
#     # Convert text to audio using gTTS and save directly to a file
#     output_audio_file = "output.mp3"  # File name for the output audio
#     try:
#         tts = gTTS(text, lang='en', slow=False)
#         tts.save(output_audio_file)  # Save the audio to a file

#         st.write("Audio conversion successful.")
#         return output_audio_file  # Return the file path for further use
#     except Exception as e:
#         st.write("Error during audio conversion:", e)
#         return None

# # Function to extract specific pages based on user input
# def extract_pages(pdf_reader, page_selection):
#     pages = []
#     num_pages = len(pdf_reader.pages)
    
#     # Parse the input to handle ranges and specific pages
#     selections = page_selection.split(",")
    
#     for sel in selections:
#         sel = sel.strip()
#         if "-" in sel:
#             # Handle ranges like "1-3"
#             try:
#                 start, end = map(int, sel.split("-"))
#                 if 1 <= start <= num_pages and 1 <= end <= num_pages and start <= end:
#                     for i in range(start - 1, end):  # Zero-based index
#                         pages.append(pdf_reader.pages[i])
#                 else:
#                     st.write(f"Invalid range: {sel}")
#             except ValueError:
#                 st.write(f"Invalid range format: {sel}")
#         else:
#             # Handle specific pages
#             try:
#                 if sel.isdigit():
#                     page_num = int(sel)
#                     if 1 <= page_num <= num_pages:
#                         pages.append(pdf_reader.pages[page_num - 1])  # Zero-based index
#                     else:
#                         st.write(f"Invalid page number: {sel}")
#                 else:
#                     st.write(f"Invalid page number format: {sel}")
#             except ValueError:
#                 st.write(f"Unable to parse page number: {sel}")

#     return pages

# # Streamlit App Interface
# st.title("PDF to Audio Converter")
# st.markdown("A Project by **YUSUF ABDUL** - NACEST/COM/HND22/780")
# st.write("(Departmet of Computer Science)")
# # st.markdown("<u>text</u>", unsafe_allow_html=True)  Use this to underline text
# st.markdown("*Supervisor:* Mr. Ike Innocent")

# # Upload the PDF file
# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
# if uploaded_file is not None:
#     st.write("File uploaded successfully.")
    
#     # Voice selection
#     voice_type = st.selectbox("Select Voice", ["Male", "Female"])
    
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
#         audio_path = convert_pdf_to_audio(uploaded_file, reading_speed, page_selection)
        
#         if audio_path:
#             st.write("Conversion complete.")
            
#             # Allow the user to play the audio using Streamlit's audio component
#             st.audio(audio_path, format='audio/mp3')
            
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

#     st.write("Upload a PDF to get started.")



