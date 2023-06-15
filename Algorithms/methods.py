
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter
import nibabel as nib
import os
from Preprocessing.methods import get_updated_path
#Auxiliary Functions
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
#Function to validate if the digit typed is an integer
def on_validate_int(new_value):
    if new_value.strip() == "":
        return True
    return is_int(new_value)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#Function to validate if the digit typed is a float
def on_validate_float(new_value):
    if new_value.strip() == "":
        return True
    return is_float(new_value)
#Function to save the image 
def save_image(image, filename):
    name , extension = os.path.splitext(os.path.basename(get_updated_path()))
    name = name.split('.')[0]
    imageUploaded = nib.load(get_updated_path())
    affine = imageUploaded.affine
    # Create a nibabel image object from the image data
    image = nib.Nifti1Image(image.astype(np.float32), affine=affine)
    # Save the image as a NIfTI file
    output_path = os.path.join("Segmentations", name+"_"+filename)
    nib.save(image, output_path)
#K-Means algorithm
def k_img(image, tolerance, iterations, k, axis, axis_value):
    # initialize centroids
    centroids = np.linspace(np.amin(image), np.amax(image), num=k)
    for i in range(iterations):
        distance = np.abs(image[..., np.newaxis] - centroids)
        segmentation = np.argmin(distance, axis=-1)

        for id in range(k):
            centroids[id] = image[segmentation == id].mean()

    save_image(segmentation, "k-means_segmentation.nii.gz")
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

def k_form(image, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tol=float(tolerance_entry.get())
        i=int(iteration_entry.get())
        k=int(k_entry.get())

        k_img(image,tol,i,k,axis, axis_value)

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

#Region Growing Algorithm
def region_img(image, tolerance, origin_x, origin_y ,origin_z, axis, axis_value):
    valor_medio_cluster = image[origin_x, origin_y, origin_z]
    segmentation = np.zeros_like(image)
    segmentation[origin_x, origin_y, origin_z] = 1
    neighbors=[(origin_x, origin_y, origin_z)]
    while neighbors:
      x, y, z = neighbors.pop()

      for dx in [-1, 0, 1] :
        for dy in [-1, 0, 1] :
          for dz in [-1, 0, 1]:
            if(
                ((x+dx) < image.shape[0]) and 
                ((x+dx) >= 0) and
                ((y+dy) < image.shape[1]) and 
                ((y+dy) >= 0) and
                ((z+dz) < image.shape[2]) and
                ((z+dz) >= 0)
                ):
                  if np.abs(valor_medio_cluster - image[x+dx, y+dy, z + dz]) < tolerance and segmentation[x+dx, y+dy, z+dz] == 0 :
                        segmentation[x+dx, y+dy, z+dz] = 1
                        neighbors.append((x+dx, y+dy, z+dz))

    # Verificar si el archivo existe
    save_image(segmentation, "rg_segmentation.nii.gz")
    # segmented_img = nib.Nifti1Image(segmentation.astype(np.float32), affine=np.eye(4))
    # nib.save(segmented_img, "Segmentations/rg_segmentation.nii.gz")
    if (axis == "x"):
        plt.imshow(segmentation[axis_value,:,:])
    elif (axis == "y"):
        plt.imshow(segmentation[:,axis_value,:])
    elif (axis == "z"):
        plt.imshow(segmentation[:,:,axis_value])
    #Show histogram
    #plt.hist(image.flatten(), 50)
    plt.show()

def region_form(image, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tol=float(tolerance_entry.get())
        x = int(x_entry.get())
        y = int(y_entry.get())
        z = int(z_entry.get())

        region_img(image,tol,x,y,z,axis,axis_value)

        tolerance_entry.delete(0, tkinter.END)
        x_entry.delete(0, tkinter.END)
        y_entry.delete(0, tkinter.END)
        z_entry.delete(0, tkinter.END)

        top.destroy()

    top = ctk.CTkToplevel()
    top.title("Region Growing Form")
    top.grab_set() #Block the main window
    top.protocol("WM_DELETE_WINDOW", lambda: top.destroy())
    #Get screen dimensions
    screen_width = 1920
    screen_height = 1080
    #Set window dimensions
    top_width = int(screen_width * 0.25)
    top_height = int(screen_height*0.4)
    #Position
    top_x = int(screen_width/3)
    top_y = int(screen_height/4)
    top.geometry(f"{top_width}x{top_height}+{top_x}+{top_y}")

    #Frame
    form_frame = ctk.CTkFrame(top, width=top_width*0.8, height=top_height*0.8)

    #Label
    title_label = ctk.CTkLabel(form_frame, text="Region Growing Form", font=("Times New Roman", 20, "bold"))
    tolerance_label = ctk.CTkLabel(form_frame, text="Tolerance: ", font=("Times New Roman", 20, "bold"))
    seed_label = ctk.CTkLabel(form_frame, text="Seed: ", font=("Times New Roman", 20, "bold"))
    x_label = ctk.CTkLabel(form_frame, text="X: ", font=("Times New Roman", 20, "bold"))
    y_label = ctk.CTkLabel(form_frame, text="Y: ", font=("Times New Roman", 20, "bold"))
    z_label = ctk.CTkLabel(form_frame, text="Z: ", font=("Times New Roman", 20, "bold"))
    #Textfield
    tolerance_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))
    x_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    x_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    y_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    y_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    z_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    z_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))

    #Button
    finish_button = ctk.CTkButton(form_frame, text="Finish Form", width=50, height=30, command=finish_form)

    #Pack
    form_frame.place(relx=0.5, rely=0.5, anchor="c")
    title_label.place(relx=0.5, rely=0.1, anchor="n")
    tolerance_label.place(relx=0.2, rely=0.3, anchor="w")
    seed_label.place(relx=0.2, rely=0.4, anchor="w")
    x_label.place(relx=0.2, rely=0.5, anchor="w")
    y_label.place(relx=0.2, rely=0.6, anchor="w")
    z_label.place(relx=0.2, rely=0.7, anchor="w")
    tolerance_entry.place(relx=0.5, rely=0.3, anchor="w")
    x_entry.place(relx=0.5, rely=0.5, anchor="w")
    y_entry.place(relx=0.5, rely=0.6, anchor="w")
    z_entry.place(relx=0.5, rely=0.7, anchor="w")
    finish_button.place(relx=0.5, rely= 0.85, anchor="n")

    top.mainloop()

def threshold_img(image, tolerance, tau, axis, axis_value):
    while True:
        segmentation = image >= tau
        #For the Background
        mBG = image[segmentation == False]
        if len(mBG) > 0:
            mBG = np.nan_to_num(mBG, nan=0)
            mBG = mBG.mean()
        else:
            mBG = 0

        #For the Foreground
        mFG = image[segmentation]
        if len(mFG) > 0:
            mFG = np.nan_to_num(mFG, nan=0)
            mFG = mFG.mean()
        else:
            mFG = 0

        # Update tau
        post_tau = 0.5 * (mBG + mFG)

        # Check if accepts the tolerance, if not, continue iterating
        if np.abs(tau - post_tau) < tolerance:
            break
        else:
            tau = post_tau
        
    # Guardar la imagen
    save_image(segmentation, "isodata_segmentation.nii.gz")
    # segmented_img = nib.Nifti1Image(segmentation.astype(np.float32), affine=np.eye(4))
    # nib.save(segmented_img, "Segmentations/isodata_segmentation.nii.gz")
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
    
def thresholding_form(image, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tau=float(tau_entry.get())
        tol=float(tolerance_entry.get())

        threshold_img(image,tol,tau, axis, axis_value)

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

#Gaussian Mixtures Models Algorithm
def likehood(image, mean, std):
    return np.exp(-0.5 * ((image-mean)/std) **2)/(std * np.sqrt(2 * np.pi))

def gaussian_mixtures(image, clusters, iterations,tolerance, axis, axis_value):
    voxels = np.prod(image.shape)
    mean = np.linspace(image.min(), image.max())
    std = np.ones(clusters)*(image.max() - image.min())/ (2*clusters)
    pre_probability = np.ones(clusters)/clusters
    post_probaility = np.zeros((voxels,clusters))

    for i in range(iterations):
        for k in range(clusters):
            post_probaility[:,k]= pre_probability[k] * likehood(image.flatten(), mean[k], std[k])
        post_probaility = post_probaility/np.sum(post_probaility, axis=1)[:,np.newaxis]
    
        new = np.sum(post_probaility, axis=0)
        pre_probability = new/voxels
        mean = np.sum(post_probaility*image.flatten()[:,np.newaxis], axis=0)/new
        std = np.sqrt(np.sum(post_probaility*(image.flatten()[:,np.newaxis] - mean) **2, axis=0)/new)

        if np.max(np.abs(pre_probability - post_probaility.sum(axis=0)/voxels)) < tolerance:
            break
    
    segmentation = np.argmax(post_probaility, axis=1)
    segmentation = segmentation.reshape(image.shape)
    # Verificar si el archivo existe
    save_image(segmentation, "gaussian_segmentation.nii.gz")
    # segmented_img = nib.Nifti1Image(segmentation.astype(np.float32), affine=np.eye(4))
    # nib.save(segmented_img, "Segmentations/gaussian_segmentation.nii.gz")
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

def gaussian_form(image, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        k=int(segment_entry.get())
        iterations=int(iteration_entry.get())
        tol=float(tolerance_entry.get())

        gaussian_mixtures(image,k,iterations, tol,axis, axis_value)

        segment_entry.delete(0, tkinter.END)
        iteration_entry.delete(0, tkinter.END)
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
    title_label = ctk.CTkLabel(form_frame, text="GMM Form", font=("Times New Roman", 20, "bold"))
    segments_label = ctk.CTkLabel(form_frame, text="# Segments: ", font=("Times New Roman", 20, "bold"))
    iterations_label = ctk.CTkLabel(form_frame, text="# Iterations: ", font=("Times New Roman", 20, "bold"))
    tolerance_label = ctk.CTkLabel(form_frame, text="Tolerance: ", font=("Times New Roman", 20, "bold"))

    #Textfield
    segment_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    segment_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    iteration_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    iteration_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    tolerance_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))

    #Button
    finish_button = ctk.CTkButton(form_frame, text="Finish Form", width=50, height=30, command=finish_form)

    #Pack
    form_frame.place(relx=0.5, rely=0.5, anchor="c")
    title_label.place(relx=0.5, rely=0.1, anchor="n")
    segments_label.place(relx=0.2, rely=0.3, anchor="w")
    iterations_label.place(relx=0.2, rely=0.5, anchor="w")
    tolerance_label.place(relx=0.2, rely=0.7, anchor="w")
    segment_entry.place(relx=0.5, rely=0.3, anchor="w")
    iteration_entry.place(relx=0.5, rely=0.5, anchor="w")
    tolerance_entry.place(relx=0.5, rely=0.7, anchor="w")
    finish_button.place(relx=0.5, rely= 0.85, anchor="n")

    top.mainloop()

########################################################################################