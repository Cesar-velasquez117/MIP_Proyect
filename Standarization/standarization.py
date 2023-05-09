from scipy.signal import find_peaks
from scipy import stats as st
import statistics as stat
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas_widget2 = None
def rescaling(path, canva):
    global canvas_widget2
    img_data=nib.load(path).get_fdata()
    canva.delete("all")
    min_value = img_data.min()
    max_value = img_data.max()

    img_data_rescaled = (img_data - min_value) / (max_value - min_value)

    #Create a neew figure and plot the histogram
    fig = plt.figure()
    plt.hist(img_data_rescaled[img_data_rescaled>0.01].flatten(),bins=100)

    if canvas_widget2 is None:
        canvas_widget2 = FigureCanvasTkAgg(fig,canva)
        canvas_widget2.get_tk_widget().pack()
    else:    
        canvas_widget2.figure = fig
        canvas_widget2.draw()

def zscore(path, canva):
    global canvas_widget2
    img_data=nib.load(path).get_fdata()
    canva.delete("all")
    mean_value = img_data[img_data>10].mean()
    std_deviation_value = img_data[img_data>10].std()

    img_data_rescaled = (img_data - mean_value) / std_deviation_value

    #Create a neew figure and plot the histogram
    fig = plt.figure()
    plt.hist(img_data_rescaled.flatten(),bins=100)

    if canvas_widget2 is None:
        canvas_widget2 = FigureCanvasTkAgg(fig,canva)
        canvas_widget2.get_tk_widget().pack()
    else:    
        canvas_widget2.figure = fig
        canvas_widget2.draw()

def white_stripe(path,canva):
    global canvas_widget2
    img_data=nib.load(path).get_fdata()
    canva.delete("all")
    #Calcular el histograma
    hist, bin_edges = np.histogram(img_data.flatten(), bins=100)

    #Encontrar picos
    picos, _ = find_peaks(hist, height=100)
    val_picos = bin_edges[picos]

    #Rescalado de la imagen
    img_data_rescaled = img_data/val_picos[1]

    #Mostrar el histograma con los picos identificados
    fig = plt.figure()
    plt.axvline(val_picos[0], color='r', linestyle='--')
    plt.hist(img_data.flatten(), bins=100)
    plt.plot(bin_edges[picos], hist[picos], "x")

    if canvas_widget2 is None:
        canvas_widget2 = FigureCanvasTkAgg(fig,canva)
        canvas_widget2.get_tk_widget().pack()
    else:    
        canvas_widget2.figure = fig
        canvas_widget2.draw()

    

