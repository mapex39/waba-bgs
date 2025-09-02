from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return "Webhook çalışıyor!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Gelen veri:", data)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)