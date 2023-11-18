from quart import g, abort, Quart, render_template
from quart_db import QuartDB
from quart_schema import QuartSchema, validate_request, validate_response
from dotenv import load_dotenv
import os
import asyncio

app = Quart(__name__)
load_dotenv()
app.config['QUART_APP'] = os.getenv('QUART_APP')
app.config['QUART_ENV'] = os.getenv('QUART_ENV')
app.config['DB_USER'] = os.getenv('DB_USER')
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['DB_NAME'] = os.getenv('DB_NAME')
app.config['DB_PORT'] = os.getenv('DB_PORT')
app.config['DB_HOST'] = os.getenv('DB_HOST')
# db_params = config()
# database_url = f"postgresql://{db_params['user']}:@{db_params['host']}:{db_params['port']}/{db_params['database']}"

database_url = f"postgresql://{app.config['DB_NAME']}:{app.config['DB_PASSWORD']}@{app.config['DB_HOST']}:{app.config['DB_PORT']}/{app.config['DB_NAME']}"
QuartDB(app, url=database_url)
QuartSchema(app)
