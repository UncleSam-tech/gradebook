from flask import Flask, jsonify
app = Flask(__name__)

# Accept both "/" and "/api/ping"
@app.post("/", defaults={"_": ""})
@app.get("/api/ping")
def main():
    return jsonify({"ok": True, "fn": "ping"})
