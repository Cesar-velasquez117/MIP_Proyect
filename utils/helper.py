import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from Classes.SlidePanel import SlidePanel

#Function to add the sidebar to the window
def add_sidebar(window, window2):
    sidebar = SlidePanel(window, 0, -0.2)
    if window.title() == "Prepocessing": 
        preprocess_button =  ctk.CTkButton(sidebar, text="Preprocessing Methods", width=140, height=30, command=lambda: show_window(window2,window), state="disabled")
        processing_button = ctk.CTkButton(sidebar, text="Processing Methods", width=140, height=30, command=lambda: processing(window2, window))
    else:
        preprocess_button =  ctk.CTkButton(sidebar, text="Go to Preprocessing", width=140, height=30, command=lambda: show_window(window,window2))
        processing_button = ctk.CTkButton(sidebar, text="Processing Methods", width=140, height=30, command=lambda: processing(window, window2), state="disabled")
    sidebar_img = ctk.CTkImage(light_image=Image.open("Image/sidebar.png"),dark_image=Image.open("Image/sidebar.png"),size=(50,50))
    sidebar_button = ctk.CTkButton(window, width=50,text="", image=sidebar_img, command=sidebar.animate, fg_color="transparent", hover_color="lightgray", anchor="w")
    #Sidebar elements
    sidebar_button.place(relx=0,rely=0, anchor="nw")
    processing_button.place(relx=0.5, rely=0.1, anchor="c")
    preprocess_button.place(relx=0.5, rely=0.2, anchor="c")

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
#Function to validate if the digit typed is an integer
def on_validate_int(new_value):
    if new_value.strip() == "":
        return True
    return is_int(new_value)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#Function to validate if the digit typed is a float
def on_validate_float(new_value):
    if new_value.strip() == "":
        return True
    return is_float(new_value)

#Function to browse the image_file
def browse_file(label, list, combobox, combobox2):
    file_path = filedialog.askopenfilename()
    if file_path:
      if file_path not in list:
          label.configure(text=file_path)
          list.append(file_path)
          #Updates the values in the Combo box
          combobox.configure(values=list)
          combobox2.configure(values=list)
      else:
          label.configure(text="This file was already uploaded")

#Function to go back to the Preprocessing window
def show_window(window,window2):
    window.withdraw()
    window2.deiconify()
#Function to go to the Processing window
def processing(window, window2):
    window2.withdraw()
    window.deiconify()
#Function to close the app
def on_closing(window):
    window.destroy()
    window.quit()
