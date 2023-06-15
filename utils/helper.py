import customtkinter as ctk
import numpy as np
import SimpleITK as sitk
import os
import nibabel as nib
import matplotlib.pyplot as plt
from scipy import ndimage
from tkinter import filedialog, messagebox, Listbox
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
    listbox = Listbox(sidebar, width=30)
    volume_button = ctk.CTkButton(sidebar, text="Calculate Volumes", width=140, height=30, command=lambda: calculate_volume(listbox) )
    volume_label = ctk.CTkLabel(sidebar, text="Voxel Count", font=("Times New Roman", 20, "bold"))
    sidebar_img = ctk.CTkImage(light_image=Image.open("Image/sidebar.png"),dark_image=Image.open("Image/sidebar.png"),size=(50,50))
    sidebar_button = ctk.CTkButton(window, width=50,text="", image=sidebar_img, command=sidebar.animate, fg_color="transparent", hover_color="lightgray", anchor="w")
    #Sidebar elements
    sidebar_button.place(relx=0,rely=0, anchor="nw")
    processing_button.place(relx=0.5, rely=0.1, anchor="c")
    preprocess_button.place(relx=0.5, rely=0.2, anchor="c")
    volume_button.place(relx=0.5, rely=0.3, anchor="c")
    volume_label.place(relx=0.5, rely=0.5, anchor="c")
    listbox.place(relx=0.5, rely=0.7, anchor="c")

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
    centroids = np.linspace(np.amin(image), np.amax(image), num=k)
    for i in range(iterations):
        distance = np.abs(image[..., np.newaxis] - centroids)
        segmentation = np.argmin(distance, axis=-1)

        for id in range(k):
            centroids[id] = image[segmentation == id].mean()
    return segmentation

def Median_borders(image):
    # Median Filter with borders
    filtered_image_data = np.zeros_like(image)

    threshold = 100

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

                # Calculate the new threshold as the average of below_threshold and above_threshold
                threshold = (np.mean(below_threshold) + np.mean(above_threshold)) / 2
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
     
    return filtered_image_data

def remove_skull(path):
    if (os.path.exists('Registration/IR_registered_img.nii.gz')and os.path.exists('Registration/T1_registered_img.nii.gz') ):
        # Cargar la imagen NIfTI

        nifti_img = nib.load(
        "Registration/IR_registered_img.nii.gz")
        # Asegúrate de ajustar la ruta y el nombre del archivo

        # Obtener los datos de la imagen
        data = nifti_img.get_fdata()

        # Definir escalas espaciales
        scales = [7.5]  # Escalas para aplicar filtros gaussianos

        # Aplicar filtros gaussianos en diferentes escalas
        filtered_images = []
        for scale in scales:
            # Aplicar filtro gaussiano
            filtered = ndimage.gaussian_filter(data, sigma=scale)
            filtered = k_means(filtered, 2,15)
            # Crear una nueva imagen nibabel con el cerebro extraído
            brain_extracted_image = nib.Nifti1Image(
            filtered, affine=nifti_img.affine, dtype=np.int16
            )

            # Guardar la imagen con el cerebro extraído en un nuevo archivo
            nib.save(brain_extracted_image,  "Skull/IR_skull.nii.gz")
            filtered_images.append(filtered)

        # RESTAR UNA IMAGEN

        # Cargar las imágenes
        imagen_original = sitk.ReadImage(
        "Registration/T1_registered_img.nii.gz")
    
        imagen_referencia = sitk.ReadImage("Skull/IR_skull.nii.gz")

        # Modify the metadata of image2 to match image1
        imagen_referencia.SetOrigin(imagen_original.GetOrigin())
        imagen_referencia.SetSpacing(imagen_original.GetSpacing())
        imagen_referencia.SetDirection(imagen_original.GetDirection())

        # Realizar segmentación basada en umbral adaptativo
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(1)
        otsu_filter.SetOutsideValue(0)
        mascara_referencia = otsu_filter.Execute(imagen_referencia)

        # Aplicar la máscara a la imagen original
        imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

        # Obtener los datos de la imagen sin el cráneo
        # Obtener los datos de la imagen sin el cráneo
        data_sin_craneo = sitk.GetArrayFromImage(imagen_sin_craneo)

        # Obtener los datos de la máscara
        data_mascara = sitk.GetArrayFromImage(mascara_referencia)

        # Crear una máscara booleana para los valores cero dentro del cerebro
        mascara_cero_cerebro = (data_sin_craneo == 0) & (data_mascara != 0)

        # Asignar un valor distinto a los valores cero dentro del cerebro
        valor_distinto = 4
        data_sin_craneo[mascara_cero_cerebro] = valor_distinto

        # Crear una nueva imagen SimpleITK con los datos modificados
        imagen_sin_craneo_modificada = sitk.GetImageFromArray(data_sin_craneo)
        imagen_sin_craneo_modificada.CopyInformation(imagen_sin_craneo)

        # Guardar la imagen sin el cráneo

        sitk.WriteImage(
            imagen_sin_craneo_modificada,"Skull/FLAIR_skull.nii.gz")

        # ----------------------------------------------------------------------------------
        # Quitar cráneo a FLAIR Original
        # ----------------------------------------------------------------------------------
        # Cargar las imágenes
        imageno= nib.load(path)
        imagenx= nib.load(path).get_fdata()
        imagenx2=Median_borders(imagenx)

        brain_extracted_image = nib.Nifti1Image(
            imagenx2, affine= imageno.affine, dtype=np.int16
            )

            # Guardar la imagen con el cerebro extraído en un nuevo archivo
        nib.save(brain_extracted_image,  "Skull/FLAIR.nii.gz")
        

        imagen_original = sitk.ReadImage("Skull/FLAIR.nii.gz")
        imagen_referencia = sitk.ReadImage("Skull/IR_skull.nii.gz")

        # Realizar segmentación basada en umbral adaptativo
        otsu_filter = sitk.OtsuThresholdImageFilter()
        otsu_filter.SetInsideValue(1)
        otsu_filter.SetOutsideValue(0)
        mascara_referencia = otsu_filter.Execute(imagen_referencia)

        # Aplicar la máscara a la imagen original
        imagen_sin_craneo = sitk.Mask(imagen_original, mascara_referencia)

        # Guardar la imagen sin el cráneo

        sitk.WriteImage(
            imagen_sin_craneo,
           "Skull/original_FLAIR_skull.nii.gz"
        )

        # ----------------------------------------------------------------------------------
        # Segmentar lesiones
        # ----------------------------------------------------------------------------------

        image = nib.load("Skull/FLAIR_skull.nii.gz")
       
        image_data = image.get_fdata()
        image_data_flair_without_skull = nib.load(
        "Skull/original_FLAIR_skull.nii.gz").get_fdata()

        image_data_flair_segmented = k_means(image_data_flair_without_skull, 15, 15)

        # Where the values are 3, replace them in the image_data with a value of 3
        image_data_flair_segmented[:,:,:13] = 0
        image_data = np.where(image_data_flair_segmented == 6, 3, image_data)

        for z in range(14 - 1, -1, -1):
            image_data[:,:,z] = np.where(image_data[:,:,z] == 3, 0, image_data[:,:,z])

        affine = image.affine
        # Create a nibabel image object from the image data
        image = nib.Nifti1Image(image_data.astype(np.float32), affine=affine)
        # Save the image as a NIfTI file
        output_path = "Skull/FLAIR_skull_lesion.nii.gz"
        nib.save(image, output_path)
        messagebox.showinfo(message="You have created your segmentation map succesfully", title="SUCCESS")

    else:
         messagebox.showerror(message="Images must be registered in Flair format", title="ERROR")

def calculate_volume(listbox):
    lesion_map_path = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii.gz")])
    lesion_image = nib.load(lesion_map_path)
    lesion_data = lesion_image.get_fdata()
    segmented_values = np.unique(lesion_data)
    volumes_mm3 = {}
    volumes = {}
    for value in segmented_values:
        if value !=0:
            volume = np.count_nonzero(lesion_data == value)
            volumes[value] = volume
            voxel_size = np.abs(lesion_image.affine.diagonal()[:3])
            mm3 = volume * np.prod(voxel_size)
            volumes_mm3[value] = mm3
            listbox.insert("end", f"Label {int(value)} : {volume}")
            listbox.insert("end","\n")
    print("Voxeles: ",volumes)
    print("MM3: ", volumes_mm3)
