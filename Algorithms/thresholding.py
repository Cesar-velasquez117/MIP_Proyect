import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter

def threshold_img(path, tolerance, tau, axis, axis_value):
    image_data = nib.load(path)
    image = image_data.get_fdata()

    while True:
        segmentation = image >= tau
        mBG = image[np.multiply(image > 10, segmentation == 0)].mean()
        mFG = image[np.multiply(image > 10, segmentation == 1)].mean()
    
        post_tau = 0.5 * (mBG + mFG)

        if np.abs(tau-post_tau) < tolerance:
            break
        else:
            tau = post_tau
        
    #Show image
    if (axis == "x"):
        plt.imshow(segmentation[axis_value,:,:])
    elif (axis == "y"):
        plt.imshow(segmentation[:,axis_value,:])
    elif (axis == "z"):
        plt.imshow(segmentation[:,:,axis_value])
    #Show histogram
    #plt.hist(image.flatten(), 50)
    plt.show()

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def on_validate_float(new_value):
    if new_value.strip() == "":
        return True
    return is_float(new_value)

def thresholding_form(path, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tau=float(tau_entry.get())
        tol=float(tolerance_entry.get())

        threshold_img(path,tol,tau, axis, axis_value)

        tau_entry.delete(0, tkinter.END)
        tolerance_entry.delete(0, tkinter.END)
        top.destroy()
    #GUI
    top = ctk.CTkToplevel()
    top.title("Thresholding Form")
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

    #Frame
    form_frame = ctk.CTkFrame(top, width=top_width*0.8, height=top_height*0.8)

    #Label
    title_label = ctk.CTkLabel(form_frame, text="Thresholding Form", font=("Times New Roman", 20, "bold"))
    tolerance_label = ctk.CTkLabel(form_frame, text="Tolerance: ", font=("Times New Roman", 20, "bold"))
    tau_label = ctk.CTkLabel(form_frame, text="Tau: ", font=("Times New Roman", 20, "bold"))

    #Textfield
    tolerance_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))
    tau_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    tau_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))

    #Button
    finish_button = ctk.CTkButton(form_frame, text="Finish Form", width=50, height=30, command=finish_form)

    #Pack
    form_frame.place(relx=0.5, rely=0.5, anchor="c")
    title_label.place(relx=0.5, rely=0.1, anchor="n")
    tolerance_label.place(relx=0.2, rely=0.4, anchor="w")
    tau_label.place(relx=0.2, rely=0.6, anchor="w")
    tolerance_entry.place(relx=0.5, rely=0.4, anchor="w")
    tau_entry.place(relx=0.5, rely=0.6, anchor="w")
    finish_button.place(relx=0.5, rely= 0.85, anchor="n")

    top.mainloop()

if __name__ == '__main__':
    thresholding_form()
