import tkinter as tk
import paho.mqtt.client as mqtt
import json
import time

deviceNumber = 1 #rpi01
broker = "172.26.188.16" # main device ip
port = 1883 # should figure out why this is this
topic_send = "mainDevice/send" # single topic used to send to main device
topic_receive = "mainDevice/receive" # single topic that all rpi0s are subscribed to


class ScrabbleApp:
    def __init__(self, root):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # self.client.connect(broker,port,keepalive=60)
        self.client.loop_start()
        
        #Timing variables used for testing
        self.start_time = 0
        self.end_time = 0

        self.scores = [0,0,0,0]
        self.turns = 1
        self.score_labels = []

        self.root = root
        self.root.title("Scrabbletron")
        self.root.geometry("800x600") 
        self.root.minsize(600, 400)  
        self.main_frame = tk.Frame(self.root)
        self.results_frame = tk.Frame(self.root)
        self.invalid_frame = tk.Frame(self.root)
        self.submit_frame = tk.Frame(self.root)
        self.check_frame = tk.Frame(self.root)
        for frame in (self.main_frame, self.results_frame,self.invalid_frame,self.submit_frame,self.check_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.setup_main_page()
        self.setup_results_page()
        self.main_frame.tkraise()

    
    def on_connect(self,client,userdata,flags,rc):
        if rc == 0:
            self.client.subscribe(topic_receive)
    
    def on_message(self,client,userdata,msg):
        result = json.loads(msg.payload.decode())
        print(f"Received from mainDevice: {result}")
        if result[2] == 2:
            self.scores = result[3]
            self.turns = result[4]
            self.update_scores()
        elif result[1] == deviceNumber:
            #Valid hint request returned
            if result[2] == 1:
                self.root.after(0,self.show_hints,result[3])
            #Valid check request returned
            elif result[2] == 4:
                self.root.after(0,self.show_check,result[3])
            #Valid submit request returned
            elif result[2] == 6:
                self.root.after(0,self.show_submit,result[3])
            elif result[2] ==7:
                self.root.after(0,self.show_invalid_request)

    def setup_main_page(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.tile_display = tk.Entry(self.main_frame, font=("Helvetica", 14), justify="center")
        self.tile_display.grid(row=2, column=0, padx=10, pady=2, sticky="ew")
        self.create_keyboard()

        # write fn to display scores

        score_frame = tk.Frame(self.main_frame)
        score_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        score_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        for i in range(4):
            if i+1 == self.turns:
                label = tk.Label(score_frame, text=f"Player {i+1}: {self.scores[i]}", font=("Helvetica", 14,"bold"))
            else:
                label = tk.Label(score_frame, text=f"Player {i+1}: {self.scores[i]}", font=("Helvetica", 14))
            label.grid(row=0, column=i, padx=5)
            self.score_labels.append(label)
    

        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.check_button = tk.Button(button_frame, text="Check", command=self.check_board, font=("Helvetica", 14))
        self.check_button.grid(row=0, column=0, padx=5, sticky="ew")
        self.submit_button = tk.Button(button_frame, text="Submit", command=self.submit_word, font=("Helvetica", 14))
        self.submit_button.grid(row=0, column=1, padx=5, sticky="ew")
        self.hint_button = tk.Button(button_frame, text="Hint", command=self.send_hints, font=("Helvetica", 14))
        self.hint_button.grid(row=0, column=2, padx=5, sticky="ew")

    def setup_results_page(self):
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.hint_text = tk.Text(self.results_frame, font=("Helvetica", 14), wrap="word")
        self.hint_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.back_button = tk.Button(self.results_frame, text="Back", command=self.go_to_main_page, font=("Helvetica", 14))
        self.back_button.grid(row=1, column=0, pady=10, sticky="ew")

    def create_keyboard(self):
        keyboard_frame = tk.Frame(self.main_frame)
        keyboard_frame.grid(row=1, column=0, pady=5, sticky="nsew")
        keyboard_frame.grid_columnconfigure(0, weight=1)
        keyboard_layout = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        for i, row in enumerate(keyboard_layout):
            row_frame = tk.Frame(keyboard_frame)
            row_frame.pack(anchor="center")
            for char in row:
                button = tk.Button(row_frame, text=char, font=("Helvetica", 14),
                                   command=lambda c=char: self.add_letter(c), width=3, height=1)
                button.pack(side="left", padx=5)
        delete_button_frame = tk.Frame(keyboard_frame)
        delete_button_frame.pack(anchor="center", pady=5)
        delete_button = tk.Button(delete_button_frame, text="Delete", font=("Helvetica", 14), command=self.delete_last_letter, width=6, height=1)
        delete_button.pack(side="left", padx=5)
    
    def delete_last_letter(self):
        current_text = self.tile_display.get()
        if current_text: 
            self.tile_display.delete(0, tk.END)
            self.tile_display.insert(0, current_text[:-1])

    def add_letter(self, char):
        current_text = self.tile_display.get()
        self.tile_display.delete(0, tk.END)
        self.tile_display.insert(0, current_text + char)

    def check_board(self):
        self.check_button.config(state="disabled")
        self.root.after(5000, lambda: self.check_button.config(state="normal"))
        letters = self.tile_display.get().strip().lower()
        self.tile_display.delete(0, tk.END)
        rack = list(letters)
        if len(rack) == 0:
            msg_to_send = [deviceNumber,0,3,' ']
        else:
            msg_to_send = [deviceNumber,0,3,rack[0]]
        print(f"Sending {msg_to_send}")
        self.client.publish(topic_send,json.dumps(msg_to_send))

    def submit_word(self):
        msg_to_send = [deviceNumber,0,5,0]
        print(f"Sending {msg_to_send}")
        self.client.publish(topic_send,json.dumps(msg_to_send))

    def send_hints(self):
        self.start_time = time.time()
        self.hint_text.delete("1.0", tk.END)
        letters = self.tile_display.get().strip().lower()
        self.tile_display.delete(0, tk.END)
        rack = list(letters)
        number = [deviceNumber,0,0] + rack
        print(f"Sending {number}")
        self.client.publish(topic_send,json.dumps(number))

    def show_check(self,valid):
        self.check_frame.grid_columnconfigure(0, weight=1)
        self.check_frame.grid_rowconfigure(0, weight=1)
        self.check_text = tk.Text(self.check_frame, font=("Helvetica", 28), wrap="word")
        self.check_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        if valid[0]:
            self.check_text.insert('1.0',f"Detected word {valid[4]} is Valid and has score {valid[1]}")
        else:
            self.check_text.insert('1.0',f"The detected word {valid[4]} is Invalid")
        self.back_button = tk.Button(self.check_frame, text="Back", command=self.go_to_main_page, font=("Helvetica", 14))
        self.back_button.grid(row=1, column=0, pady=10, sticky="ew")
        self.check_frame.tkraise()
        
    
    def show_submit(self,valid):
        self.submit_frame.grid_columnconfigure(0, weight=1)
        self.submit_frame.grid_rowconfigure(0, weight=1)
        self.submit_text = tk.Text(self.submit_frame, font=("Helvetica", 28), wrap="word")
        self.submit_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        if valid[0]:
            self.submit_text.insert('1.0',"Detected word is Valid and was Submitted")
        else:
            self.submit_text.insert('1.0',"The detected word is Invalid, and was not Submitted")
        self.back_button = tk.Button(self.submit_frame, text="Back", command=self.go_to_main_page, font=("Helvetica", 14))
        self.back_button.grid(row=1, column=0, pady=10, sticky="ew")
        self.submit_frame.tkraise()

    def show_invalid_request(self):
        self.invalid_frame.grid_columnconfigure(0, weight=1)
        self.invalid_frame.grid_rowconfigure(0, weight=1)
        self.invalid_text = tk.Text(self.invalid_frame, font=("Helvetica", 28), wrap="word")
        self.invalid_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.invalid_text.insert(tk.END,"It is not your turn, please wait for your turn!")
        self.back_button = tk.Button(self.invalid_frame, text="Back", command=self.go_to_main_page, font=("Helvetica", 14))
        self.back_button.grid(row=1, column=0, pady=10, sticky="ew")
        self.invalid_frame.tkraise()

    def show_hints(self,hints):
        self.hint_text.tag_configure("bold", font=("Helvetica", 20, "bold"))
        if hints:
            for word, result in hints.items():
                self.hint_text.insert(tk.END, "word: ")
                self.hint_text.insert(tk.END, f"{word}, ", "bold")
                self.hint_text.insert(tk.END, "score: ")
                self.hint_text.insert(tk.END, f"{result[0]}, ", "bold")
                self.hint_text.insert(tk.END, "start: ")
                self.hint_text.insert(tk.END, f"{result[1]}, ", "bold")
                self.hint_text.insert(tk.END, "end: ")
                self.hint_text.insert(tk.END, f"{result[2]}\n", "bold")
        else:
            self.hint_text.insert(tk.END, "No possible words found.")
        self.end_time = time.time()
        print(f"Hint gen took {self.end_time - self.start_time} to process")
        self.results_frame.tkraise()
    
    def update_scores(self):
        for i, label in enumerate(self.score_labels):
            if i+1 == self.turns:
                label.config(text=f"Player {i+1}: {self.scores[i]}", font=("Helvetica", 14,"bold"))
            else:
                label.config(text=f"Player {i+1}: {self.scores[i]}", font=("Helvetica", 14))
            
        

    def go_to_main_page(self):
        self.main_frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrabbleApp(root)
    root.mainloop()
