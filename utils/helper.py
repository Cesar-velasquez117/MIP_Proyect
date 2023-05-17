import customtkinter as ctk
import numpy as np
from tkinter import filedialog
from PIL import Image
from Classes.SlidePanel import SlidePanel
from Preprocessing.methods import rescaling, zscore, white_stripe, mean_filter, median_filter, edge_filter, hist_matching
from Algorithms.methods import k_form, region_form, thresholding_form

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
    file_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
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

def option_clicked(image, option, axis, axis_value):
    selected_option = option.get()
    if selected_option == "thresholding":
        thresholding_form(image, axis, axis_value)
    
    if selected_option == "region growing":
        region_form(image, axis, axis_value)

    if selected_option == "k-means":
        k_form(image, axis, axis_value)

#Function to show the histogram with the selected standarization method
def method_clicked(option,canva):
    selected_option = option.get()
    if selected_option == "rescaling":
        rescaling(canva)
    if selected_option == "z-score":
        zscore(canva)
    if selected_option == "white-stripe":
        white_stripe(canva)
    if selected_option == "histogram-matching":
        hist_matching(canva)
    
def denoise_clicked(option, combobox2,canva,window):
    selected_option = option.get()
    axis = combobox2.get()
    if selected_option == "mean-filter":
        mean_filter(canva,axis,window)
    if selected_option == "median-filter":
        median_filter(canva, axis, window)
    if selected_option == "edge-filter":
        edge_filter(canva, axis, window)

def borders(image):
    dfdx = np.zeros_like(image)
    dfdy = np.zeros_like(image)
    dfdz = np.zeros_like(image)
    for x in range(1, image.shape[0]-2) :
        for y in range(1, image.shape[1]-2) :
            for z in range(1, image.shape[2]-2) :
                dfdx[x, y, z] = image[x+1, y, z]-image[x-1, y, z]
                dfdy[x, y, z] = image[x, y+1, z]-image[x, y-1, z]
                dfdz[x, y, z] = image[x, y, z+1]-image[x, y, z-1]
    
    magnitud = np.sqrt(np.power(dfdx, 2) + np.power(dfdy, 2) + np.power(dfdz, 2))
    return magnitud
