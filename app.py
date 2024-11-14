from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()  # Retrieve JSON data from request
    if data:
        print("Received JSON data:", data)

        # Forward data to the specified URL
        try:
            response = requests.post("https://172.218.153.209/addGasses", json=data,
                                     verify=False)  # verify=False ignores SSL cert validation
            if response.status_code == 200:
                return jsonify({"status": "success", "message": "Data received and forwarded"}), 200
            else:
                return jsonify({"status": "error", "message": "Failed to forward data"}), response.status_code
        except requests.RequestException as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    else:
        return jsonify({"status": "error", "message": "No JSON received"}), 400


@app.route('/dangerLevels', methods=['GET'])
def receive_alert():
    # Make a request to the source endpoint
    response = requests.get("https://172.218.153.209/dangerLevels",
                            verify=False)  # verify=False ignores SSL cert validation
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Get the string data from the response
    string_data = response.text

    # Print the string to the terminal
    print("Fetched string:", string_data)

    # Return the string as a JSON response
    return jsonify({"fetched_string": string_data}), 200


if __name__ == '__main__':
    app.run()
