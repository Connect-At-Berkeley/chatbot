#import train_chatbot

from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

def send():
    return "<a href=%s>file</a>" % url_for('static', filename='intents.json')

#@app.route("/get")
#def get_bot_response():
#    userText = request.args.get('msg')
    #return str()
    #return str()
#    return str(train_chatbot.chatbot_response(userText))

# create another funtion that gets links


if __name__ == "__main__":
    app.run()
