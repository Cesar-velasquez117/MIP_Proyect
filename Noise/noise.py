import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def mean_filter(path, canva):
  img_data = nib.load(path).get_fdata()
  filtered_image_data = np.zeros_like(img_data)
  for x in range(1, img_data.shape[0]-2) :
    for y in range(1, img_data.shape[1]-2) :
      for z in range(1, img_data.shape[2]-2) :
        avg = 0
        for dx in range(-1, 1) :
          for dy in range(-1, 1) :
            for dz in range(-1, 1) :
              avg = avg + img_data[x+dx, y+dy, z+dz]

        filtered_image_data[x+1, y+1, z+1] = avg / 27