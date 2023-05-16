from scipy.signal import find_peaks
import nibabel as nib
import matplotlib.pyplot as plt
import os
import numpy as np
import customtkinter as ctk
import tkinter
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
#Auxiliary functions
def load_image(file_path):
    filename = os.path.basename(file_path)
    extension = os.path.splitext(filename)[0]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Ruta absoluta del directorio del script actual
    if (extension == "FLAIR.nii"):
        sample_image = nib.load(os.path.join(base_dir, "Image", "Base_Img", "FLAIR.nii.gz")).get_fdata()
        # procesamiento para FLAIR
    elif (extension == "IR.nii"):
        sample_image = nib.load(os.path.join(base_dir, "Image", "Base_Img", "IR.nii.gz")).get_fdata()
        # procesamiento para IR
    elif (extension == "T1.nii"):
        sample_image = nib.load(os.path.join(base_dir, "Image", "Base_Img", "T1.nii.gz")).get_fdata()
        # procesamiento para T1
    else:
        raise ValueError("Tipo de imagen no soportado")
    return sample_image

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
    sample_image = load_image(path)
    canva.delete("all")
    min_value = image.min()
    max_value = image.max()
    min_sample_value = sample_image.min()
    max_sample_value = sample_image.max()

    img_data_rescaled = (image - min_value) / (max_value - min_value)
    sample_image_rescaled = (sample_image - min_sample_value) / (max_sample_value - min_sample_value)
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
        
    ax2.hist(sample_image_rescaled[sample_image_rescaled >0.01].flatten(), 100)
    ax2.hist(img_data_rescaled[img_data_rescaled>0.01].flatten(),bins=100, alpha=0.7)
    #Medidas originales (640,480)
    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

def zscore(canva):
    global canvas_widget2, fig2, ax2, ax3, image, path, slider2, set_value_button2, slider_value_entry2
    sample_image = load_image(path)
    canva.delete("all")
    mean_value = image[image>10].mean()
    std_deviation_value = image[image>10].std()
    mean_sample_value = sample_image[sample_image>10].mean()
    std_deviation_sample_value = sample_image[sample_image>10].std()

    img_data_rescaled = (image - mean_value) / std_deviation_value
    sample_image_rescaled = (sample_image - mean_sample_value) / std_deviation_sample_value
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
    ax2.hist(sample_image_rescaled.flatten(), 100)
    ax2.hist(img_data_rescaled.flatten(),bins=100, alpha=0.7)

    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

def white_stripe(canva):
    global canvas_widget2, fig2, ax2, ax3, image, path, slider2, set_value_button2, slider_value_entry2
    sample_image = load_image(path)
    canva.delete("all")
    #Calcular el histograma
    hist, bin_edges = np.histogram(image.flatten(), bins=100)
    sample_hist, sample_bin_edges = np.histogram(sample_image.flatten(), bins=100)
    #Encontrar picos
    peaks, _ = find_peaks(hist, height=100)
    val_peaks = bin_edges[peaks]
    sample_peaks, sample_ = find_peaks(sample_hist, height=100)
    val_sample_peaks = sample_bin_edges[sample_peaks]

    #Rescalado de la imagen
    img_data_rescaled = image/val_peaks[1]
    sample_image_rescaled = sample_image/val_sample_peaks[1]
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
    ax2.hist(sample_image_rescaled.flatten(), 100)
    ax2.hist(img_data_rescaled.flatten(), 100, alpha = 0.7)
    #ax2.axvline(val_peaks[0], color='r', linestyle='--')
    #ax2.hist(image.flatten(), bins=100)
    #ax2.plot(bin_edges[peaks], hist[peaks], "x")

    canvas_widget2 = FigureCanvasTkAgg(fig2,canva)
    canvas_widget2.get_tk_widget().configure(width=600, height=450)
    canvas_widget2.get_tk_widget().pack()

def hist_matching(canva):
    global canvas_widget2, fig2, ax2, ax3, image, slider2, set_value_button2, slider_value_entry2
    file_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
    reference_image = nib.load(file_path).get_fdata()

    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    ref_hist, ref_bins = np.histogram(reference_image.flatten(), 256, [0, 256])

    hist_cdf = hist.cumsum()
    hist_cdf_normalized = hist_cdf / hist_cdf.max()
    ref_hist_cdf = ref_hist.cumsum()
    ref_hist_cdf_normalized = ref_hist_cdf / ref_hist_cdf.max()

    #Compute the mapping function that matches the CDFs of the input and reference images
    mapping = np.interp(hist_cdf_normalized, ref_hist_cdf_normalized, ref_bins[:-1])

    #Apply the mapping function to the input image
    matched_image = np.interp(image.flatten(), bins[:-1], mapping)
    #matched_image.reshape(image.shape).astype('uint8')
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

    #threshold = 500

    # Estimate the standard deviation of the pixel intensity
    std = np.std(image)

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
                threshold = 3 * std

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