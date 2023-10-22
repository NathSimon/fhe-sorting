from concrete import fhe
import numpy as np
import requests
import time

server_url = "http://localhost:8080"

def get_specs():
    url = server_url + "/getsepcs"
    
    response = requests.get(url)
    serialized_client_specs: str = response.content
    
    client_specs = fhe.ClientSpecs.deserialize(serialized_client_specs)
    
    if response.status_code == 200:
        return client_specs

def send_keys(keys):
    url = server_url + "/postkeys"   
    serialized_evaluation_keys:bytes = client.evaluation_keys.serialize()
    
    response = requests.post(url, serialized_evaluation_keys)
    
    if response.status_code == 200:
        print("Success sending keys")
        return
    else:
        print(f"Error sending keys: {response.status_code}")
        return

def encrypt_file():
    with open("unsorted_numbers.txt", "r") as file:
        data = file.read()
        inputset = [int(x) for x in data.split("\n") if x != ""]
    
    print(f"Encrypting {len(inputset)} elements...")
    enc_data: fhe.Value = client.encrypt(inputset)
    
    serialized_arg = enc_data.serialize()

    with open('enc_input.bin', 'wb') as file:
        file.write(serialized_arg)   

def updload_encrypted_file():
    url = server_url + "/upload"
    files = {'file': open('enc_input.bin', 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("Success uploading encrypted file")
    else:
        print(f"Error uploading encrypted file: {response.status_code}")
    
    print(response.text)
    return

def process_result():
    url = server_url + "/process"
    
    serialized_evaluation_keys:bytes = client.evaluation_keys.serialize()
    
    start_time = time.time()
    print("Processing encrypted computation...")
    response = requests.post(url, serialized_evaluation_keys)
    end_time = time.time()
    print(f"Computation finished. FHE processing time: {end_time - start_time} seconds")
    
    if response.status_code == 200:
        print("Success processing encrypted computation")
        return
    else:
        print(f"Error processing encrypted computation: {response.status_code}")
        return


def fetch_results():
    file_url = server_url + "/download/enc_result.bin"
    destination_file_path = "downloaded_enc_result.bin"
    
    try:
        response = requests.get(file_url)
        # Check if the request was successful
        if response.status_code == 200:
            # Save the downloaded content to the local file
            with open(destination_file_path, 'wb') as file:
                file.write(response.content)
                print(f"File downloaded and saved as {destination_file_path}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_sorted(arr):
    if len(arr) <= 1:
        return True
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def get_infos():
    url = server_url + "/infos"
    response = requests.get(url)
    if response.status_code == 200:
        print("Server is running")
        return True
    return False

def verify_results():
    file_path = "downloaded_enc_result.bin"
    with open(file_path, "rb") as file:
        data = file.read()
    
    result = client.decrypt(fhe.Value.deserialize(data))
    print(result)
    if is_sorted(result):
        print("The array is sorted")
    else:
        print("The array is not sorted")
    
if __name__ == "__main__":
    if(not get_infos()):
        exit()
    client = fhe.Client(get_specs())
    client.keys.generate()
    encrypt_file()
    send_keys(client.keys)
    updload_encrypted_file()
    process_result()
    fetch_results()
    verify_results()
