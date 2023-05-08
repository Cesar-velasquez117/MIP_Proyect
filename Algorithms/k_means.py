import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
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
    top = ctk.CTkToplevel()
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

    #Frame
    form_frame = ctk.CTkFrame(top, width=top_width*0.8, height=top_height*0.8)

    #Label
    title_label = ctk.CTkLabel(form_frame, text="K-Means Form", font=("Times New Roman", 20, "bold"))
    tolerance_label = ctk.CTkLabel(form_frame, text="Tolerance: ", font=("Times New Roman", 20, "bold"))
    iteration_label = ctk.CTkLabel(form_frame, text="# Iterations: ", font=("Times New Roman", 20, "bold"))
    k_label = ctk.CTkLabel(form_frame, text="# K's: ", font=("Times New Roman", 20, "bold"))

    #Textfield
    tolerance_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))
    iteration_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    iteration_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    k_entry = ctk.CTkEntry(form_frame, width=140,validate="key")
    k_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))

    #Button
    finish_button = ctk.CTkButton(form_frame, text="Finish Form", width=50, height=30, command=finish_form)

    #Pack
    form_frame.place(relx=0.5, rely=0.5, anchor="c")
    title_label.place(relx=0.5, rely=0.1, anchor="n")
    tolerance_label.place(relx=0.2, rely=0.3, anchor="w")
    iteration_label.place(relx=0.2, rely=0.5, anchor="w")
    k_label.place(relx=0.2, rely=0.7, anchor="w")
    tolerance_entry.place(relx=0.5, rely=0.3, anchor="w")
    iteration_entry.place(relx=0.5, rely=0.5, anchor="w")
    k_entry.place(relx=0.5, rely=0.7, anchor="w")
    finish_button.place(relx=0.5, rely= 0.85, anchor="n")

    top.mainloop()

if __name__ == '__main__':
    k_form()