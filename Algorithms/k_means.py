import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tkinter

def k_img(path,tolerance, iterations, axis, axis_value):
    image_data = nib.load(path)
    image = image_data.get_fdata()

    k1 = np.amin(image)
    k2 = np.mean(image)
    k3 = np.amax(image) 

    for i in range(0,iterations):
        d1 = np.abs(k1-image)
        d2 = np.abs(k2-image)
        d3 = np.abs(k3-image)

        segmentation = np.zeros_like(image)
        segmentation[np.multiply(d1 < d2, d1 < d3)] = 0
        segmentation[np.multiply(d2 < d1, d2 < d3)] = 1
        segmentation[np.multiply(d3 < d1, d3 < d2)] = 2

        k1 = image[segmentation == 0].mean()
        k2 = image[segmentation == 1].mean()
        k3 = image[segmentation == 2].mean()

        if np.abs(k1 - k2) < tolerance and np.abs(k2-k3) < tolerance and np.abs(k1-k3) < tolerance:
            break


    #Show image
    if (axis == "x"):
        plt.imshow(segmentation[axis_value,:,:])
    elif (axis == "y"):
        plt.imshow(segmentation[:,axis_value,:])
    elif (axis == "z"):
        plt.imshow(segmentation[:,:,axis_value])
    #Show histogram
    #plt.hist(image.flatten(), 100)
    plt.show()

def k_form(path, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tol=float(tolerance_entry.get())
        i=int(iteration_entry.get())

        k_img(path,tol,i,axis, axis_value)

        top.destroy()
    #GUI
    top = tkinter.Toplevel()
    top.title("K-Means Form")
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
    title_label = tkinter.Label(top, text="K-Means Form", font=("Times New Roman", 15, "bold"))
    tolerance_label = tkinter.Label(top, text="Tolerance: ", font=("Times New Roman", 15, "bold"))
    iteration_label = tkinter.Label(top, text="# Iterations: ", font=("Times New Roman", 15, "bold"))

    #Textfield
    tolerance_entry = tkinter.Entry(top, width=20, text="tolerance")
    iteration_entry = tkinter.Entry(top, width=10, text="iterations")

    #Button
    finish_button = tkinter.Button(top, text="Finish Form", width=20, height=2, command=finish_form)

    #Pack
    title_label.place(x=top_width/2, y=10, anchor="n")
    tolerance_label.place(x=top_width*0.1, y=70, anchor="w")
    iteration_label.place(x=top_width*0.1, y=100, anchor="w")
    tolerance_entry.place(x=top_width*0.4, y=70, anchor="w")
    iteration_entry.place(x=top_width*0.4, y=100, anchor="w")
    finish_button.place(x=top_width/2, y= 200, anchor="n")

    top.mainloop()

if __name__ == '__main__':
    k_form()