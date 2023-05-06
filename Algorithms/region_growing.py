import tkinter
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def region_img(path, tolerance, origin_x, origin_y ,origin_z, axis, axis_value):
    image_data = nib.load(path)
    image = image_data.get_fdata()

    x = 1
    y = 1
    z = 1
    valor_medio_cluster = image[origin_x, origin_y, 20]
    segmentation = np.zeros_like(image)
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
              if np.abs(valor_medio_cluster - image[punto[0]+dx, punto[1]+dy, 20]) < tolerance :
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

    if (axis == "x"):
        plt.imshow(segmentation[axis_value,:,:])
    elif (axis == "y"):
        plt.imshow(segmentation[:,axis_value,:])
    elif (axis == "z"):
        plt.imshow(segmentation[:,:,axis_value])
    #Show histogram
    #plt.hist(image.flatten(), 50)
    plt.show()

def region_form(path, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tol=float(tolerance_entry.get())
        x = int(x_entry.get())
        y = int(y_entry.get())
        z = int(z_entry.get())

        region_img(path,tol,x,y,z,axis,axis_value)

        top.destroy()

    top = tkinter.Toplevel()
    top.title("Region Growing Form")
    top.grab_set() #Block the main window
    top.protocol("WM_DELETE_WINDOW", lambda: top.destroy())
    #Get screen dimensions
    screen_width = 1920
    screen_height = 1080
    #Set window dimensions
    top_width = int(screen_width * 0.25)
    top_height = int(screen_height*0.3)
    #Position
    top_x = int(screen_width/3)
    top_y = int(screen_height/4)
    top.geometry(f"{top_width}x{top_height}+{top_x}+{top_y}")

    #Label
    title_label = tkinter.Label(top, text="Region Growing Form", font=("Times New Roman", 15, "bold"))
    tolerance_label = tkinter.Label(top, text="Tolerance: ", font=("Times New Roman", 15, "bold"))
    seed_label = tkinter.Label(top, text="Seed: ", font=("Times New Roman", 15, "bold"))
    x_label = tkinter.Label(top, text="X: ", font=("Times New Roman", 15, "bold"))
    y_label = tkinter.Label(top, text="Y: ", font=("Times New Roman", 15, "bold"))
    z_label = tkinter.Label(top, text="Z: ", font=("Times New Roman", 15, "bold"))
    #Textfield
    tolerance_entry = tkinter.Entry(top, width=20, text="tolerance")
    x_entry = tkinter.Entry(top, width=10)
    y_entry = tkinter.Entry(top, width=10)
    z_entry = tkinter.Entry(top, width=10)

    #Button
    finish_button = tkinter.Button(top, text="Finish Form", width=20, height=2, command=finish_form)

    #Pack
    title_label.place(x=top_width/2, y=10, anchor="n")
    tolerance_label.place(x=top_width*0.1, y=70, anchor="w")
    seed_label.place(x=top_width*0.1, y=100, anchor="w")
    x_label.place(x=top_width*0.1, y=130, anchor="w")
    y_label.place(x=top_width*0.1, y=150, anchor="w")
    z_label.place(x=top_width*0.1, y=170, anchor="w")
    tolerance_entry.place(x=top_width*0.4, y=70, anchor="w")
    x_entry.place(x=top_width*0.4, y=130, anchor="w")
    y_entry.place(x=top_width*0.4, y=150, anchor="w")
    z_entry.place(x=top_width*0.4, y=170, anchor="w")
    finish_button.place(x=top_width/2, y= 200, anchor="n")

    top.mainloop()

if __name__ == '__main__':
   region_form()