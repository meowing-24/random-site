from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def upload():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    content = uploaded_file.read().decode("utf-8")
    line_count = len(content.splitlines())

    webhook_url = os.environ.get("WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json={"summary": f"User uploaded a file with {line_count} lines"})

    return jsonify({"message": "File processed safely", "lines": line_count})
