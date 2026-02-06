from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def upload():
    if request.method == "GET":
        return "Send a POST request with a file to analyze."

    # Get uploaded file
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    # Basic analysis: count lines in file
    try:
        content = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        return jsonify({"error": "File must be a text file"}), 400

    line_count = len(content.splitlines())

    # Send safe summary to webhook (secure via env variable)
    webhook_url = os.environ.get("https://discord.com/api/webhooks/1441945338435997847/_kC65SYRounkuvO9pstQ3izVMpkgV4a9pk01IBC5nbJ6ue34lTmDoa7gexFqOtdG7k7P")
    if webhook_url:
        try:
            requests.post(webhook_url, json={
                "summary": f"A user uploaded a file with {line_count} lines"
            })
        except Exception:
            pass  # Do not break the API if webhook fails

    return jsonify({"message": "File processed safely", "lines": line_count})
