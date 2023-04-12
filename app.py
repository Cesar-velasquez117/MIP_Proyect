import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

#FUNCTIONS
def browse_file():
    file_path = filedialog.askopenfilename()
    selected_file_label.config(text=file_path)

def display_image():
    file_path = selected_file_label.cget("text")
    if file_path:
        image_data=nib.load(file_path)
        image = image_data.get_fdata()
        image = image[:,:,20]
        image = (image - np.min(image)) / (np.max(image) - np.min(image)) #Normalization

        img = Image.fromarray((image*255).astype(np.uint8))
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0,0, anchor="nw", image=photo)
        canvas.image = photo

def option_clicked():
    selected_option = option.get()
    if selected_option == "thresholding":
        top = tkinter.Toplevel()
        top.title("Thresholding Form")
        top.grab_set() #Block the main window
        top.protocol("WM_DELETE_WINDOW", lambda: top.destroy())
        #Get screen dimensions
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        #Set window dimensions
        top_width = int(screen_width * 0.25)
        top_height = int(screen_height*0.3)
        #Position
        top_x = int(screen_width/3)
        top_y = int(screen_height/4)
        top.geometry(f"{top_width}x{top_height}+{top_x}+{top_y}")

        #Label
        tolerance_label = tkinter.Label(top, text="Tolerance: ", font=("Times New Roman", 15, "bold"))
        tau_label = tkinter.Label(top, text="Tau: ", font=("Times New Roman", 15, "bold"))

        #Textfield
        tolerance_entry = tkinter.Entry(top, width=10, text="tolerance")
        tau_entry = tkinter.Entry(top, width=10, text="tau")

        #Pack
        tolerance_label.pack(pady=5)
        tau_label.pack(pady=5)
        tolerance_entry.pack(side= tkinter.RIGHT, pady=5)
        tau_entry.pack(side= tkinter.RIGHT, pady=5)

        top.mainloop()

#GUI

window = tkinter.Tk()
window.title("Image Procesing App")

#Get screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
#Set window dimensions
window_width = int(screen_width * 0.5)
window_height = int(screen_height*0.6)
#Position
x = int(screen_width/4)
y = int(screen_height/4)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Variable to store the selected option of the radio buttons
option = tkinter.StringVar()

#Labels
welcome_label = tkinter.Label(window, text="Welcome user ", font=("Times New Roman", 15, "bold"))
selected_file_label = tkinter.Label(window)

#Buttons
browse_button = tkinter.Button(window, text="Browse", command=browse_file)
show_img_button = tkinter.Button(window, text="Show Image", command= display_image)
apply_button = tkinter.Button(window, text="Segment", command = option_clicked)

#Radio Buttons
thresholding_button = tkinter.Radiobutton(window, text="Thresholding", variable = option, value="thresholding")
reg_growing_button = tkinter.Radiobutton(window, text="Region Growing", variable = option, value="region growing")
k_means_button = tkinter.Radiobutton(window, text="K-means", variable = option, value="k-means")

#Canvas
canvas = tkinter.Canvas(window, width=520, height=512 )

#Textfield
x_entry = tkinter.Entry(window, width=10, text="Width")
y_entry = tkinter.Entry(window, width=10, text="Height")
z_entry = tkinter.Entry(window, width=10, text="Dimension")



#Pack
welcome_label.pack()
browse_button.pack()
selected_file_label.pack()
canvas.pack(side=tkinter.RIGHT)
x_entry.pack(pady=5)
y_entry.pack(pady=5)
z_entry.pack(pady=5)
show_img_button.pack(pady=5)
thresholding_button.pack(pady=5)
reg_growing_button.pack(pady=5)
k_means_button.pack(pady=5)
apply_button.pack(pady=5)

window.mainloop()