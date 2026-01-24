from flask import Flask
import os

app = Flask(__name__)

# Используем порт, который Render даёт через переменную окружения
PORT = int(os.environ.get("PORT", 5000))

@app.route("/")
def hello():
    return "Hello, Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)