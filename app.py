import tkinter
import customtkinter as ctk
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.helper import add_sidebar, on_validate_int, browse_file, on_closing, method_clicked, denoise_clicked, option_clicked, borders
from utils.globals import *
from Preprocessing.methods import set_image, get_updated_image, get_updated_ax

#FUNCTIONS

def display_image():
    global canvas_widget, fig, ax, image, ax2, fig2
    image = get_updated_image()
    fig2,ax2 = get_updated_ax()
    if ax2 is not None:
        ax2.clear()

    canvas.delete("all")

    #Slider 
    global axis
    axis = axis_combobox.get()
    if (axis == "x"):
        slider = ctk.CTkSlider(img_option_frame, from_=0, to=image.shape[0]-1)
    elif (axis == "y"):
        slider = ctk.CTkSlider(img_option_frame, from_=0, to=image.shape[1]-1)
    elif (axis == "z"):
        slider = ctk.CTkSlider(img_option_frame, from_=0, to=image.shape[2]-1)
    slider.set(0)
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

    if fig is None:
        fig, ax= plt.subplots()
    else:
        ax.clear()
        
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

def display_borders():
    global canvas_widget, fig, ax, image, ax2, fig2
    image = get_updated_image()
    border = borders(image)
    fig2,ax2 = get_updated_ax()
    if ax2 is not None:
        ax2.clear()

    canvas.delete("all")

    #Slider 
    global axis
    axis = axis_combobox.get()
    if (axis == "x"):
        slider = ctk.CTkSlider(img_option_frame, from_=0, to=border.shape[0]-1)
    elif (axis == "y"):
        slider = ctk.CTkSlider(img_option_frame, from_=0, to=border.shape[1]-1)
    elif (axis == "z"):
        slider = ctk.CTkSlider(img_option_frame, from_=0, to=border.shape[2]-1)
    slider.set(0)
    slider.place(relx=0.5, y=100, anchor="c")

    #Slider Entry
    def set_slider_value():
        value = int(slider_value_entry.get())
        if axis == "x":
            if value < 0:
                value = 0
            elif value >= border.shape[0]:
                value = border.shape[0] - 1
        elif axis == "y":
            if value < 0:
                value = 0
            elif value >= border.shape[1]:
                value = border.shape[1] - 1
        elif axis == "z":
            if value < 0:
                value = 0
            elif value >= border.shape[2]:
                value = border.shape[2] - 1
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
            ax.imshow(border[x,:,:])
            canvas_widget.draw()
        elif (axis == "y"):
            y = int(slider.get())
            axis_value = y
            ax.imshow(border[:,y,:])
            canvas_widget.draw()
        elif (axis == "z"):
            z = int(slider.get())
            axis_value = z
            ax.imshow(border[:,:,z])
            canvas_widget.draw()
        
    slider.bind("<B1-Motion>", update_image)

    if fig is None:
        fig, ax= plt.subplots()
    else:
        ax.clear()
        
    if (axis == "x"):
        ax.imshow(border[0,:,:])
    elif (axis == "y"):
        ax.imshow(border[:,0,:])
    elif (axis == "z"):
        ax.imshow(border[:,:,0])
        
    if canvas_widget is None:
        canvas_widget = FigureCanvasTkAgg(fig,canvas)
        canvas_widget.get_tk_widget().pack()
    else:    
        canvas_widget.figure = fig
        canvas_widget.draw()

#Processing GUI
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
ctk.deactivate_automatic_dpi_awareness()
window = ctk.CTk()
window.title("Image Procesing App")
window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))

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
segmentation_label = ctk.CTkLabel(master=radiobutton_frame, text="Choose your segmentation method: ", font=("Times New Roman", 20, "bold"))

#Buttons
browse_button = ctk.CTkButton(welcome_frame, text="Browse Image", width=40, height=28, command=lambda: browse_file(selected_file_label, path_list, paths_combobox, paths_combobox2))
show_img_button = ctk.CTkButton(img_option_frame, text="Show Image", width=40 ,command= display_image)
apply_button = ctk.CTkButton(master=radiobutton_frame, text="Apply Method", width=40,command = lambda: option_clicked(get_updated_image(), option, axis,axis_value))
set_button = ctk.CTkButton(img_option_frame, text="Set",width=70,command=lambda: set_image(paths_combobox.get(), selected_file_label, selected_file_label2))
show_border_button = ctk.CTkButton(img_option_frame, text="Show Borders", width=40, command= display_borders)

#Radio Buttons

thresholding_button = ctk.CTkRadioButton(master=radiobutton_frame, text="Thresholding", variable = option, value="thresholding")
thresholding_button.configure(font=("Times New Roman", 20))
reg_growing_button = ctk.CTkRadioButton(master=radiobutton_frame, text="Region Growing", variable = option, value="region growing")
reg_growing_button.configure(font=("Times New Roman", 20))
k_means_button = ctk.CTkRadioButton(master=radiobutton_frame, text="K-means", variable = option, value="k-means")
k_means_button.configure(font=("Times New Roman", 20))

#Canvas
canvas = tkinter.Canvas(window, width=window_width/4, height=window_height/4)

#Combo Box
path_list = []
image_list=[]
paths_combobox = ctk.CTkComboBox(img_option_frame, width=190, state="readonly")
axis_list = ["x","y","z"]
axis_combobox = ctk.CTkComboBox(img_option_frame, width=200, values=axis_list, state="readonly")

#Pack
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
set_button.place(relx=0.8, y = 20, anchor="w")
axis_label.place(relx=0.05, y=60, anchor="w")
axis_combobox.place(relx=0.35, y=60, anchor="w")
show_img_button.place(relx=0.49, y = 180, anchor="e")
show_border_button.place(relx=0.51, y=180, anchor="w")
#Processing Methods Frame
radiobutton_frame.place(relx=0.25, rely=0.75, anchor="c")
segmentation_label.place(x=10, y= 20, anchor="w")
thresholding_button.place(x=10, y=60, anchor="w")
reg_growing_button.place(x=10, y=100, anchor="w")
k_means_button.place(x=10, y=140, anchor="w")
apply_button.place(x=160, y = 200, anchor="n")

#GUI Preprocessing
window2 = ctk.CTkToplevel()
window2.title("Prepocessing")
window2.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))
window2.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Frames
browse_frame = ctk.CTkFrame(window2, width=window_width/2, height=120)
select_frame = ctk.CTkFrame(window2, width= window_width/3, height=110)
standarization_frame = ctk.CTkFrame(window2, width= window_width/7, height=300)
noise_frame= ctk.CTkFrame(window2, width= window_width/7, height=300)

#Labels
browse_label = ctk.CTkLabel(browse_frame, text="Select a file you would like to Pre-process", font=("Times New Roman", 25, "bold"))
note_label = ctk.CTkLabel(browse_frame, text="Note that the image uploaded here will also appear in the Processing window", font=("Times New Roman", 12, "bold"))
selected_file_label2 = ctk.CTkLabel(browse_frame, text="")
choose_file_label=ctk.CTkLabel(select_frame, text="Choose the file you would like to Pre-process\nfrom the options below:", font=("Times New Roman", 20, "bold"))
standarization_label = ctk.CTkLabel(standarization_frame, text="Apply standarization\nMethod", font=("Times New Roman", 16, "bold"))
noise_label = ctk.CTkLabel(noise_frame, text="Apply noise reduction", font=("Times New Roman", 16, "bold"))
axis_label2 = ctk.CTkLabel(noise_frame, text="Choose axis:",font=("Times New Roman", 16, "bold"))

standarization_option = ctk.StringVar()
noise_option = ctk.StringVar()
#Buttons
browse_button = ctk.CTkButton(browse_frame, text="Browse Image", width=40, height=28, command=lambda: browse_file(selected_file_label2, path_list, paths_combobox, paths_combobox2))
standarization_button = ctk.CTkButton(standarization_frame, text="Show Histogram", width=40, height=28, command=lambda: method_clicked(standarization_option,canvas2))
noise_button = ctk.CTkButton(noise_frame, text="Show Image", width=40, height=28, command=lambda: denoise_clicked(noise_option, axis_combobox2, canvas2,window2))
set_img_button = ctk.CTkButton(select_frame, text="Set Image", width=100,command= lambda: set_image(paths_combobox2.get(), selected_file_label2, selected_file_label))

#Radio Buttons
rescaling_button = ctk.CTkRadioButton(standarization_frame, text="Rescaling", variable = standarization_option, value="rescaling", font=("Times New Roman", 16))
z_score_button = ctk.CTkRadioButton(standarization_frame, text="Z-Score", variable= standarization_option, value="z-score", font=("Times New Roman", 16))
white_stripe_button = ctk.CTkRadioButton(standarization_frame, text="White Stripe", variable=standarization_option, value="white-stripe", font=("Times New Roman",16))
pair_button = ctk.CTkRadioButton(standarization_frame, text="Histogram matching", variable=standarization_option,value="histogram-matching", font=("Times New Roman", 16))
mean_button = ctk.CTkRadioButton(noise_frame, text="Mean Filter", variable=noise_option, value="mean-filter", font=("Times New Roman", 16))
median_button = ctk.CTkRadioButton(noise_frame, text="Median Filter", variable=noise_option, value="median-filter", font=("Times New Roman", 16))
edge_button = ctk.CTkRadioButton(noise_frame, text="Edge filter", variable=noise_option, value="edge-filter", font=("Times New Roman", 16))
#ComboBox
paths_combobox2 = ctk.CTkComboBox(select_frame, width=200, state="readonly")
axis_combobox2 = ctk.CTkComboBox(noise_frame, width=105, state="readonly", values=["x","y","z"])
#Canvas
canvas2 = tkinter.Canvas(window2, width=window_width/4, height=window_height/4)

#Pack
#Browse-Frame
browse_frame.place(relx=0.5, rely=0.01, anchor="n")
browse_label.place(relx=0.5 , y=5,  anchor="n")
note_label.place(relx=0.5, y=35, anchor="n")
browse_button.place(relx=0.5, y=80, anchor="c")
selected_file_label2.place(relx=0.5, y=90,  anchor="n")
#Canvas
canvas2.place(relx=0.3, rely=0.56, anchor="c")
#Select-Frame
select_frame.place(relx=0.75, rely=0.3, anchor="c")
choose_file_label.place(relx=0.1, rely=0.25, anchor="w")
paths_combobox2.place(relx=0.4, rely=0.7, anchor="c")
set_img_button.place(relx=0.75, rely=0.7, anchor="c")
#Standarization-Frame
standarization_frame.place(relx=0.66, rely=0.425, anchor="n")
standarization_label.place(relx=0.5, rely=0.025, anchor="n")
rescaling_button.place(relx=0.1, rely= 0.2, anchor="w")
z_score_button.place(relx=0.1, rely= 0.35, anchor="w")
white_stripe_button.place(relx=0.1, rely= 0.5, anchor="w")
pair_button.place(relx=0.1, rely= 0.65, anchor="w")
standarization_button.place(relx=0.5, rely=0.9, anchor="c")
#Noise-Frame
noise_frame.place(relx=0.84, rely=0.425, anchor="n")
noise_label.place(relx=0.5, rely=0.05, anchor="n")
mean_button.place(relx=0.1, rely=0.2, anchor="w")
median_button.place(relx=0.1, rely= 0.35, anchor="w")
edge_button.place(relx=0.1, rely=0.5, anchor="w")
noise_button.place(relx=0.5, rely=0.9, anchor="c")
axis_label2.place(relx=0.5, rely=0.6, anchor="c")
axis_combobox2.place(relx=0.5, rely=0.7, anchor="c")

window.withdraw()

#Sidebar for window
add_sidebar(window, window2)
#Sidebar for window2
add_sidebar(window2, window)

window.mainloop()

