import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tkinter

def k_img(path,tolerance, iterations, k, axis, axis_value):
    image_data = nib.load(path)
    image = image_data.get_fdata()

    # initialize centroids
    centroids = np.random.choice(image.flatten(), k)
    centroids_old = centroids.copy()

    for i in range(0, iterations):
        distances = np.zeros((image.shape[0], image.shape[1], image.shape[2], k))
        for j, c in enumerate(centroids):
            distances[:, :, :, j] = np.sqrt((image - c) ** 2)
        segmentation = np.argmin(distances, axis=-1)

        for j in range(k):
            cluster = image[segmentation == j]
            if len(cluster) > 0:
                centroids[j] = cluster.mean()

        if np.allclose(centroids, centroids_old, atol=tolerance):
            break

        centroids_old = centroids.copy()

    #Show image
    if (axis == "x"):
        plt.imshow(segmentation[axis_value,:,:])
    elif (axis == "y"):
        plt.imshow(segmentation[:,axis_value,:])
    elif (axis == "z"):
        plt.imshow(segmentation[:,:,axis_value])
    # Show histogram
    # plt.hist(image.flatten(), 100)
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

def k_form(path, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tol=float(tolerance_entry.get())
        i=int(iteration_entry.get())
        k=int(k_entry.get())

        k_img(path,tol,i,k,axis, axis_value)

        tolerance_entry.delete(0, tkinter.END)
        iteration_entry.delete(0, tkinter.END)
        k_entry.delete(0, tkinter.END)
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
    k_label = tkinter.Label(top, text="# K's: ", font=("Times New Roman", 15, "bold"))

    #Textfield
    tolerance_entry = tkinter.Entry(top, width=20, validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))
    iteration_entry = tkinter.Entry(top, width=10, validate="key")
    iteration_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    k_entry = tkinter.Entry(top, width=10,validate="key")
    k_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))

    #Button
    finish_button = tkinter.Button(top, text="Finish Form", width=20, height=2, command=finish_form)

    #Pack
    title_label.place(x=top_width/2, y=10, anchor="n")
    tolerance_label.place(x=top_width*0.1, y=70, anchor="w")
    iteration_label.place(x=top_width*0.1, y=100, anchor="w")
    k_label.place(x=top_width*0.1, y=130, anchor="w")
    tolerance_entry.place(x=top_width*0.4, y=70, anchor="w")
    iteration_entry.place(x=top_width*0.4, y=100, anchor="w")
    k_entry.place(x=top_width*0.4, y=130, anchor="w")
    finish_button.place(x=top_width/2, y= 200, anchor="n")

    top.mainloop()

if __name__ == '__main__':
    k_form()