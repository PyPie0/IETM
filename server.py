from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Server response.</h1>"


if __name__ == "__main__":
    app.run(host="192.168.0.102", port=5000)