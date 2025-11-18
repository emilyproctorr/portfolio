# Emily Proctor
# Slusky Lab

# Functionality
    # GUI that displays contact map image and AlphaFold prediction image (previously generated and stored in folders)
    # User has ability to flip forward and backward through all loaded images
    # User has ability to click buttons 'yes', 'maybe', 'no' for each protein
    # User is able to see answer displayed for each protein (yes, maybe, or no)
    # Generates output file containing each protein id along with each user answer per protein
    # Generates index file so user is able to exit program and save position
# Purpose
    # View many proteins and determine if protein is a specific characteristic
    # ex: I personally created and used this program to flip through many number of proteins and determine based off contact map and AlphaFold image, 
        # if protein was predicted beta barrel or not


import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
import os

# create window

window = tk.Tk()
window.geometry("1500x1500")

# contact map images

cmap_ids = [] # XP_044412266_1
cmap_image_list0 = []
for filename in os.listdir("837_seqs/837_cmap_images/"):
    if filename == ".DS_Store":
        continue
    else:
        filename_list = filename.split(".")
        cmap_ids.append(filename_list[0].replace("_CASPmap", ""))
        cmap_image_list0.append(filename)

# af images

af_ids = [] # XP_044323029_1
af_image_list = [] # XP_044406460_1_top_af_prediction.png
for filename in os.listdir("837_seqs/837_af_images/"):
    if filename == ".DS_Store":
        continue
    else:
        filename_list = filename.split(".")
        af_ids.append(filename_list[0].replace("_top_af_prediction", ""))
        af_image_list.append(filename)

# do this so image lists are in same order
cmap_image_list = [] # XP_044435964_1_CASPmap.png
for id in af_ids:
    for image in cmap_image_list0:
        if id in image:
            cmap_image_list.append(image)

# dict to store results

results_dict = {}
try:
    with open("output.txt", "r") as file:
        for line in file:
            line = line.strip().split()
            results_dict[line[0]] = line[1]
    with open("index.txt", "r") as file:
        for line in file:
            index = int(line.strip()) - 1
except:
    for id in af_ids:
        results_dict[id] = None
    index = -1

# protein id and answer label, indexer label

label4 = tk.Label(window, text="", font=("Arial",30))
label4.place(x=10, y=0)

label5 = tk.Label(window, text="", font=("Arial",20))
label5.place(x=10, y=50)

label6 = tk.Label(window, text="", font=("Arial",30))
label6.place(x=515, y=0)

# change imgaes

panel1 = tk.Label(window)
panel1.place(x=10,y=100)

def f_change_image1():
    try:
        global index
        index += 1
        img = cmap_image_list[index]
    except:
        index -= 1
        return

    img = ImageTk.PhotoImage(Image.open(f"837_seqs/837_cmap_images/{img}").resize((500,500)))
    panel1.img = img
    panel1['image'] = img

f_change_image1()

panel2 = tk.Label(window)
panel2.place(x=515,y=100)

current_image = None
def f_change_image2():
    try:
        global index
        img = af_image_list[index]
    except:
        return

    global current_image
    img_list = img.split(".")
    current_image = img_list[0].replace("_top_af_prediction", "")
    img = ImageTk.PhotoImage(Image.open(f"837_seqs/837_af_images/{img}").resize((500,500)))
    panel2.img = img
    panel2['image'] = img

    current_answer = ""
    for id, answer in results_dict.items():
        if id == current_image:
            current_answer = answer
    label4.config(text=f"ID: {current_image}")
    label6.config(text=f"Answer: {current_answer}")

    id_list = list(results_dict.keys())
    id_index = id_list.index(current_image) + 1
    label5.config(text=f"{id_index} of 837")

f_change_image2()

def b_change_image1():
    global index
    index -= 1
    if index < 0:
        index += 1
        return

    b_change_image2()
    img = cmap_image_list[index]

    img = ImageTk.PhotoImage(Image.open(f"837_seqs/837_cmap_images/{img}").resize((500,500)))
    panel1.img = img
    panel1['image'] = img

def b_change_image2():
    global index
    img = af_image_list[index]

    global current_image
    img_list = img.split(".")
    current_image = img_list[0].replace("_top_af_prediction", "")
    img = ImageTk.PhotoImage(Image.open(f"837_seqs/837_af_images/{img}").resize((500,500)))
    panel2.img = img
    panel2['image'] = img

    current_answer = ""
    for id, answer in results_dict.items():
        if id == current_image:
            current_answer = answer
    label4.config(text=f"ID: {current_image}")
    label6.config(text=f"Answer: {current_answer}")

    id_list = list(results_dict.keys())
    id_index = id_list.index(current_image) + 1
    label5.config(text=f"{id_index} of 837")

# count labels

label1 = tk.Label(window, text=0)
label1.place(x=30, y=660)

label2 = tk.Label(window, text=0)
label2.place(x=130, y=660)

label3 = tk.Label(window, text=0)
label3.place(x=230, y=660)

# update data stucture as button is clicked or using key bindings and update counts

yes_count = 0
def store_yes(event):
    global current_image

    results_dict[current_image] = "Yes"

    no_count = 0
    yes_count = 0
    maybe_count = 0
    for id, answer in results_dict.items():
        if answer == "No":
            no_count += 1
        elif answer == "Yes":
            yes_count += 1
        elif answer == "Maybe":
            maybe_count += 1
        else:
            continue

    label3.config(text=no_count)
    label1.config(text=yes_count)
    label2.config(text=maybe_count)

maybe_count = 0
def store_maybe(event):
    global current_image

    results_dict[current_image] = "Maybe"

    no_count = 0
    yes_count = 0
    maybe_count = 0
    for id, answer in results_dict.items():
        if answer == "No":
            no_count += 1
        elif answer == "Yes":
            yes_count += 1
        elif answer == "Maybe":
            maybe_count += 1
        else:
            continue

    label3.config(text=no_count)
    label1.config(text=yes_count)
    label2.config(text=maybe_count)

no_count = 0
def store_no(event):
    global current_image

    results_dict[current_image] = "No"

    no_count = 0
    yes_count = 0
    maybe_count = 0
    for id, answer in results_dict.items():
        if answer == "No":
            no_count += 1
        elif answer == "Yes":
            yes_count += 1
        elif answer == "Maybe":
            maybe_count += 1
        else:
            continue

    label3.config(text=no_count)
    label1.config(text=yes_count)
    label2.config(text=maybe_count)


# button click, call all functions

def yes_button(event):
    store_yes(event)
    f_change_image1()
    f_change_image2()

def maybe_button(event):
    store_maybe(event)
    f_change_image1()
    f_change_image2()

def no_button(event):
    store_no(event)
    f_change_image1()
    f_change_image2()

def forward_image(event):
    f_change_image1()
    f_change_image2()

def back_image(event):
    b_change_image1()

# buttons

button1 = tk.Button(window, text="Yes", width=4, height=1, command=lambda:yes_button(button1))
button1.place(x=0, y=630)

button2 = tk.Button(window, text="Maybe", width=5, height=1, command=lambda:maybe_button(button2))
button2.place(x=100, y=630)

button3 = tk.Button(window, text="No", width=4, height=1, command=lambda:no_button(button3))
button3.place(x=200, y=630)

# key bindinds

window.bind("<a>", yes_button)
window.bind("<s>", maybe_button)
window.bind("<d>", no_button)
window.bind("<Right>", forward_image)
window.bind("<Left>", back_image)

# exit and save

def save_and_exit():
    global index
    with open("index.txt", "w") as index_file:
        index_file.write(str(index))
    with open("output.txt", "w") as output_file:
        for protein, answer in results_dict.items():
            output_file.write(f"{protein} {answer}\n")
    window.destroy()

exit_button = tk.Button(window, text="Save and Exit", command=save_and_exit)
exit_button.place(x=0, y=700)

window.protocol("WM_DELETE_WINDOW", save_and_exit)

# execute window

window.mainloop()
