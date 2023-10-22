from flask import Flask, request, jsonify, send_file
from concrete import fhe

app = Flask(__name__)
server = fhe.Server.load("server_bubble_sort.zip")

@app.route('/infos', methods=['GET'])
def get_data():
    data = {'message': 'Api is working'}
    return jsonify(data)

@app.route('/getsepcs', methods=['GET'])
def get_specs():
    serialized_client_specs: str = server.client_specs.serialize()
    return serialized_client_specs

@app.route('/postkeys', methods=['POST'])
def post_keys():
    serialized_evaluation_keys: bytes = request.data
    deserialized_evaluation_keys = fhe.EvaluationKeys.deserialize(serialized_evaluation_keys)
    return "Success"

@app.route('/process', methods=['POST'])
def process():
    
    serialized_evaluation_keys: bytes = request.data
    deserialized_evaluation_keys = fhe.EvaluationKeys.deserialize(serialized_evaluation_keys)
    
    file_path = "uploaded_file.bin"
    with open(file_path, "rb") as file:
        data = file.read()

    deserialized_arg = fhe.Value.deserialize(data)

    result:fhe.Value = server.run(deserialized_arg, evaluation_keys=deserialized_evaluation_keys)

    serialized_result:bytes = result.serialize()
    with open("enc_result.bin", "wb") as file:
        file.write(serialized_result)

    return "Success"
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    file.save("uploaded_file.bin")
    return 'File uploaded successfully', 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Define the path to the file you want to serve
    file_path = filename  # Replace with the actual file path
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8080)