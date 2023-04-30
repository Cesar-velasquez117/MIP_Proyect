import tkinter
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Algorithms.thresholding import thresholding_form
from Algorithms.k_means import k_form

#FUNCTIONS
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
      selected_file_label.config(text=file_path)
      path_list.append(file_path)
      #Updates the values in the Combo box
      paths_combobox.config(values=path_list)

canvas_widget = None
def display_image():
    global canvas_widget
    file_path = paths_combobox.get()
    if file_path:
        image_data=nib.load(file_path)
        image = image_data.get_fdata()
        canvas.delete("all")

        fig, ax= plt.subplots()
        ax.imshow(image[:,:,20])

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
        thresholding_form(file_path)
    
    if selected_option == "region growing":
        top = tkinter.Toplevel()
        top.title("Region Growing Form")
        top.grab_set() #Block the main window
        top.protocol("WM_DELETE_WINDOW", lambda: top.destroy())
        #Get screen dimensions
        screen_width = 1920
        screen_height = 1080
        #Set window dimensions
        top_width = int(screen_width * 0.25)
        top_height = int(screen_height*0.3)
        #Position
        top_x = int(screen_width/3)
        top_y = int(screen_height/4)
        top.geometry(f"{top_width}x{top_height}+{top_x}+{top_y}")

        #Label
        title_label = tkinter.Label(top, text="Region Growing Form", font=("Times New Roman", 15, "bold"))
        tolerance_label = tkinter.Label(top, text="Tolerance: ", font=("Times New Roman", 15, "bold"))
        tau_label = tkinter.Label(top, text="Tau: ", font=("Times New Roman", 15, "bold"))

        #Textfield
        tolerance_entry = tkinter.Entry(top, width=20, text="tolerance")
        tau_entry = tkinter.Entry(top, width=20, text="tau")

        #Button
        finish_button = tkinter.Button(top, text="Finish Form", width=20, height=2)

        #Pack
        title_label.place(x=top_width/2, y=10, anchor="n")
        tolerance_label.place(x=top_width*0.1, y=70, anchor="w")
        tau_label.place(x=top_width*0.1, y=100, anchor="w")
        tolerance_entry.place(x=top_width*0.4, y=70, anchor="w")
        tau_entry.place(x=top_width*0.4, y=100, anchor="w")
        finish_button.place(x=top_width/2, y= 200, anchor="n")

        top.mainloop()

    if selected_option == "k-means":
        k_form(file_path)
    
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
#original_button = tkinter.Radiobutton(window, text="Original", variable =option, value="original")
#original_button.config(font=("Times New Roman", 16), padx=10, pady=10)
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
show_img_button.place(x=180, y = 180, anchor="n")
segmentation_label.place(x=10, y= 230, anchor="w")
#original_button.place(x=10, y= 270, anchor="w")
thresholding_button.place(x=10, y=310, anchor="w" )
reg_growing_button.place(x=10, y=350, anchor="w")
k_means_button.place(x=10, y=390, anchor="w")
apply_button.place(x=180, y = 580, anchor="n")

window.mainloop()