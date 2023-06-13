from scipy.signal import find_peaks
import nibabel as nib
import matplotlib.pyplot as plt
import os
import numpy as np
import customtkinter as ctk
import SimpleITK as sitk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.globals import canvas_widget2, fig2, ax2, ax3, slider2, set_value_button2, slider_value_entry2, image

path=""
def set_image(file_path, label1, label2):
    global image, path
    image= nib.load(file_path).get_fdata()
    path = file_path
    label1.configure(text="Current image: " + path)
    label2.configure(text="Current image: " + path)


def get_updated_image():
    global image
    return image

def delete_fig():
    global fig2
    if fig2 is not None:
        fig2.clf()
        plt.close(fig2)

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

def show_image(original, filtered, canva, axis, window):
    global canvas_widget2, fig2, ax2, ax3, slider2, set_value_button2, slider_value_entry2
    canva.delete("all")
    #Slider 
    global axis2
    axis2 = axis
    if (axis2 == "x"):
        slider2 = ctk.CTkSlider(window, from_=0, to=original.shape[0]-1)
    elif (axis2 == "y"):
        slider2 = ctk.CTkSlider(window, from_=0, to=original.shape[1]-1)
    elif (axis2 == "z"):
        slider2 = ctk.CTkSlider(window, from_=0, to=original.shape[2]-1)
    slider2.set(0)
    slider2.place(relx=0.175, rely=0.95, anchor="c")

    #Slider Entry
    def set_slider_value():
        value = int(slider_value_entry2.get())
        if axis2 == "x":
            if value < 0:
                value = 0
            elif value >= original.shape[0]:
                value = original.shape[0] - 1
        elif axis2 == "y":
            if value < 0:
                value = 0
            elif value >= original.shape[1]:
                value = original.shape[1] - 1
        elif axis2 == "z":
            if value < 0:
                value = 0
            elif value >= original.shape[2]:
                value = original.shape[2] - 1
        slider2.set(value)
        update_image()

    slider_value_entry2 = ctk.CTkEntry(window, validate="key")
    slider_value_entry2.configure(validatecommand=(window.register(on_validate_int), '%P'))
    slider_value_entry2.place(relx=0.375, rely=0.95, anchor="e")
    set_value_button2 = ctk.CTkButton(window, text="Go", command=set_slider_value)
    set_value_button2.place(relx=0.395, rely=0.95, anchor="w")

    def update_image(*args):
        global axis_value2
        if (axis2 == "x"):
            x = int(slider2.get())
            axis_value2 = x
            ax2.imshow(original[x,:,:])
            ax3.imshow(filtered[x,:,:])
            canvas_widget2.draw()
        elif (axis2 == "y"):
            y = int(slider2.get())
            axis_value2 = y
            ax2.imshow(original[:,y,:])
            ax3.imshow(filtered[:,y,:])
            canvas_widget2.draw()
        elif (axis2 == "z"):
            z = int(slider2.get())
            axis_value2 = z
            ax2.imshow(original[:,:,z])
            ax3.imshow(filtered[:,:,z])
            canvas_widget2.draw()
        
    slider2.bind("<B1-Motion>", update_image)

    if fig2 is not None:
        fig2.clf()
        fig2 = None
        ax2 = None
        ax3 = None
        canvas_widget2.get_tk_widget().destroy()
        canvas_widget2 = None
        
    fig2, (ax2,ax3)= plt.subplots(1,2)

    if (axis2 == "x"):
        ax2.imshow(original[0,:,:])
        ax3.imshow(filtered[0,:,:])
    elif (axis2 == "y"):
        ax2.imshow(original[:,0,:])
        ax3.imshow(filtered[:,0,:])
    elif (axis2 == "z"):
        ax2.imshow(original[:,:,0])
        ax3.imshow(filtered[:,:,0])
        
    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=580, height=435)
    canvas_widget2.get_tk_widget().pack()

############################################################################################################
#Standarization Methods

def rescaling(canva):
    global canvas_widget2, fig2, ax2, ax3, image, path, slider2, set_value_button2, slider_value_entry2
    canva.delete("all")
    min_value = image.min()
    max_value = image.max()

    img_data_rescaled = (image - min_value) / (max_value - min_value)
    image = img_data_rescaled
    #Create a neew figure and plot the histogram
    if fig2 is not None:
        fig2.clf()
        fig2 = None
        ax2 = None
        ax3 = None
        canvas_widget2.get_tk_widget().destroy()
        canvas_widget2 = None
        if slider2 is not None:
            slider2.destroy()
            slider2 = None
            set_value_button2.destroy()
            set_value_button2 = None
            slider_value_entry2.destroy()
            slider_value_entry2 = None
    
    fig2, ax2 = plt.subplots()
        
    ax2.hist(img_data_rescaled[img_data_rescaled>0.01].flatten(),bins=100)
    #Medidas originales (640,480)
    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

def zscore(canva):
    global canvas_widget2, fig2, ax2, ax3, image, path, slider2, set_value_button2, slider_value_entry2
    canva.delete("all")
    mean_value = image[image>10].mean()
    std_deviation_value = image[image>10].std()

    img_data_rescaled = (image - mean_value) / std_deviation_value
    image = img_data_rescaled
    #Create a neew figure and plot the histogram
    if fig2 is not None:
        fig2.clf()
        fig2 = None
        ax2 = None
        ax3 = None
        canvas_widget2.get_tk_widget().destroy()
        canvas_widget2 = None
        if slider2 is not None:
            slider2.destroy()
            slider2 = None
            set_value_button2.destroy()
            set_value_button2 = None
            slider_value_entry2.destroy()
            slider_value_entry2 = None
    
    fig2, ax2 = plt.subplots()
    ax2.hist(img_data_rescaled.flatten(),bins=100)

    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

def white_stripe(canva):
    global canvas_widget2, fig2, ax2, ax3, image, path, slider2, set_value_button2, slider_value_entry2
    canva.delete("all")
    #Calcular el histograma
    hist, bin_edges = np.histogram(image.flatten(), bins=100)
    #Encontrar picos
    peaks, _ = find_peaks(hist, height=100)
    val_peaks = bin_edges[peaks]

    #Rescalado de la imagen
    img_data_rescaled = image/val_peaks[1]
    image = img_data_rescaled

    #Mostrar el histograma con los picos identificados
    if fig2 is not None:
        fig2.clf()
        fig2 = None
        ax2 = None
        ax3 = None
        canvas_widget2.get_tk_widget().destroy()
        canvas_widget2 = None
        if slider2 is not None:
            slider2.destroy()
            slider2 = None
            set_value_button2.destroy()
            set_value_button2 = None
            slider_value_entry2.destroy()
            slider_value_entry2 = None
    
    fig2, ax2 = plt.subplots()
    ax2.hist(img_data_rescaled.flatten(), 100)

    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

def hist_matching(canva):
    global canvas_widget2, fig2, ax2,ax3, image, slider2, set_value_button2, slider_value_entry2
    k = 40
    file_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
    reference_image = nib.load(file_path).get_fdata()

    ref_hist = reference_image.flatten()
    img_hist = image.flatten()

    ref_landmarks = np.percentile(ref_hist, np.linspace(0,100,k))
    img_landmarks = np.percentile(img_hist, np.linspace(0,100,k))

    mapping = np.interp(img_hist, img_landmarks, ref_landmarks)
    matched_image = mapping.reshape(image.shape)
    image = matched_image

    if fig2 is not None:
        fig2.clf()
        fig2 = None
        ax2 = None
        ax3 = None
        canvas_widget2.get_tk_widget().destroy()
        canvas_widget2 = None
        if slider2 is not None:
            slider2.destroy()
            slider2 = None
            set_value_button2.destroy()
            set_value_button2 = None
            slider_value_entry2.destroy()
            slider_value_entry2 = None
    
    fig2, ax2 = plt.subplots()
    ax2.hist(matched_image.flatten(), 100)
    ax2.hist(reference_image.flatten(), 100, alpha=0.5)

    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

############################################################################################################
#Denoise methods
def mean_filter(canva,axis, window):
  global image
  filtered_image_data = np.zeros_like(image)
  for x in range(1, image.shape[0]-2) :
    for y in range(1, image.shape[1]-2) :
      for z in range(1, image.shape[2]-2) :
        avg = 0
        for dx in range(-1, 1) :
          for dy in range(-1, 1) :
            for dz in range(-1, 1) :
              avg = avg + image[x+dx, y+dy, z+dz]

        filtered_image_data[x+1, y+1, z+1] = avg / 27
  show_image(image, filtered_image_data,canva,axis,window)
  image = filtered_image_data

def median_filter(canva,axis,window):
    global image
    filtered_image_data = np.zeros_like(image)
    for x in range(1, image.shape[0]-2) :
        for y in range(1, image.shape[1]-2) :
            for z in range(1, image.shape[2]-2) :
                neightbours = []
                for dx in range(-1, 1) :
                    for dy in range(-1, 1) :
                        for dz in range(-1, 1) :
                            neightbours.append(image[x+dx, y+dy, z+dz])

                median = np.median(neightbours)
                filtered_image_data[x+1, y+1, z+1] = median
    show_image(image, filtered_image_data, canva, axis, window)
    image = filtered_image_data

def edge_filter(canva, axis, window):
    global image
    # Median Filter with borders
    filtered_image_data = np.zeros_like(image)

    threshold = float(input("Ingrese el valor del umbral: "))

    for x in range(1, image.shape[0]-2):
        for y in range(1, image.shape[1]-2):
            for z in range(1, image.shape[2]-2):
                # Compute the derivatives in x, y, and z directions
                dx = image[x+1, y, z] - image[x-1, y, z]
                dy = image[x, y+1, z] - image[x, y-1, z]
                dz = image[x, y, z+1] - image[x, y, z-1]

                # Compute the magnitude of the gradient
                magnitude = np.sqrt(dx*dx + dy*dy + dz*dz)
           
                # Compute the threshold using a fraction of the standard deviation
                below_threshold = magnitude[magnitude < threshold]
                above_threshold = magnitude[magnitude >= threshold]

                if below_threshold.size > 0 and above_threshold.size > 0:
                    # Calculate the new threshold as the average of below_threshold and above_threshold
                    threshold = (np.mean(below_threshold) + np.mean(above_threshold)) / 2
                elif below_threshold.size > 0:
                    threshold = np.mean(below_threshold)
                elif above_threshold.size > 0:
                    threshold = np.mean(above_threshold)
                else:
                    threshold = threshold

                # Calculate the new threshold as the average of below_threshold and above_threshold
                # threshold = (np.mean(below_threshold) + np.mean(above_threshold)) / 2
                # If the magnitude is below the threshold, apply median filter
                if magnitude < threshold:
                    neighbours = []
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            for dz in range(-1, 2):
                                neighbours.append(image[x+dx, y+dy, z+dz])
                    median = np.median(neighbours)
                    filtered_image_data[x, y, z] = median
                else:
                    filtered_image_data[x, y, z] = image[x, y, z]
    
    show_image(image, filtered_image_data, canva, axis, window)
    image = filtered_image_data

######################################################################################################################
#REGISTRATION

def rigid_register():
    fixed_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "FLAIR.nii.gz")])
    segmented_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
    global path
    #Load Images
    fixed_image = sitk.ReadImage(fixed_path)
    segmented_image = sitk.ReadImage(segmented_path)
    moving_image = sitk.ReadImage(path)

    #Convert image types
    fixed_image = sitk.Cast(fixed_image, sitk.sitkFloat32)
    moving_image = sitk.Cast(moving_image, sitk.sitkFloat32)
    segmented_image = sitk.Cast(segmented_image, sitk.sitkFloat32)

    # Define the registration components
    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric - Mutual Information
    registration_method.SetMetricAsMattesMutualInformation()

    # Interpolator
    registration_method.SetInterpolator(sitk.sitkNearestNeighbor)

    # Optimizer - Gradient Descent
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100,
                                                     estimateLearningRate=registration_method.EachIteration)

    # Initial transform - Identity
    initial_transform = sitk.Transform()
    registration_method.SetInitialTransform(initial_transform)

    # Setup for the registration process
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Perform registration
    final_transform = registration_method.Execute(fixed_image, segmented_image)

    # Apply the final transformation to the moving image
    registered_image = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkNearestNeighbor, 0.0, fixed_image.GetPixelID())

    # Save the registered image as NIfTI
    # Verificar si el archivo existe
    if os.path.exists("Registration/registered_img.nii.gz"):
        # Borrar el archivo existente
        os.remove("Registration/registered_img.nii.gz")
    sitk.WriteImage(registered_image, "Registration/registered_img.nii.gz")

    # Crear una ventana
    window = ctk.CTkToplevel()
    screen_width = 1920
    screen_height = 1080
    #Set window dimensions
    window_width = int(screen_width * 0.2)
    window_height = int(screen_height*0.05)
    #Position
    x = int(screen_width*0.25)
    y = int(screen_height*0.25)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Definir el mensaje que se mostrará
    mensaje = "Se ha registrado la imagen con exito"

    # Crear un widget Label para mostrar el mensaje
    label = ctk.CTkLabel(window, text=mensaje)
    label.pack()

    # Mostrar la ventana
    window.mainloop()
