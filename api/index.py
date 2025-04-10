from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai

# 配置 Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        #chat-container {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
            background-color: white;
            border-radius: 5px;
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
            background-color: #f5f5f5;
            margin-right: 20%;
        }
        #input-container {
            display: flex;
            gap: 10px;
        }
        #user-input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #1976d2;
        }
    </style>
</head>
<body>
    <h1>AI Chat</h1>
    <div id="chat-container"></div>
    <div id="input-container">
        <input type="text" id="user-input" placeholder="輸入您的訊息...">
        <button onclick="sendMessage()">發送</button>
    </div>
    <script>
        function addMessage(message, isUser) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, true);
            input.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                if (data.error) {
                    addMessage('錯誤: ' + data.error, false);
                } else {
                    addMessage(data.response, false);
                }
            } catch (error) {
                addMessage('錯誤: 無法連接到伺服器', false);
            }
        }

        // 按 Enter 鍵發送訊息
        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

def handler(request):
    if request.path == '/':
        return Response(
            HTML_TEMPLATE,
            status=200,
            headers={'Content-Type': 'text/html'}
        )
    elif request.path == '/health':
        return Response(
            json.dumps({"status": "healthy"}),
            status=200,
            headers={'Content-Type': 'application/json'}
        )
    elif request.path == '/chat' and request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = model.generate_content(data.get('message', ''))
            return Response(
                json.dumps({"response": response.text}),
                status=200,
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            return Response(
                json.dumps({"error": str(e)}),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    else:
        return Response(
            json.dumps({"error": "Not Found"}),
            status=404,
            headers={'Content-Type': 'application/json'}
        ) 