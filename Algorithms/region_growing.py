import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

image_path='D:/Procesamiento de Imagenes/MIP_Proyect/Images/4/FLAIR.nii.gz'
image_data = nib.load(image_path)
image = image_data.get_fdata()

origin_x = 100
origin_y = 100
origin_z = 1
x = 1
y = 1
z = 1
valor_medio_cluster = image[origin_x, origin_y, 20]
tol = 50
segmentation = np.zeros_like(image)
itera = 1
point = [origin_x,origin_y]
tail = [point]
evaluated=[]
while True:
  punto = tail.pop(0)

  print(len(tail))
  
  for dx in [-x, 0, x] :
    for dy in [-y, 0, y] :
      if((punto[0]+dx < 230) and ((punto[0]+dx) > 0) and (punto[1]+dy < 230) and ((punto[1]+dy) > 0) ):
        if ([punto[0]+dx, punto[1]+dy] not in(evaluated)):
          if np.abs(valor_medio_cluster - image[punto[0]+dx, punto[1]+dy, 20]) < tol :
              segmentation[punto[0]+dx, punto[1]+dy, 20] = 1
              tail.append([punto[0]+dx, punto[1]+dy])
              evaluated.append([punto[0]+dx, punto[1]+dy])
          else :
              segmentation[punto[0]+dx, punto[1]+dy, 20] = 0
              tail.append([punto[0]+dx, punto[1]+dy])
              evaluated.append([punto[0]+dx, punto[1]+dy])

  valor_medio_cluster = image[segmentation == 1].mean()

  

  # x += 1
  # y += 1
  # z += 1
  if len(tail) == 0:
    break

#Show image
plt.imshow(segmentation[:,:,20])
#Show histogram
#plt.hist(image.flatten(), 50)
plt.show()