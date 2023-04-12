import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

image_path='D:/Procesamiento de Imagenes/MIP_Proyect/Images/4/T1.nii.gz'
image_data = nib.load(image_path)
image = image_data.get_fdata()

tol = 1
tau = 150
iterations = 3
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

    if np.abs(k1 - k2) < tol and np.abs(k2-k3) < tol and np.abs(k1-k3) < tol:
        break


#Show image
plt.imshow(segmentation[:,:,100])
#Show histogram
#plt.hist(image.flatten(), 100)
plt.show()