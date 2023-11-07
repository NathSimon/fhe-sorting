
from concrete import fhe
import numpy as np
import requests
import time
import json

server_url = None  
client = None

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

def encrypt_file(file_path):
    with open(file_path, "r") as file:
        data = file.read()
        inputset = [int(x) for x in data.split("\n") if x != ""]
    
    inputset = np.array(inputset)
    
    
    print(f"Unsorted values: {inputset}")
    
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
        return end_time - start_time
    else:
        print(f"Error processing encrypted computation: {response.status_code}")
        return end_time - start_time

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
    
    return result
    
def setServerCircuit(algorithm, comparison):
    url = server_url + "/setcircuit"
    data = {
        "algorithm": algorithm,
        "comparison": comparison
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("Server Circuit set to " +  algorithm + " sort algorithm with " + comparison + " comparison strategie")
        return True
    else:
        print(f"Error setting circuit to " + algorithm + " sort algorithm with " + comparison+ " comparison strategie :" + f"{response.status_code}")
        return False


def run_sorting_process(file_path):
    global client
    client = fhe.Client(get_specs())
    client.keys.generate()
    encrypt_file("unsorted_numbers.txt")
    send_keys(client.keys)
    updload_encrypted_file()
    process_result()
    fetch_results()
    verify_results()

def set_server_url(url):
    global server_url
    server_url = url



def setClient():
    global client
    client = fhe.Client(get_specs())
    client.keys.generate()



##############

import customtkinter
import os
import joblib
import pandas as pd
import numpy as np
import pickle
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import time
home_text = "FHE sorting GUI Client pour l'UE SR2I309"

algorithm = "bubble"
mode = "chunked"
file_path = ""
waiting_label = ""
input_label = ""

from PIL import ImageTk
from PIL import Image

class ToplevelWindowSuspect(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("suspicious anomalies detected")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create home frame
        self.info_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)#

        self.textbox = customtkinter.CTkTextbox(self.info_frame)
        self.textbox.grid(row=0, column=0, padx=(30, 30), pady=(30, 30), sticky="nsew")
        self.textbox.insert("0.0", predict_text_suspect)
        self.textbox.configure(state="disabled")

        self.info_frame.grid(row=0, column=0, sticky="nsew")

        #self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        #self.label.pack(padx=20, pady=20)

        

        #self.focus()

        """
        self.textbox_predict = customtkinter.CTkTextbox(self)
        self.textbox_predict.configure(state="disabled")
        self.textbox_predict.pack(padx=20, pady=20, fill="both", expand=True)  # Fill the entire frame
        self.textbox_predict.insert("0.0", home_text)
        """


    def set_text(self, text):
        
        self.textbox_predict.delete("0.0", "end")  # Clear existing text
        self.textbox_predict.insert("0.0", text)  # Insert new text
        
        return


class ToplevelWindowDanger(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x600")
        self.title("dangerous anomalies detected")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create home frame
        self.info_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)#

        self.textbox = customtkinter.CTkTextbox(self.info_frame)
        self.textbox.grid(row=0, column=0, padx=(30, 30), pady=(30, 30), sticky="nsew")
        self.textbox.insert("0.0", predict_text_danger)
        self.textbox.configure(state="disabled")

        self.info_frame.grid(row=0, column=0, sticky="nsew")

        #self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        #self.label.pack(padx=20, pady=20)

        

        #self.focus()

        """
        self.textbox_predict = customtkinter.CTkTextbox(self)
        self.textbox_predict.configure(state="disabled")
        self.textbox_predict.pack(padx=20, pady=20, fill="both", expand=True)  # Fill the entire frame
        self.textbox_predict.insert("0.0", home_text)
        """


    def set_text(self, text):
        
        self.textbox_predict.delete("0.0", "end")  # Clear existing text
        self.textbox_predict.insert("0.0", text)  # Insert new text
        
        return

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.toplevel_window_suspect = None
        self.toplevel_window_danger = None
        self.change_appearance_mode_event("Dark")
        self.file_loaded = 0
        self.file_training_loaded = 0
        self.title("FHE sorting")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_image.png")), size=(56, 56))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bug_dark.png")), size=(20, 20))
        
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "info_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "info_white.png")), size=(20, 20))
        self.circuit = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "circuit_image.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "circuit_image.png")), size=(20, 20))
        
        self.chiffrement = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chiffrement_image.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "chiffrement_image.png")), size=(20, 20))

        self.serveur = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "server-solid.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "server-solid.png")), size=(20, 20))
        
        ###################
        self.calcul = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calcul_image.png")),
                                             dark_image = Image.open(os.path.join(image_path, "calcul_image.png")), size=(20, 20))
        
        #same but for clear
        self.clear = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "clear_image.png")),
                                             dark_image = Image.open(os.path.join(image_path, "clear_image.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(9, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  FHE sorting",#image
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Informations",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_1_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Choix du serveur",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.frame_1_button_event)
        self.frame_1_button.grid(row=2, column=0, sticky="ew")
        
        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Choix du circuit",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=3, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Chiffrement",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=4, column=0, sticky="ew")
        
        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Process",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=5, column=0, sticky="ew")
        
        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Resultats",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=6, column=0, sticky="ew")
        
        """
        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="step_6",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.serveur, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=7, column=0, sticky="ew")
        
        self.frame_7_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="step_7",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.serveur, anchor="w", command=self.frame_7_button_event)
        self.frame_7_button.grid(row=8, column=0, sticky="ew")
        """
        
        
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=9, column=0, padx=20, pady=20, sticky="s")

        #créer la 4ème frame
        self.step_4_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.step_4_frame.grid_columnconfigure(0, weight=1)
        self.step_4_frame.grid_rowconfigure(3, weight=1)
        self.step_4_frame.grid_rowconfigure(4, weight=1)
        self.step_4_frame.grid_rowconfigure(5, weight=1)
        
        self.step_4_frame_process = customtkinter.CTkButton(self.step_4_frame, 
                                                            text="process",
                                                           command=self.step_4_process_function)
        self.step_4_frame_process.grid(row=3, column=0, padx=20, pady=10)
        
        #image
        #self.step_4_frame_progressbar = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "bug_colored.png")),
        #                                             dark_image=Image.open(os.path.join(image_path, "bug_colored.png")), size=(20, 20))
        
        self.step_4_frame_loading_label = customtkinter.CTkLabel(self.step_4_frame, text=waiting_label, width=20, height=2, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.step_4_frame_loading_label.grid(row=4, column=0, padx=20, pady=10)
        #self.step_4_frame_progressbar_button.grid(row=4, column=0, padx=20, pady=10)
        
        #créer la 5ème frame
        self.step_5_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.step_5_frame.grid_columnconfigure(0, weight=1)
        self.step_5_frame.grid_rowconfigure(3, weight=1)
        
        self.step_5_frame_clear = customtkinter.CTkButton(self.step_5_frame, 
                                                            text="clear",
                                                           command=self.step_5_clear_function)
        self.step_5_frame_clear.grid(row=3, column=0, padx=20, pady=10)
        
        #label
        self.step_5_frame_label = customtkinter.CTkLabel(self.step_5_frame, text="", width=20, height=2, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.step_5_frame_label.grid(row=4, column=0, padx=20, pady=10)
        
        #créer la 6ème frame
        self.step_6_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.step_6_frame.grid_columnconfigure(0, weight=1)
        self.step_6_frame.grid_rowconfigure(0, weight=1)


        # create home frame
        self.info_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)#

        self.textbox = customtkinter.CTkTextbox(self.info_frame)
        self.textbox.grid(row=0, column=0, padx=(30, 30), pady=(30, 30), sticky="nsew")
        self.textbox.insert("0.0", home_text)
        self.textbox.configure(state="disabled")

        # create step_1 frame
        self.step_1_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.step_1_frame.grid_columnconfigure(0, weight=1)
        self.step_1_frame.grid_rowconfigure(0, weight=1)
        self.step_1_frame.grid_rowconfigure(1, weight=1)
        
        self.frame_1_ip = customtkinter.CTkEntry(self.step_1_frame, placeholder_text="Server IP")#, placeholder_color="gray50")
        
        self.frame_1_ip.grid(row=0, column=0, padx=20, pady=10)
        
        self.frame_1_chiffrer = customtkinter.CTkButton(self.step_1_frame, 
                                                            text="submit",
                                                           command=self.step_1_function)
        self.frame_1_chiffrer.grid(row=1, column=0, padx=20, pady=10)
        
        """
        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="step_3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chiffrement, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=4, column=0, sticky="ew")
        """

        self.tabview = customtkinter.CTkTabview(master=self.step_6_frame)
        self.tabview.grid(row=0, column=0, padx=(30, 30), pady=(30, 30), sticky="nsew")

        self.tabview.add("RMC")  # add tab at the end
        

        self.tabview.add("SVM")  # add tab at the end

        self.tabview.add("AdaBoost")  # add tab at the end

        self.tabview.add("XGBoost")  # add tab at the end

        self.tabview.add("MLPC")  # add tab at the end

        self.tabview.set("RMC")  # set currently visible tab

        # create third frame
        self.step_2_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.step_2_frame.grid_columnconfigure(0, weight=1)

        #the four next elements have to be dispached verticlayy uniformément
        self.step_2_frame.grid_rowconfigure(0, weight=1)
        self.step_2_frame.grid_rowconfigure(1, weight=1)
        self.step_2_frame.grid_rowconfigure(2, weight=1)
        self.step_2_frame.grid_rowconfigure(3, weight=1)
        self.step_2_frame.grid_rowconfigure(4, weight=1)
        self.step_2_frame.grid_rowconfigure(5, weight=1)
        self.step_2_frame.grid_rowconfigure(6, weight=1)
        self.step_2_frame.grid_rowconfigure(7, weight=1)
        self.step_2_frame.grid_rowconfigure(8, weight=1)
        self.step_2_frame.grid_rowconfigure(9, weight=1)
        self.step_2_frame.grid_rowconfigure(10, weight=1)

        self.step_2_frame_list_1 = customtkinter.CTkOptionMenu(self.step_2_frame, values=["bubble", "insertion", "topk"],
                                                                command=self.step_2_function_algorithm)
        self.step_2_frame_list_1.grid(row=3, column=0, padx=20, pady=10)

        self.step_2_frame_list_2 = customtkinter.CTkOptionMenu(self.step_2_frame, values=["chunked", "OTLU", "TTLU"],
                                                                command=self.step_2_function_mode)
        self.step_2_frame_list_2.grid(row=4, column=0, padx=20, pady=10)
       
        """
        self.step_2_frame_button_2 = customtkinter.CTkButton(self.step_2_frame, 
                                                            text="load inputs",
                                                            command=self.load_file)
        self.step_2_frame_button_2.grid(row=5, column=0, padx=20, pady=10)
        """
        
        self.step_2_frame_button_3 = customtkinter.CTkButton(self.step_2_frame, 
                                                            text="submit",
                                                           command=self.step_2_function)
        self.step_2_frame_button_3.grid(row=9, column=0, padx=20, pady=10)

        self.step_2_frame_button_4 = customtkinter.CTkLabel(self.step_2_frame, text="",
                                                           compound="left", 
                                                           text_color="red", 
                                                           font=customtkinter.CTkFont(size=15, weight="bold"))
        

        
        self.step_2_frame_button_4.grid(row=10, column=0, padx=20, pady=10)

        self.step_2_frame_button_5 = customtkinter.CTkLabel(self.step_2_frame, text="",
                                                           compound="left", 
                                                           text_color="red", 
                                                           font=customtkinter.CTkFont(size=15, weight="bold"))
        self.step_2_frame_button_5.grid(row=11, column=0, padx=20, pady=10)

        #train frame

        # create third frame
        self.step_3_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.step_3_frame.grid_columnconfigure(0, weight=1)
        self.step_3_frame.grid_rowconfigure(3, weight=1)

        #the four next elements have to be dispached verticlayy uniformément
        self.step_3_frame.grid_rowconfigure(0, weight=1)
        self.step_3_frame.grid_rowconfigure(1, weight=1)
        self.step_3_frame.grid_rowconfigure(2, weight=1)
        self.step_3_frame.grid_rowconfigure(3, weight=1)
        self.step_3_frame.grid_rowconfigure(4, weight=1)
        self.step_3_frame.grid_rowconfigure(5, weight=1)
        self.step_3_frame.grid_rowconfigure(6, weight=1)
        self.step_3_frame.grid_rowconfigure(7, weight=1)
        self.step_3_frame.grid_rowconfigure(8, weight=1)
        self.step_3_frame.grid_rowconfigure(9, weight=1)
    
        self.step_3_frame_button_2 = customtkinter.CTkButton(self.step_3_frame, 
                                                            text="load inputs",
                                                            command=self.load_file_inputs)
        self.step_3_frame_button_2.grid(row=2, column=0, padx=20, pady=10)

        """
        self.step_3_frame_list_1 = customtkinter.CTkOptionMenu(self.step_3_frame, values=["bubble", "insertion", "topk"],
                                                                command=self.none)
        self.step_3_frame_list_1.grid(row=3, column=0, padx=20, pady=10)
        """

        self.step_3_frame_button_3 = customtkinter.CTkButton(self.step_3_frame, 
                                                            text="cipher",
                                                           command=self.step_3_cipher_function)
        self.step_3_frame_button_3.grid(row=4, column=0, padx=20, pady=10)
        
        self.step_3_frame_button_4 = customtkinter.CTkButton(self.step_3_frame, 
                                                            text="process",
                                                           command=self.step_3_process_function)
        self.step_3_frame_button_4.grid(row=5, column=0, padx=20, pady=10)
        
        self.step_3_frame_label = customtkinter.CTkLabel(self.step_3_frame, text=input_label, width=20, height=2, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.step_3_frame_label.grid(row=6, column=0, padx=20, pady=10)
        
        
        self.select_frame_by_name("Information")

    def do_something(self):
        self.label.config(text = "Wait till I'm done...")
        self.label.update_idletasks()
        time.sleep(2)
        print ("end sleep")
        self.label.config(text = "I'm done doing...")

    def draw(self):
        image = Image.open("images/bug_colored.png")
        angle = 0
        while True:
            tkimage = ImageTk.PhotoImage(image.rotate(angle))
            canvas_obj = self.canvas.create_image(
                250, 250, image=tkimage)
            self.master.after_idle(self.update)
            yield
            self.canvas.delete(canvas_obj)
            angle += 10
            angle %= 360

    def step_4_process_function(self):
        #sow messagebox
        box = messagebox.showinfo("Processing", "loading")
        delay = process_result()
        fetch_results()
        global waiting_label
        time.sleep(2)
        waiting_label = "done in "+ str(delay) + " seconds"
        self.step_4_frame_loading_label.configure(text=waiting_label)
        self.select_frame_by_name("step_5")
        
        return

    def step_5_clear_function(self):
        clear = verify_results()#message ok saying it's done
        self.step_5_frame_label.configure(text=clear)
        messagebox.showerror("Clear", "Done")
        return

    def step_3_cipher_function(self):
        encrypt_file(file_path)
        send_keys(client.keys)
        updload_encrypted_file()
        return
        
    def step_3_process_function(self):
        #go next step
        self.select_frame_by_name("step_4")
        """
        process_result()
        fetch_results()
        """
        return

    def step_2_function_algorithm(self, new_algorithm):
        global algorithm
        algorithm = new_algorithm
        return
    
    def step_2_function_mode(self, new_mode):
        global mode
        mode = new_mode
        return
    
    def step_2_function(self):
        global algorithm
        global mode        
        setServerCircuit(algorithm, mode)
        setClient()
        self.select_frame_by_name("step_3")

    def step_1_function(self):
        global server_url
        server_url = "http://" + self.frame_1_ip.get()
        
        
        if(not get_infos()):
            messagebox.showerror("Error", "Server not found")
            return
        
        self.select_frame_by_name("step_2")

    def none(self):
        return

    def load_file_inputs(self):
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale de tkinter
        global file_path
        global input_label
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as file:
            data = file.read()
            inputset = [int(x) for x in data.split("\n") if x != ""]
        inputset = np.array(inputset)
        input_label = inputset#.tostring()
        self.step_3_frame_label.configure(text=input_label)
        

    def load_file(self):
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale de tkinter
        file_path = filedialog.askopenfilename()
        self.data = pd.read_csv(file_path, header=None)
        self.file_loaded = 1

     
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Informations" else "transparent")
        self.frame_1_button.configure(fg_color=("gray75", "gray25") if name == "step_1" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "step_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "step_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "step_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "step_5" else "transparent")

        # show selected frame
        if name == "Informations":
            self.info_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.info_frame.grid_forget()
        if name == "step_1":
            self.step_1_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.step_1_frame.grid_forget()
        if name == "step_2":
            self.step_2_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.step_2_frame.grid_forget()
        if name == "step_3":
            self.step_3_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.step_3_frame.grid_forget()
        if name == "step_4":
            self.step_4_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.step_4_frame.grid_forget()
        if name == "step_5":
            self.step_5_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.step_5_frame.grid_forget()
            
            
    def home_button_event(self):
        self.select_frame_by_name("Informations")

    def frame_1_button_event(self):
        self.select_frame_by_name("step_1")

    def frame_2_button_event(self):
        self.select_frame_by_name("step_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("step_3")
    
    def frame_4_button_event(self):
        self.select_frame_by_name("step_4")
    
    def frame_5_button_event(self):
        self.select_frame_by_name("step_5")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

