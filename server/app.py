from flask import Flask, request, jsonify, send_file
from concrete import fhe
import argparse

app = Flask(__name__)
#server = fhe.Server.load("circuits/server_bubble_sort_chunked.zip")

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
    parser = argparse.ArgumentParser(description="STU Qr Code reader Connector")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to run the API server")
    parser.add_argument("--port", type=int, default="8080", help="Port to run the API server")
    parser.add_argument("--algorithm", type=str, default="topk", help="Algorithm to run. Options: bubble, insertion, topk")
    parser.add_argument("--comparison", type=str, default="OTLU", help="Comparison strategy to use. Options: OTLU, TTLU, chunked")
    args = parser.parse_args()
    
    if(args.algorithm == "bubble" and args.comparison == "OTLU"):
        server = fhe.Server.load("circuits/server_bubble_sort_OTLU.zip")
    elif(args.algorithm == "bubble" and args.comparison == "TTLU"):
        server = fhe.Server.load("circuits/server_bubble_sort_TTLU.zip")
    elif(args.algorithm == "bubble" and args.comparison == "chunked"):
        server = fhe.Server.load("circuits/server_bubble_sort_chunked.zip")  
    elif(args.algorithm == "insertion" and args.comparison == "OTLU"):
        server = fhe.Server.load("circuits/server_insertion_sort_OTLU.zip")
    elif(args.algorithm == "insertion" and args.comparison == "chunked"):
        server = fhe.Server.load("circuits/server_insertion_sort_chunked.zip")
    elif(args.algorithm == "topk" and args.comparison == "OTLU"):
        server = fhe.Server.load("circuits/server_topk_sort_OTLU.zip")    
    elif(args.algorithm == "topk" and args.comparison == "chunked"):
        server = fhe.Server.load("circuits/server_topk_sort_chunked.zip")
    else :
        print("Invalid algorithm or comparison strategy")
        exit()
    print("Welcome to the server side of the fhe-sorting project 🚀")
    app.run(args.host, args.port)