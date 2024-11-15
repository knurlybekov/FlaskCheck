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
    try:
        response = requests.post("https://172.218.153.209/dangerLevels", verify=False)
        response.raise_for_status()
        string_data = response.text
        print("Fetched string:", string_data)
        return jsonify({"fetched_string": string_data}), 200
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    app.run()
