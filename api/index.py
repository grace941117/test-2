from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello World"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# Vercel 需要這個變數
app = app 