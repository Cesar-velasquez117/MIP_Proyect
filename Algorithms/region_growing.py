import tkinter
import customtkinter as ctk
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

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def on_validate_float(new_value):
    if new_value.strip() == "":
        return True
    return is_float(new_value)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def on_validate_int(new_value):
    if new_value.strip() == "":
        return True
    return is_int(new_value)

def region_form(path, axis, axis_value):
    #Gets the values for the thresholding algorithm
    def finish_form():
        tol=float(tolerance_entry.get())
        x = int(x_entry.get())
        y = int(y_entry.get())
        z = int(z_entry.get())

        region_img(path,tol,x,y,z,axis,axis_value)

        tolerance_entry.delete(0, tkinter.END)
        x_entry.delete(0, tkinter.END)
        y_entry.delete(0, tkinter.END)
        z_entry.delete(0, tkinter.END)

        top.destroy()

    top = ctk.CTkToplevel()
    top.title("Region Growing Form")
    top.grab_set() #Block the main window
    top.protocol("WM_DELETE_WINDOW", lambda: top.destroy())
    #Get screen dimensions
    screen_width = 1920
    screen_height = 1080
    #Set window dimensions
    top_width = int(screen_width * 0.25)
    top_height = int(screen_height*0.4)
    #Position
    top_x = int(screen_width/3)
    top_y = int(screen_height/4)
    top.geometry(f"{top_width}x{top_height}+{top_x}+{top_y}")

    #Frame
    form_frame = ctk.CTkFrame(top, width=top_width*0.8, height=top_height*0.8)

    #Label
    title_label = ctk.CTkLabel(form_frame, text="Region Growing Form", font=("Times New Roman", 20, "bold"))
    tolerance_label = ctk.CTkLabel(form_frame, text="Tolerance: ", font=("Times New Roman", 20, "bold"))
    seed_label = ctk.CTkLabel(form_frame, text="Seed: ", font=("Times New Roman", 20, "bold"))
    x_label = ctk.CTkLabel(form_frame, text="X: ", font=("Times New Roman", 20, "bold"))
    y_label = ctk.CTkLabel(form_frame, text="Y: ", font=("Times New Roman", 20, "bold"))
    z_label = ctk.CTkLabel(form_frame, text="Z: ", font=("Times New Roman", 20, "bold"))
    #Textfield
    tolerance_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    tolerance_entry.configure(validatecommand=(top.register(on_validate_float), '%P'))
    x_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    x_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    y_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    y_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))
    z_entry = ctk.CTkEntry(form_frame, width=140, validate="key")
    z_entry.configure(validatecommand=(top.register(on_validate_int), '%P'))

    #Button
    finish_button = ctk.CTkButton(form_frame, text="Finish Form", width=50, height=30, command=finish_form)

    #Pack
    form_frame.place(relx=0.5, rely=0.5, anchor="c")
    title_label.place(relx=0.5, rely=0.1, anchor="n")
    tolerance_label.place(relx=0.2, rely=0.3, anchor="w")
    seed_label.place(relx=0.2, rely=0.4, anchor="w")
    x_label.place(relx=0.2, rely=0.5, anchor="w")
    y_label.place(relx=0.2, rely=0.6, anchor="w")
    z_label.place(relx=0.2, rely=0.7, anchor="w")
    tolerance_entry.place(relx=0.5, rely=0.3, anchor="w")
    x_entry.place(relx=0.5, rely=0.5, anchor="w")
    y_entry.place(relx=0.5, rely=0.6, anchor="w")
    z_entry.place(relx=0.5, rely=0.7, anchor="w")
    finish_button.place(relx=0.5, rely= 0.85, anchor="n")

    top.mainloop()

if __name__ == '__main__':
   region_form()