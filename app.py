from flask import Flask, render_template, request, jsonify
from model import chatbot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    data = request.get_json()
    user_input = data.get('user_input', '')

    bot_response = chatbot(user_input)

    return jsonify({'reply': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
