from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
REQUEST_COUNTER = Counter('http_requests_total', "Total HTPP Requests")

@app.route('/<name>')
def hello(name):
    REQUEST_COUNTER.inc()
    return f"Hello, {name}\n"

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

