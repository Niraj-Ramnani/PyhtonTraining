# 2. Create /request-info endpoint returning method, headers, query parameters, client IP and server time. Test with Browser, Postman and cURL.
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "This is home page of assignment 2 "
    })

@app.route("/request-info")
def request_info():
    return jsonify({
        "method": request.method,
        "headers": dict(request.headers),
        "query_parameters": request.args.to_dict(),
        "client_ip": request.remote_addr,
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


if __name__ == "__main__":
    app.run(debug=True)