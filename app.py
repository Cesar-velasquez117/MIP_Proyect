import tkinter
from tkinter import filedialog, ttk
import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Algorithms.thresholding import thresholding_form
from Algorithms.k_means import k_form
from Algorithms.region_growing import region_form

#FUNCTIONS
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
      selected_file_label.config(text=file_path)
      path_list.append(file_path)
      #Updates the values in the Combo box
      paths_combobox.config(values=path_list)

canvas_widget = None
axis = ""
axis_value = 0

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def on_validate_int(new_value):
    if new_value.strip() == "":
        return True
    return is_int(new_value)


def display_image():
    global canvas_widget
    file_path = paths_combobox.get()
    if file_path:
        image_data=nib.load(file_path)
        image = image_data.get_fdata()
        canvas.delete("all")
        filename = os.path.basename(file_path)

        #Slider 
        global axis
        axis = axis_combobox.get()
        if (axis == "x"):
            slider = tkinter.Scale(window, from_=0, to=image.shape[0]-1, orient=tkinter.HORIZONTAL)
        elif (axis == "y"):
            slider = tkinter.Scale(window, from_=0, to=image.shape[1]-1, orient=tkinter.HORIZONTAL)
        elif (axis == "z"):
            slider = tkinter.Scale(window, from_=0, to=image.shape[2]-1, orient=tkinter.HORIZONTAL)
        slider.place(x=10, y=185, anchor="w")

        #Slider Entry
        def set_slider_value():
            value = int(slider_value_entry.get())
            if axis == "x":
                if value < 0:
                    value = 0
                elif value >= image.shape[0]:
                    value = image.shape[0] - 1
            elif axis == "y":
                if value < 0:
                    value = 0
                elif value >= image.shape[1]:
                    value = image.shape[1] - 1
            elif axis == "z":
                if value < 0:
                    value = 0
                elif value >= image.shape[2]:
                    value = image.shape[2] - 1
            slider.set(value)
            update_image()

        slider_value_entry = tkinter.Entry(window, validate="key")
        slider_value_entry.configure(validatecommand=(window.register(on_validate_int), '%P'))
        slider_value_entry.place(x=150, y=192.5, anchor="w")
        set_value_button = tkinter.Button(window, text="Go", command=set_slider_value)
        set_value_button.place(x=280, y=192.5, anchor="w")

        def update_image(*args):
            global axis_value
            if (axis == "x"):
                x = slider.get()
                axis_value = x
                ax.imshow(image [x,:,:])
                canvas_widget.draw()
            elif (axis == "y"):
                y = slider.get()
                axis_value = y
                ax.imshow(image [:,y,:])
                canvas_widget.draw()
            elif (axis == "z"):
                z = slider.get()
                axis_value = z
                ax.imshow(image [:,:,z])
                canvas_widget.draw()
        
        slider.bind("<B1-Motion>", update_image)

        fig, ax= plt.subplots()
        if (axis == "x"):
            ax.imshow(image[0,:,:])
        elif (axis == "y"):
            ax.imshow(image[:,0,:])
        elif (axis == "z"):
            ax.imshow(image[:,:,0])
        

        if canvas_widget is None:
            canvas_widget = FigureCanvasTkAgg(fig,canvas)
            canvas_widget.get_tk_widget().pack()
        else:    
            canvas_widget.figure = fig
            canvas_widget.draw()


def option_clicked():
    selected_option = option.get()
    file_path = paths_combobox.get()
    if selected_option == "thresholding":
        thresholding_form(file_path, axis, axis_value)
    
    if selected_option == "region growing":
        region_form(file_path)

    if selected_option == "k-means":
        k_form(file_path, axis, axis_value)
    
def on_closing():
    window.destroy()
#GUI

window = tkinter.Tk()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("Image Procesing App")

#Get screen dimensions
screen_width = 1920
screen_height = 1080
print(screen_height, screen_width)
#Set window dimensions
window_width = int(screen_width * 0.7)
window_height = int(screen_height*0.6)
#Position
x = int(screen_width*0.2)
y = int(screen_height*0.2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Variable to store the selected option of the radio buttons
option = tkinter.StringVar(value="original")

#Labels
color_label = tkinter.Label(window, bg="red", height=2, width=window_width)
welcome_label = tkinter.Label(window, text="Welcome to this image processing App", font=("Times New Roman", 17, "bold"))
selected_file_label = tkinter.Label(window)
files_label = tkinter.Label(window, text="Files Loaded: ", font=("Times New Roman", 15, "bold"))
axis_label = tkinter.Label(window, text="Axis: ", font=("Times New Roman", 15, "bold"))
segmentation_label = tkinter.Label(window, text="Choose your segmentation method: ", font=("Times New Roman", 16, "bold"))

#Buttons
browse_button = tkinter.Button(window, text="Browse", width=10, height=1, command=browse_file)
show_img_button = tkinter.Button(window, text="Show Image", width=40 ,command= display_image)
apply_button = tkinter.Button(window, text="Apply", width=40, height=2,command = option_clicked)

#Radio Buttons
thresholding_button = tkinter.Radiobutton(window, text="Thresholding", variable = option, value="thresholding")
thresholding_button.config(font=("Times New Roman", 16), padx=10, pady=10)
reg_growing_button = tkinter.Radiobutton(window, text="Region Growing", variable = option, value="region growing")
reg_growing_button.config(font=("Times New Roman", 16), padx=10, pady=10)
k_means_button = tkinter.Radiobutton(window, text="K-means", variable = option, value="k-means")
k_means_button.config(font=("Times New Roman", 16), padx=10, pady=10)

#Canvas
canvas = tkinter.Canvas(window, width=window_width/4, height=window_height/4)

#Combo Box
path_list = []
paths_combobox = ttk.Combobox(window, width=30, height=3)
axis_list = ["x","y","z"]
axis_combobox = ttk.Combobox(window, width=30, height=3, values=axis_list)


#Pack
color_label.place(x=window_width/2 , y=0,  anchor="n")
welcome_label.place(x=window_width/2 , y=10,  anchor="n")
browse_button.place(x=window_width/2, y= 60, anchor="n")
selected_file_label.place(x=window_width/2, y = 90, anchor="n")
canvas.place(x=window_width/2, y=120, anchor="nw")
files_label.place(x=10, y=128, anchor="w")
paths_combobox.place(x=240, y=120, anchor="n")
axis_label.place(x=10, y=158, anchor="w")
axis_combobox.place(x=240, y=150, anchor="n")
show_img_button.place(x=180, y = 220, anchor="n")
segmentation_label.place(x=10, y= 270, anchor="w")
thresholding_button.place(x=10, y=330, anchor="w" )
reg_growing_button.place(x=10, y=370, anchor="w")
k_means_button.place(x=10, y=410, anchor="w")
apply_button.place(x=180, y = 580, anchor="n")

window.mainloop()