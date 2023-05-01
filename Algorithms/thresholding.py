import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
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
    top = tkinter.Toplevel()
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

    #Label
    title_label = tkinter.Label(top, text="Thresholding Form", font=("Times New Roman", 15, "bold"))
    tolerance_label = tkinter.Label(top, text="Tolerance: ", font=("Times New Roman", 15, "bold"))
    tau_label = tkinter.Label(top, text="Tau: ", font=("Times New Roman", 15, "bold"))

    #Textfield
    tolerance_entry = tkinter.Entry(top, width=20, text="tolerance", validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))
    tau_entry = tkinter.Entry(top, width=20, text="tau",validate="key")
    tau_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))

    #Button
    finish_button = tkinter.Button(top, text="Finish Form", width=20, height=2, command=finish_form)

    #Pack
    title_label.place(x=top_width/2, y=10, anchor="n")
    tolerance_label.place(x=top_width*0.1, y=70, anchor="w")
    tau_label.place(x=top_width*0.1, y=100, anchor="w")
    tolerance_entry.place(x=top_width*0.4, y=70, anchor="w")
    tau_entry.place(x=top_width*0.4, y=100, anchor="w")
    finish_button.place(x=top_width/2, y= 200, anchor="n")

    top.mainloop()

if __name__ == '__main__':
    thresholding_form()
