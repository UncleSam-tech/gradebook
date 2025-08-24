from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
@app.get("/api/ping")
def main():
    return jsonify({"ok": True, "fn": "ping"})
