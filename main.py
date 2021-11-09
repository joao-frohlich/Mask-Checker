import tkinter as tk
from PIL import ImageTk, Image
import cv2 as cv
import numpy as np
import json
import os
from tkinter import filedialog as fd
import annotationView

root = tk.Tk()
root.geometry("600x180")
root.configure(padx=20, pady=20, bg='#1c1c1c')
root.title("Fix annotations")

json_path = ''
images_path = ''

def search_json():
    global json_path
    json_path = fd.askopenfilename(initialdir='~', title="Select the JSON file", filetypes=(("JSON files","*.json"), ("All Files", "*")))
    global label
    if json_path != '':
        label.grid_forget()
        label = tk.Label(root, text=json_path, bg='#1c1c1c', fg="#c1c1c1", padx=5, pady=5)
        label.grid(row=0,column=1, padx=5)

def search_folder():
    global images_path
    images_path = fd.askdirectory(initialdir='~', title="Select the Images folder")
    global label2
    if images_path != '':
        label2.grid_forget()
        label2 = tk.Label(root, text=images_path, bg='#1c1c1c', fg="#c1c1c1", padx=5, pady=5)
        label2.grid(row=1, column=1, padx=5, pady=20)

open_file_button = tk.Button(
    root,
    text="Select JSON",
    bg='#1c1c1c',
    fg="#c1c1c1",
    activebackground="#3c3c3c",
    command=search_json,
    padx=5,
    pady=5,
    width=17
)
open_file_button.grid(row=0,column=0, padx=5)

label = tk.Label(
    root,
    text="No File Selected",
    bg='#1c1c1c',
    fg="#c1c1c1",
    padx=5,
    pady=5
)
label.grid(row=0, column=1, padx=5)

open_folder_button = tk.Button(
    root,
    text="Select Image Folder",
    bg='#1c1c1c',
    fg="#c1c1c1",
    activebackground="#3c3c3c",
    command=search_folder,
    padx=5,
    pady=5,
    width=17
)
open_folder_button.grid(row=1, column=0, padx=5, pady=20)

label2 = tk.Label(
    root,
    text="No Folder Selected",
    bg='#1c1c1c',
    fg="#c1c1c1",
    padx=5,
    pady=5
)
label2.grid(row=1, column=1, padx=5, pady=20)

def redirect(tmp_window, img_path, js_path):
    global entry
    aux = entry.get()
    if aux.isnumeric():
        image_id = int(aux)
        if (image_id <= 0):
            image_id = 1
    else:
        image_id = 1
    tmp_window.destroy()
    annotationView.annotation_view(img_path, js_path, image_id, root)


def call_annotation_view(tmp_img, tmp_json):
    if True:
    # if tmp_img != '' and tmp_json != '':
        if tmp_img == '':
            tmp_img = '/home/paulo/Área de Trabalho/PLDs'
        if tmp_json == '':
            tmp_json = '/home/paulo/Área de Trabalho/PLDs/qridr.json'

        tmp_window = tk.Toplevel()
        tmp_window.configure(padx = 20, pady = 20, bg = "#1c1c1c")
        label3 = tk.Label(tmp_window, text = "Insert image id", bg="#1c1c1c", fg="#c1c1c1")
        label3.grid(row=0,column=0,padx=10)
        global entry
        entry = tk.Entry(tmp_window)
        entry.grid(row=0, column=1)
        confirm_button = tk.Button(tmp_window, text = "Confirm", bg="#1c1c1c", fg="#c1c1c1", activebackground = "#3c3c3c", command = lambda:redirect(tmp_window,tmp_img,tmp_json))
        confirm_button.grid(row=1, column=0, pady=10)
        tmp_window.bind("<Return>", lambda x: redirect(tmp_window,tmp_img,tmp_json))
    else:
        print("Error, paths not defined")

start_annotation_button = tk.Button(
    root,
    text="Start Annotation",
    bg='#1c1c1c',
    fg="#c1c1c1",
    command = lambda: call_annotation_view(images_path, json_path),
    activebackground="#3c3c3c",
    padx=5,
    pady=5,
    width=17
)
start_annotation_button.grid(row=2,column=0)

root.bind("<Control-j>", lambda x: search_json())
root.bind("<Control-m>", lambda x: search_folder())

root.mainloop()
