from flask import Flask, render_template, request
from chatbot_g import chatbot_g

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot_g(userText))

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0') 
