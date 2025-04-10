from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import os
import sys

# 從環境變數獲取 API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .chat-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .chat-messages {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #f1f1f1;
            margin-right: 20%;
        }
        .input-container {
            display: flex;
        }
        #user-input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>AI Chatbot</h1>
        <div class="chat-messages" id="chat-messages"></div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your message here...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function addMessage(message, isUser) {
            const chatMessages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value.trim();
            
            if (message) {
                addMessage(message, true);
                userInput.value = '';
                
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, false);
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('Sorry, there was an error processing your request.', false);
                });
            }
        }

        // 按 Enter 鍵發送消息
        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

# 路由：主頁
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# 路由：聊天 API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

# 路由：健康檢查
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# CLI 模式
def cli_mode():
    print("AI Chatbot CLI Mode (Type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        try:
            response = model.generate_content(user_input)
            print(f"AI: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

# Vercel 需要這個變數
app = app

# 主程式
if __name__ == '__main__':
    # 檢查是否以 CLI 模式運行
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        cli_mode()
    else:
        # 否則以 Web 模式運行
        app.run(debug=True) 