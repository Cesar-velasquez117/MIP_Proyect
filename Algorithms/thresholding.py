import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

image_path='D:/Procesamiento de Imagenes/MIP_Proyect/Images/4/T1.nii.gz'
image_data = nib.load(image_path)
image = image_data.get_fdata()

tol = 1
tau = 150

while True:
    segmentation = image >= tau
    mBG = image[np.multiply(image > 10, segmentation == 0)].mean()
    mFG = image[np.multiply(image > 10, segmentation == 1)].mean()
    
    post_tau = 0.5 * (mBG + mFG)

    if np.abs(tau-post_tau) < tol:
        break
    else:
        tau = post_tau

#Show image
plt.imshow(segmentation[:,:,100])
#Show histogram
#plt.hist(image.flatten(), 50)
plt.show()