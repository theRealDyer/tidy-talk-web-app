import os
from flask import Flask, render_template, request, send_file, make_response
from docx import Document
from openai import OpenAI
from dotenv import load_dotenv
import io

load_dotenv() # loads environment variables (e.g. API key) from .env file 

app = Flask(__name__)

# Function to process the audio file
def process_audio(audio_file):

    # Read the content of the audio file as bytes
    audio_content = audio_file.read()

    # Wrap the audio content as a file-like object with a 'name' attribute
    audio_file_like_obj = io.BytesIO(audio_content)
    audio_file_like_obj.name = audio_file.filename

    # Assign my personal api key
    client = OpenAI(api_key = os.getenv('API_KEY'))


    ### STT SECTION

    # Pass the audio content as a file-like object
    result = client.audio.transcriptions.create(model="whisper-1", file=audio_file_like_obj)

    # assign transcribed text to variable
    stt_original = result.text

    ### CHATGPT PROMPT-REQUEST

    # run chat prompt request
    chat_request = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": f"""
    I have some text that is about a subject and will begin after the phrase "Here is the text:". Please do the following to it:
    - Clean it up to ensure the structure reads well, giving it paragraphs, etc.
    - Remove any parts that are duplications of other parts.
    - Check for grammatical errors and punctuation and fix them.
    - Correct any factual mistakes.
    - recognise the main theme and content of the text and remove anything that is irrelevant or doesn't fit the theme.
    Here is the text:
                            '''
                            {stt_original}
                            '''
    """}])

    chat_output = chat_request.choices[0].message.content

    ### EXPORT STRING TO DOC FILE

    # Create a new Document
    doc_out = Document()
    # Add a paragraph with your string
    doc_out.add_paragraph(chat_output)

    return doc_out


# old (working) index() function

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
    template = render_template('index.html')
    response = make_response(template)
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response


# @app.route('/process', methods=['POST'])
# def process():
#     audio_file = request.files['audio_file']

#     if audio_file:
#         # Process the audio file and get the output doc file
#         doc_file = process_audio(audio_file)

#         # Save the Document object to a temporary file
#         temp_output_path = "temp_output.docx"
#         doc_file.save(temp_output_path)

#         # Provide the processed doc file for download
#         return send_file(
#             temp_output_path,
#             mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#             as_attachment=True,
#             download_name='output.docx'
#         )


#     return "No file uploaded!"

@app.route('/process', methods=['POST'])
def process():
    audio_file = request.files['audio_file']

    if audio_file:
        # Get the desired output filename based on the input audio file name
        input_filename = audio_file.filename
        output_filename = f"{os.path.splitext(input_filename)[0]}_transformed.docx"

        # Process the audio file and get the output doc file
        doc_file = process_audio(audio_file)

        # Save the Document object to the provided output filename
        doc_file.save(output_filename)

        # Provide the processed doc file for download
        return send_file(
            output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=output_filename  # Set the download name to the dynamic output filename
        )

    return "No file uploaded!"


if __name__ == '__main__':
    app.run(debug=True, port=8000)





