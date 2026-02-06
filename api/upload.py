from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/upload", methods=["POST"])
def upload():
    # Get uploaded file
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    # Example analysis: count lines
    content = uploaded_file.read().decode("utf-8")
    line_count = len(content.splitlines())

    # Send safe summary to webhook
    webhook_url = "https://discord.com/api/webhooks/1441945338435997847/_kC65SYRounkuvO9pstQ3izVMpkgV4a9pk01IBC5nbJ6ue34lTmDoa7gexFqOtdG7k7P"
    requests.post(webhook_url, json={
        "summary": f"User uploaded a file with {line_count} lines"
    })

    return jsonify({"message": "File processed safely", "lines": line_count})

# Required for Vercel Python deployment
def handler(environ, start_response):
    from werkzeug.wrappers import Request, Response
    request = Request(environ)
    response = app.full_dispatch_request()
    return response(environ, start_response)
