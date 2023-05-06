import tkinter
import customtkinter as ctk
from tkinter import filedialog, ttk
import os
import nibabel as nib
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Algorithms.thresholding import thresholding_form
from Algorithms.k_means import k_form
from Algorithms.region_growing import region_form
from Classes.SlidePanel import SlidePanel


#FUNCTIONS
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
      selected_file_label.configure(text=file_path)
      path_list.append(file_path)
      #Updates the values in the Combo box
      paths_combobox.configure(values=path_list)

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
            slider = ctk.CTkSlider(img_option_frame, from_=0, to=image.shape[0]-1)
        elif (axis == "y"):
            slider = ctk.CTkSlider(img_option_frame, from_=0, to=image.shape[1]-1)
        elif (axis == "z"):
            slider = ctk.CTkSlider(img_option_frame, from_=0, to=image.shape[2]-1)
        slider.place(relx=0.5, y=100, anchor="c")

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

        slider_value_entry = ctk.CTkEntry(img_option_frame, validate="key")
        slider_value_entry.configure(validatecommand=(window.register(on_validate_int), '%P'))
        slider_value_entry.place(relx=0.49, y=140, anchor="e")
        set_value_button = ctk.CTkButton(img_option_frame, text="Go", command=set_slider_value)
        set_value_button.place(relx=0.51, y=140, anchor="w")

        def update_image(*args):
            global axis_value
            if (axis == "x"):
                x = int(slider.get())
                axis_value = x
                ax.imshow(image [x,:,:])
                canvas_widget.draw()
            elif (axis == "y"):
                y = int(slider.get())
                axis_value = y
                ax.imshow(image [:,y,:])
                canvas_widget.draw()
            elif (axis == "z"):
                z = int(slider.get())
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
    window.quit()

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()
window = ctk.CTk()
window.title("Image Procesing App")

screen_width = 1920
screen_height = 1080
#Set window dimensions
window_width = int(screen_width * 0.7)
window_height = int(screen_height*0.6)
#Position
x = int(screen_width*0.2)
y = int(screen_height*0.2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Variable to store the selected option of the radio buttons
option = ctk.StringVar(value="original")

#Frames
welcome_frame = ctk.CTkFrame(master=window, width=window_width/2,height=110 )
img_option_frame = ctk.CTkFrame(master=window, width= window_width/3, height=210)
radiobutton_frame = ctk.CTkFrame(master=window, width= window_width/4, height=250)

#Labels
welcome_label = ctk.CTkLabel(welcome_frame, text="Welcome to this image processing App", text_color="blue", font=("Times New Roman", 25, "bold"))
selected_file_label = ctk.CTkLabel(welcome_frame, text="")
files_label = ctk.CTkLabel(img_option_frame, text="Files Loaded: ", font=("Times New Roman", 20, "bold"))
axis_label = ctk.CTkLabel(img_option_frame, text="Axis: ", font=("Times New Roman", 20, "bold"))
segmentation_label = ctk.CTkLabel(master=radiobutton_frame, text="Choose your segmentation method: ", font=("Times New Roman", 16, "bold"))

#animated widget
sidebar = SlidePanel(window, 0,-0.2)

#Load Image for button
sidebar_img = ctk.CTkImage(light_image=Image.open("Image/sidebar.png"),dark_image=Image.open("Image/sidebar.png"),size=(50,50))

#Buttons
browse_button = ctk.CTkButton(welcome_frame, text="Browse Image", fg_color="red", width=40, height=28, command=browse_file)
show_img_button = ctk.CTkButton(img_option_frame, text="Show Image", width=40 ,command= display_image)
apply_button = ctk.CTkButton(master=radiobutton_frame, text="Apply Method", width=40,command = option_clicked)
sidebar_button = ctk.CTkButton(window, width=50,text="", image=sidebar_img, command=sidebar.animate, fg_color="transparent", hover_color="lightgray", anchor="w")

#Radio Buttons

thresholding_button = ctk.CTkRadioButton(master=radiobutton_frame, text="Thresholding", variable = option, value="thresholding")
thresholding_button.configure(font=("Times New Roman", 16))
reg_growing_button = ctk.CTkRadioButton(master=radiobutton_frame, text="Region Growing", variable = option, value="region growing")
reg_growing_button.configure(font=("Times New Roman", 16))
k_means_button = ctk.CTkRadioButton(master=radiobutton_frame, text="K-means", variable = option, value="k-means")
k_means_button.configure(font=("Times New Roman", 16))

#Canvas
canvas = tkinter.Canvas(window, width=window_width/4, height=window_height/4)

#Combo Box
path_list = []
paths_combobox = ctk.CTkComboBox(img_option_frame, width=200, height=5, state="readonly")
axis_list = ["x","y","z"]
axis_combobox = ctk.CTkComboBox(img_option_frame, width=200, height=5, values=axis_list, state="readonly")

#Pack
sidebar_button.place(relx=0,rely=0, anchor="nw")
#Welcome Frame
welcome_frame.place(relx=0.5, rely=0.01, anchor="n")
welcome_label.place(relx=0.5 , y=5,  anchor="n")
browse_button.place(relx=0.5, y= 50, anchor = "n")
selected_file_label.place(relx=0.5, y=75,  anchor="n")
#Canvas
canvas.place(relx=0.5, rely=0.2, anchor="nw")
#File Selector Frame
img_option_frame.place(relx=0.25, rely=0.2, anchor="n")
files_label.place(relx=0.05, y=20, anchor="w")
paths_combobox.place(relx=0.35, y=20, anchor="w")
axis_label.place(relx=0.05, y=50, anchor="w")
axis_combobox.place(relx=0.35, y=50, anchor="w")
show_img_button.place(relx=0.5, y = 180, anchor="c")
#Processing Methods Frame
radiobutton_frame.place(relx=0.25, rely=0.75, anchor="c")
segmentation_label.place(x=10, y= 20, anchor="w")
thresholding_button.place(x=10, y=60, anchor="w")
reg_growing_button.place(x=10, y=100, anchor="w")
k_means_button.place(x=10, y=140, anchor="w")
apply_button.place(x=160, y = 200, anchor="n")

window.mainloop()
