import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

image_path='D:/Procesamiento de Imagenes/MIP_Proyect/Images/4/FLAIR.nii.gz'
image_data = nib.load(image_path)
image = image_data.get_fdata()

x=1
y=1
z=1

tol = 4
mean_cluster = image[x,y,z]
segmentation = np.zeros_like(image)

#perform region growing
while True:
    voxels_added = 0
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            for dz in [-1,0,1]:
                # skip the voxel if its already in the segmentation
                if segmentation[x+dx, y+dy, z+dz] != 0:
                    continue

                # add the voxel to the segmentation if its within the tolerance
                if np.abs(mean_cluster - image[x+dx, y+dy, z+dz]) < tol:
                    segmentation[x+dx, y+dy, z+dz] = 1
                    voxels_added += 1
    
    # if no voxels were added on this iteration, stop the loop
    if voxels_added == 0:
        break

    # recalculate the mean value of the segmented region
    mean_cluster = image[segmentation == 1].mean()

#Show image
plt.imshow(segmentation[:,:,2])
#Show histogram
#plt.hist(image.flatten(), 50)
plt.show()