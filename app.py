# This file should never be open-sourced since we have a lot of tokens exposed
# If we do open-source it, we'll need to create a config.sh script that is only viewable to us that
# sets environment variables corresponding to email usernames and passwords
# We'll also need to create another repo to prevent people from viewing previous commit history with tokens exposed
from __future__ import print_function
import os
import pickle
import os.path
import flask
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import flask_login
import hashlib

from email import header

header.MAXLINELEN = 32

EMAILS_HASHES = {}

# TODO: seperate into views.py, models.py, etc.

app = Flask(__name__)
app.secret_key = 's;ldflkadjfa;slkjfdsa' 


# login_manager = flask_login.LoginManager()

# login_manager.init_app(app)

# users = {'connect.berkeley@gmail.com': {'password': 'Y6Wl8erM8P9E'}}

# class User(flask_login.UserMixin):
#     pass

# @login_manager.user_loader
# def user_loader(email):
#     if email not in users:
#         return

#     user = User()
#     user.id = email
#     return user

# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users:
#         return

#     user = User()
#     user.id = email

#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['password'] == users[email]['password']

#     return user

def load_spreadsheets():
    service = build('sheets', 'v4', credentials=ACCOUNT_INFO)
    spreadsheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")
    range_name = os.environ.get("GOOGLE_CELL_RANGE")

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    data = {}

    index_to_dict_names = {}

    for idx, header_name in enumerate(values[0]):
        data[header_name] = []
        index_to_dict_names[idx] = header_name

    for i in range(1, len(values)):
        for idx, val in enumerate(values[i]):
            header_name_temp = index_to_dict_names[idx]
            data[header_name_temp] += [val]
    
    # counter = 0
    # countEmails = len(data["Email Address"])
    # for i in range(countEmails):
    #     email = data["Email Address"][i]

    #     hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
    #     data["Email Address"][i] = hashed_email
        
    #     if hashed_email not in EMAILS_HASHES:
    #         EMAILS_HASHES[hashed_email] = email

    #     counter+=1
    
    # print(len(data["Email Address"]))

    return data

def load_spreadsheets_2():
    service = build('sheets', 'v4', credentials=ACCOUNT_INFO)
    spreadsheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID_2")
    range_name = os.environ.get("GOOGLE_CELL_RANGE_2")

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    data = {}

    index_to_dict_names = {}

    for idx, header_name in enumerate(values[0]):
        data[header_name] = []
        index_to_dict_names[idx] = header_name

    for i in range(1, len(values)):
        for idx, val in enumerate(values[i]):
            header_name_temp = index_to_dict_names[idx]
            data[header_name_temp] += [val]
    
    # counter = 0
    # countEmails = len(data["Email Address"])
    # for i in range(countEmails):
    #     email = data["Email Address"][i]

    #     hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
    #     data["Email Address"][i] = hashed_email
        
    #     if hashed_email not in EMAILS_HASHES:
    #         EMAILS_HASHES[hashed_email] = email

    #     counter+=1
    
    # print(len(data["Email Address"]))

    return data

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if flask.request.method == 'GET':
#         return '''
#                <form action='/' method='POST'>
#                 <input type='text' name='email' id='email' placeholder='email'/>
#                 <input type='password' name='password' id='password' placeholder='password'/>
#                 <input type='submit' name='submit'/>
#                </form>
#                '''

#     email = flask.request.form['email']
#     if email in users:
#         if flask.request.form['password'] == users[email]['password']:
#             user = User()
#             user.id = email
#             flask_login.login_user(user)
#             return flask.redirect(flask.url_for('protected'))

#     return '''
#                <div>
#                 <p> Bad Login>
#                 <p> <a href="/">Login again</a></p>
#                <div>
#                '''


@app.route('/')
def resources():
    data = load_spreadsheets()
    return render_template('resources.html', values=data)

# @app.route('/club')
# @flask_login.login_required
# def club():
#     data = load_spreadsheets_2()
#     return render_template('club.html', values=data)

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     flask_login.logout_user()
#     return unauthorized_handler()

# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request


def get_account_info():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    GOOGLE_PRIVATE_KEY = os.environ["GOOGLE_PRIVATE_KEY"]
    # The environment variable has escaped newlines, so remove the extra backslash
    GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')

    account_info = {
        "private_key": GOOGLE_PRIVATE_KEY,
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(
        account_info, scopes=scopes)
    return credentials


# Get Creds: https://developers.google.com/sheets/api/quickstart/python?authuser=4
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
ACCOUNT_INFO = get_account_info()
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
# if os.path.exists('token.pickle'):
#     with open('token.pickle', 'rb') as token:
#         creds = pickle.load(token)
# # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             'cal-connect-283117-4264648035cf.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#     # Save the credentials for the next run
#     with open('token.pickle', 'wb') as token:
#         pickle.dump(creds, token)

# Mail


# app.config.update(
#     DEBUG=True,
#     # EMAIL SETTINGS
#     MAIL_SERVER='smtp.ocf.berkeley.edu',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USERNAME='hello@connected.berkeley.edu',
#     MAIL_PASSWORD='iK57NHs0SWp2'
# )
app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='connect.berkeley@gmail.com',
    MAIL_PASSWORD='Connect-berkeley-to-everyone'
)

mail = Mail(app)

@app.route('/send-mail', methods=['POST'])
def send_mail():
    print("in send mail")
    print(request)
    email = request.form["email"]
    real_email = EMAILS_HASHES[email]
    response = request.form["agentResponse"]
    # response = response.replace(" ", "\'&nbsp;\'")
    # response = response.replace("<p>", "<pre>")
    # response = response.replace("</p>", "</pre>")
    if not response:
        return "Cannot email an empty message"
    try:
        msg = Message("Connect@Cal Response",
                      sender="hello@connected.berkeley.edu",
                    #   cc=["connect.berkeley@gmail.com"],
                      recipients=[real_email])
        msg.html = response
        mail.send(msg)
        return render_template('mailsent.html')

    except Exception as e:
        return(str(e))

PROCESSED_DATA = []

# @app.route("/")
# def index():
#     service = build('sheets', 'v4', credentials=ACCOUNT_INFO)
#     spreadsheet_id = os.environ.get("GOOGLE_SPREADSHEET_ID")
#     range_name = os.environ.get("GOOGLE_CELL_RANGE")

#     result = service.spreadsheets().values().get(
#         spreadsheetId=spreadsheet_id, range=range_name).execute()
#     values = result.get('values', [])

#     # To make sure # of cols = # of rows for DataTables library
#     # Sheets API automatically does not return any empty cell values
#     df = pd.DataFrame(values)
#     PROCESSED_DATA = df.replace([''], [None]).values.tolist()

#     return render_template('index.html', values=PROCESSED_DATA)


#import train_chatbot

# from flask import Flask, render_template, request

# app = Flask(__name__)
# app.static_folder = 'static'

# @app.route("/")
# def home():
#     return render_template("index.html")

# def send():
#     return "<a href=%s>file</a>" % url_for('static', filename='intents.json')

# @app.route("/get")
# def get_bot_response():
#    userText = request.args.get('msg')
#     return str()
#     return str()
#    return str(train_chatbot.chatbot_response(userText))

# create another funtion that gets links


# if __name__ == "__main__":
#     app.run()
