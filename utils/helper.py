import customtkinter as ctk
import numpy as np
import SimpleITK as sitk
import os
import nibabel as nib
import matplotlib.pyplot as plt
from scipy import ndimage
from tkinter import filedialog
from PIL import Image
from Classes.SlidePanel import SlidePanel
from Preprocessing.methods import rescaling, zscore, white_stripe, mean_filter, median_filter, edge_filter, hist_matching
from Algorithms.methods import k_form, region_form, thresholding_form, gaussian_form

#Function to add the sidebar to the window
def add_sidebar(window, window2):
    sidebar = SlidePanel(window, 0, -0.2)
    if window.title() == "Prepocessing": 
        preprocess_button =  ctk.CTkButton(sidebar, text="Preprocessing Methods", width=140, height=30, command=lambda: show_window(window2,window), state="disabled")
        processing_button = ctk.CTkButton(sidebar, text="Processing Methods", width=140, height=30, command=lambda: processing(window2, window))
    else:
        preprocess_button =  ctk.CTkButton(sidebar, text="Go to Preprocessing", width=140, height=30, command=lambda: show_window(window,window2))
        processing_button = ctk.CTkButton(sidebar, text="Processing Methods", width=140, height=30, command=lambda: processing(window, window2), state="disabled")
    volume_button = ctk.CTkButton(sidebar, text="Calculate Volumes", width=140, height=30 )
    sidebar_img = ctk.CTkImage(light_image=Image.open("Image/sidebar.png"),dark_image=Image.open("Image/sidebar.png"),size=(50,50))
    sidebar_button = ctk.CTkButton(window, width=50,text="", image=sidebar_img, command=sidebar.animate, fg_color="transparent", hover_color="lightgray", anchor="w")
    #Sidebar elements
    sidebar_button.place(relx=0,rely=0, anchor="nw")
    processing_button.place(relx=0.5, rely=0.1, anchor="c")
    preprocess_button.place(relx=0.5, rely=0.2, anchor="c")
    volume_button.place(relx=0.5, rely=0.3, anchor="c")

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

#Function to browse the image_file
def browse_file(label, list, combobox, combobox2):
    file_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
    if file_path:
      if file_path not in list:
          label.configure(text=file_path)
          list.append(file_path)
          #Updates the values in the Combo box
          combobox.configure(values=list)
          combobox2.configure(values=list)
      else:
          label.configure(text="This file was already uploaded")

#Function to go back to the Preprocessing window
def show_window(window,window2):
    window.withdraw()
    window2.deiconify()
#Function to go to the Processing window
def processing(window, window2):
    window2.withdraw()
    window.deiconify()
#Function to close the app
def on_closing(window):
    window.destroy()
    window.quit()

def option_clicked(image, option, axis, axis_value):
    selected_option = option.get()
    if selected_option == "thresholding":
        thresholding_form(image, axis, axis_value)
    
    if selected_option == "region growing":
        region_form(image, axis, axis_value)

    if selected_option == "k-means":
        k_form(image, axis, axis_value)
    if selected_option == "gaussian mixtures model":
        gaussian_form(image, axis, axis_value)

#Function to show the histogram with the selected standarization method
def method_clicked(option,canva):
    selected_option = option.get()
    if selected_option == "rescaling":
        rescaling(canva)
    if selected_option == "z-score":
        zscore(canva)
    if selected_option == "white-stripe":
        white_stripe(canva)
    if selected_option == "histogram-matching":
        hist_matching(canva)
    
def denoise_clicked(option, combobox2,canva,window):
    selected_option = option.get()
    axis = combobox2.get()
    if selected_option == "mean-filter":
        mean_filter(canva,axis,window)
    if selected_option == "median-filter":
        median_filter(canva, axis, window)
    if selected_option == "edge-filter":
        edge_filter(canva, axis, window)

def borders(image):
    dfdx = np.zeros_like(image)
    dfdy = np.zeros_like(image)
    dfdz = np.zeros_like(image)
    for x in range(1, image.shape[0]-2) :
        for y in range(1, image.shape[1]-2) :
            for z in range(1, image.shape[2]-2) :
                dfdx[x, y, z] = image[x+1, y, z]-image[x-1, y, z]
                dfdy[x, y, z] = image[x, y+1, z]-image[x, y-1, z]
                dfdz[x, y, z] = image[x, y, z+1]-image[x, y, z-1]
    
    magnitud = np.sqrt(np.power(dfdx, 2) + np.power(dfdy, 2) + np.power(dfdz, 2))
    return magnitud

def k_means(image, iterations, k):
    # initialize centroids
    centroids = np.linspace(np.amin(image), np.amax(image), k)
    for i in range(iterations):
        distance = np.abs(image[..., np.newaxis] - centroids)
        segmentation = np.argmin(distance, axis=-1)

        for id in range(k):
            centroids[id] = image[segmentation == id].mean()
    return segmentation
def remove_skull():
    if (os.path.exists('Registration/IR_registered_img.nii.gz') and os.path.exists('Registration/T1_registered_img.nii.gz')):
        #Load IR image
        img = nib.load('Registration/IR_registered_img.nii.gz')

        #Get data
        data = img.get_fdata()

        #Definicion de las escalas espaciales
        scales = [7.5] #Escalas para aplicar filtros

        #Aplicar filtros gaussianos en diferentes escalas
        filtered_imgs = []
        for scale in scales:
            #Aplicacion del filtro gaussiano
            filtered = ndimage.gaussian_filter(data, sigma=scale)
            filtered = k_means(filtered, 10, 2)
            extracted_brain = nib.Nifti1Image(filtered, img.affine, dtype=np.int16)

            #Guardar la imagen con el cerebro extraido
            nib.save(extracted_brain, 'Skull/IR_skull.nii.gz')
            filtered_imgs.append(filtered)

        #Restar Imagen
        #Cargar imagenes FLAIR e IR(sin craneo)
        original_img = sitk.ReadImage('Registration/T1_registered_img.nii.gz')
        reference_img = sitk.ReadImage('Skull/IR_skull.nii.gz')

        #Realizar segmentacion basada en un umbral adaptativo
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(1)
        otsu_filter.SetOutsideValue(0)
        ref_mask = otsu_filter.Execute(reference_img)

        # Apply mask to the original image
        img_without_skull = sitk.Mask(original_img, ref_mask)

        # Get data from the image without skull
        data_skull = sitk.GetArrayFromImage(img_without_skull)

        # Get data from mask
        mask_data = sitk.GetArrayFromImage(ref_mask)

        # Create bool mask for 0 values inside the brain
        mask_brain_cero =  (data_skull == 0) & (mask_data != 0)
        
        # Asign a diferent value to values diferent from 0 inside the brain
        new_value = np.max(original_img) + 1
        data_skull[mask_brain_cero] = new_value

        # Create new SimpleITK image with modified data
        img_without_skull_modified = sitk.GetImageFromArray(data_skull)
        img_without_skull_modified.CopyInformation(img_without_skull)

        # Save Image without 
        sitk.WriteImage(img_without_skull_modified, 'Skull/FLAIR_skull.nii.gz')
