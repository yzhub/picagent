from flask import Flask, request

from controller.Index import Index

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return Index().runing(request.args)


if __name__ == '__main__':
    app.run(debug=False, host="127.0.0.1", port=80)
