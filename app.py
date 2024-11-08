from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()  # Retrieve JSON data from request
    if data:
        print("Received JSON data:", data)
        return jsonify({"status": "success", "message": "Data received"}), 200
    else:
        return jsonify({"status": "error", "message": "No JSON received"}), 400


if __name__ == '__main__':
    app.run()
