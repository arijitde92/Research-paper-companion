from quart import g, abort, Quart, render_template, url_for, request, redirect, flash
from quart_db import QuartDB
from quart_schema import QuartSchema, validate_request, validate_response
from quart_uploads import UploadSet, configure_uploads, DOCUMENTS
from dotenv import load_dotenv
import os
import asyncio

app = Quart(__name__)
load_dotenv()

UPLOAD_FOLDER = './uploaded_files'
UPLOADED_FILES_DEST = './uploaded_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_FILES_DEST'] = UPLOADED_FILES_DEST
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['QUART_APP'] = os.getenv('QUART_APP')
app.config['QUART_ENV'] = os.getenv('QUART_ENV')
app.config['DB_USER'] = os.getenv('DB_USER')
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['DB_NAME'] = os.getenv('DB_NAME')
app.config['DB_PORT'] = os.getenv('DB_PORT')
app.config['DB_HOST'] = os.getenv('DB_HOST')

uploaded_docs = UploadSet('files', DOCUMENTS)
configure_uploads(app, uploaded_docs)

database_url = f"postgresql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}@{app.config['DB_HOST']}:{app.config['DB_PORT']}/{app.config['DB_NAME']}"
print(database_url)
QuartDB(app, url=database_url)
QuartSchema(app)

messages = [{'sender': 'bot', 'text': 'Hi! How may I help you?'},
            {'sender': 'user', 'text': 'I want to know more about black holes'},
            {'sender': 'bot', 'text': 'Certainly. Black holes are black colored holes'},
            {'sender': 'user', 'text': "That's great! Thanks"}]


@app.route("/chat")
async def chat():
    return await render_template('chat.html', messages=messages)


@app.route("/enter_question", methods=['POST'])
async def new_message():
    if request.method == 'POST':
        sender = 'user'
        data_dict = await request.form
        messages.append({'sender': sender, 'text': data_dict['txtQuestion']})
        messages.append({'sender': 'bot', 'text': 'Reply from AI: ...'})
    return redirect(url_for('chat'))


@app.route("/upload_pdf", methods=['POST'])
async def upload_file():
    """New post route."""
    if request.method == 'POST':
        files = await request.files
        form = await request.form
        doc = files.get('file-upload')
        filename = await uploaded_docs.save(doc, name='user/assignment1.')
        await flash("Post Successfully", "success")
        print("File uploaded to ", filename)
        return 'OK'
    else:
        return redirect(url_for('chat'))

if __name__ == "__main__":
    app.run(debug=True)
