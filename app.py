import tkinter as tk
import json
import time




class ScrabbleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lily")
        self.root.geometry("800x600") 
        self.root.minsize(600, 400)  
        self.main_frame = tk.Frame(self.root)
        
        self.photo_frame = tk.Frame(self.root)
        
        for frame in (self.main_frame,self.photo_frame):
            frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.setup_main_page()
        # self.setup_results_page()
        self.main_frame.tkraise()

    def setup_main_page(self):
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        button_frame = tk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.check_button = tk.Button(button_frame, text="Couple Slideshow", command=self.display_slideshow, font=("Helvetica", 14))
        self.check_button.grid(row=0, column=0, padx=5, sticky="ew")
        self.submit_button = tk.Button(button_frame, text="Love Letter", command=self.display_loveletter, font=("Helvetica", 14))
        self.submit_button.grid(row=0, column=1, padx=5, sticky="ew")
        self.hint_button = tk.Button(button_frame, text="Rosie :)", command=self.display_rosie, font=("Helvetica", 14))
        self.hint_button.grid(row=0, column=2, padx=5, sticky="ew")

    def display_slideshow(self):
        self.photo_frame.grid_columnconfigure(0,weight=1)
        self.photo = tk.PhotoImage(file='./couple_photos/test_img.jpg')
        self.back_button = tk.Button(self.photo_frame, text="Back", command=self.go_to_main_page, font=("Helvetica", 14))
        self.back_button.grid(row=1, column=0, pady=10, sticky="ew")
        self.photo_frame.tkraise()

        return

    def display_loveletter(self):
        return
    
    def display_rosie(self):
        return

    def setup_results_page(self):
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.hint_text = tk.Text(self.results_frame, font=("Helvetica", 14), wrap="word")
        self.hint_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.back_button = tk.Button(self.results_frame, text="Back", command=self.go_to_main_page, font=("Helvetica", 14))
        self.back_button.grid(row=1, column=0, pady=10, sticky="ew")

    
        
    
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

            
        

    def go_to_main_page(self):
        self.main_frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScrabbleApp(root)
    root.mainloop()
