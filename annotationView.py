import tkinter as tk
from PIL import ImageTk, Image
import os
import jsonProcessing
import imageProcessing

def set_image(image_path, image_data, image_id, im_width, im_height, annotationsRectangle):
    global my_image
    global image_frame
    global bg_label
    global res_constraint
    imageProcessing.drawMasks(image_path, '/tmp/aux.jpg', '/tmp/aux2.jpg', annotationsRectangle, image_data)
    w = im_width
    h = im_height
    my_image = ImageTk.PhotoImage(Image.open('/tmp/aux2.jpg').resize((int(res_constraint*(w)),int(res_constraint*(h))), Image.ANTIALIAS))
    bg_label = tk.Label(image_frame, image=my_image)
    bg_label.place(x=0,y=0)
#
def prev_image(num_images):
    global data
    global imgs_path
    global current_image
    global status_frame
    global status_label
    if (current_image > 1):
        current_image-=1
        image_id = current_image
        set_image(imgs_path+'/'+data[image_id]['image_info']['file_name'], data[image_id]['annotations_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'], data[image_id]['image_info']['annotationsRectangle'])
        status_label.forget()
        status_label = tk.Label(
            status_frame,
            text='Image ' + str(current_image) + ' of ' + str(num_images),
            border = 1,
            background = '#1c1c1c',
            foreground = '#c1c1c1',
            highlightbackground = "#c1c1c1",
            highlightcolor = "#c1c1c1",
            highlightthickness = 1,
            anchor = tk.E,
        )
        status_label.pack(expand=True, fill='both')

        global info_label
        info_label = tk.Label(
            status_frame,
            text='Date: ' + str(data[current_image]['image_info']['date'][2])
                + '/' + str(data[current_image]['image_info']['date'][1])
                + '/' + str(data[current_image]['image_info']['date'][0]),
            border = 1,
            background = '#1c1c1c',
            foreground = '#c1c1c1',
            highlightbackground = "#c1c1c1",
            highlightcolor = "#c1c1c1",
            highlightthickness = 1
        )
        info_label.place(x=0, y=0)


def next_image(num_images):
    global data
    global imgs_path
    global current_image
    global status_frame
    global status_label
    if (current_image < num_images+10):
        current_image+=1
        image_id = current_image
        set_image(imgs_path+'/'+data[image_id]['image_info']['file_name'], data[image_id]['annotations_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'], data[image_id]['image_info']['annotationsRectangle'])
        status_label.forget()
        status_label = tk.Label(
            status_frame,
            text='Image ' + str(current_image) + ' of ' + str(num_images),
            border = 1,
            background = '#1c1c1c',
            foreground = '#c1c1c1',
            highlightbackground = "#c1c1c1",
            highlightcolor = "#c1c1c1",
            highlightthickness = 1,
            anchor = tk.E,
        )
        status_label.pack(expand=True, fill='both')

        global info_label
        info_label = tk.Label(
            status_frame,
            text='Date: ' + str(data[current_image]['image_info']['date'][2])
                + '/' + str(data[current_image]['image_info']['date'][1])
                + '/' + str(data[current_image]['image_info']['date'][0]),
            border = 1,
            background = '#1c1c1c',
            foreground = '#c1c1c1',
            highlightbackground = "#c1c1c1",
            highlightcolor = "#c1c1c1",
            highlightthickness = 1
        )
        info_label.place(x=0, y=0)
#
# def save_undefined(tmp_window, json_path):
#     tmp_window.destroy()
#     save_image(json_path)
#
# def select_undefined(json_path):
#     global vars
#     global checkboxes2
#     global aux_values
#     checkboxes2 = {}
#     aux_values = {}
#     tmp_window = tk.Toplevel()
#     tmp_window.configure(bg = "#1c1c1c")
#     tmp_window.geometry("800x630")
#     global my_image2
#     my_image2 = ImageTk.PhotoImage(Image.open('/tmp/aux.jpg').resize((800,600), Image.ANTIALIAS))
#     bg_label2 = tk.Label(tmp_window, image=my_image2)
#     bg_label2.place(x=0,y=0)
#     for i in vars:
#         aux_values[i] = vars[i].get()
#         checkboxes2[i] = tk.Checkbutton(
#             tmp_window,
#             variable=vars[i],
#             onvalue=3,
#             offvalue=aux_values[i],
#             bd=0,
#             padx=0,
#             pady=0
#         )
#         checkboxes2[i].place(x=aux_centers[i][0], y=aux_centers[i][1], height=7, width=7)
#     confirm_button = tk.Button(tmp_window, text = "Confirm", bg="#1c1c1c", fg="#c1c1c1", activebackground = "#3c3c3c", pady=10, command = lambda: save_undefined(tmp_window, json_path))
#     confirm_button.place(x=360,y=605,width=80, height=20)
#     tmp_window.bind("<Return>", lambda x: save_undefined(tmp_window, json_path))
#
def mark_image_reason(current_image):
    tmp_window = tk.Toplevel()
    tmp_window.configure(bg = '#1c1c1c')
    tmp_window.geometry("300x250")
    reasons=['Carro não segmentado', 'Carro segmentado errado', 'Mascara sem carro', 'Mascara duplicada', 'Outros']
    vars = {}
    # aux_values = {}
    checkboxes = {}
    for i in range(0,5):
        vars[i] = tk.IntVar()
        # aux_values[i] = vars[i].get()
        checkboxes[i] = tk.Checkbutton(
            tmp_window,
            text=reasons[i],
            variable=vars[i],
            onvalue=1,
            offvalue=0,
            bd=0,
            padx=0,
            pady=0
        )
        checkboxes[i].pack()
    confirm_button = tk.Button(tmp_window, text = "Confirm", bg="#1c1c1c", fg="#c1c1c1", activebackground = "#3c3c3c", pady=10, command = lambda: mark_image_function(current_image, vars, tmp_window))
    confirm_button.pack()

def mark_image_function(current_image, vars, tmp_window):
    jsonProcessing.mark_image_as_wrong(current_image, vars)
    tmp_window.destroy()

# def change_image(tmp_window, num_images):
#     global entry1
#     global data
#     global imgs_path
#     global current_image
#     global status_frame
#     global status_label
#     aux = entry1.get()
#     if aux.isnumeric():
#         aux = int(aux)
#         if aux > 0 and aux <= num_images:
#             current_image = aux
#             image_id = current_image
#             set_image(imgs_path+'/'+data[image_id]['image_info']['file_name'], data[image_id]['parkingSpaces_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'])
#             status_label.forget()
#             status_label = tk.Label(
#                 status_frame,
#                 text='Image ' + str(current_image) + ' of ' + str(num_images),
#                 border = 1,
#                 background = '#1c1c1c',
#                 foreground = '#c1c1c1',
#                 highlightbackground = "#c1c1c1",
#                 highlightcolor = "#c1c1c1",
#                 highlightthickness = 1,
#                 anchor = tk.E,
#             )
#             status_label.pack(expand=True, fill='both')
#
#             global info_label
#             info_label = tk.Label(
#                 status_frame,
#                 text='Date: ' + str(data[current_image]['image_info']['date'][2])
#                     + '/' + str(data[current_image]['image_info']['date'][1])
#                     + '/' + str(data[current_image]['image_info']['date'][0])
#                     + '\tCamera: ' + str(data[current_image]['image_info']['camera_id']),
#                 border = 1,
#                 background = '#1c1c1c',
#                 foreground = '#c1c1c1',
#                 highlightbackground = "#c1c1c1",
#                 highlightcolor = "#c1c1c1",
#                 highlightthickness = 1
#             )
#             info_label.place(x=0, y=0)
#     tmp_window.destroy()
#
# def select_image(num_images):
#     tmp_window = tk.Toplevel()
#     tmp_window.configure(padx = 20, pady = 20, bg = "#1c1c1c")
#     label3 = tk.Label(tmp_window, text = "Insert image id", bg="#1c1c1c", fg="#c1c1c1")
#     label3.grid(row=0,column=0,padx=10)
#     global entry1
#     entry1 = tk.Entry(tmp_window)
#     entry1.grid(row=0, column=1)
#     confirm_button = tk.Button(tmp_window, text = "Confirm", bg="#1c1c1c", fg="#c1c1c1", activebackground = "#3c3c3c", command = lambda:change_image(tmp_window,num_images))
#     confirm_button.grid(row=1, column=0, pady=10)
#     tmp_window.bind("<Return>", lambda x: change_image(tmp_window, num_images))
#
def show_original_image():
    tmp_window = tk.Toplevel()
    tmp_window.configure(bg = "#1c1c1c")
    tmp_window.geometry("1000x750")
    global my_image3
    my_image3 = ImageTk.PhotoImage(Image.open('/tmp/aux.jpg'))
    bg_label3 = tk.Label(tmp_window, image=my_image3)
    bg_label3.place(x=0,y=0)
    tmp_window.bind("<Return>", lambda x: tmp_window.destroy())
#
# def replicate_annotations(json_path):
#     global json_data
#     global data
#     global current_image
#     image_ids = jsonProcessing.get_image_ids_from_date(json_data, data[current_image]['image_info']['date'])
#     for im_id in image_ids:
#         if im_id != current_image:
#             data, json_data = jsonProcessing.copy_statuses(data,json_data,current_image,im_id)
#     jsonProcessing.saveJson(json_data, json_path)

def annotation_view(images_path, json_path, image_id, root):
    top = tk.Toplevel()
    top.title("Annotations")

    global image_frame
    global data
    global imgs_path
    global current_image
    global json_data
    global res_constraint

    res_constraint = 1.5

    # global checkboxes
    # checkboxes = {}
    current_image = image_id
    imgs_path = images_path
    json_data, data = jsonProcessing.openJson(json_path)
    num_images = len(json_data['images'])
    if image_id > num_images:
        image_id = num_images
    #
    # x0,y0,x1,y1 = data[image_id]['image_info']['annotationsRectangle']
    w = data[image_id]['image_info']['width']
    h = data[image_id]['image_info']['height']
    top.geometry(str(int(res_constraint*(w))+200)+"x"+str(int(res_constraint*(h))+20))

    image_frame = tk.Frame(top)
    image_frame.place(x=0,y=0, width=int(res_constraint*(w)), height=int(res_constraint*(h)))
    #
    set_image(images_path+'/'+data[image_id]['image_info']['file_name'], data[image_id]['annotations_info'], image_id, data[image_id]['image_info']['width'], data[image_id]['image_info']['height'], data[image_id]['image_info']['annotationsRectangle'])
    #
    side_menu = tk.Frame(
        top,
        bg = '#1c1c1c',
    )
    side_menu.place(x=int(res_constraint*(w)),y=0, width=200, height=int(res_constraint*(h)))

    prev_image_button = tk.Button(
        side_menu,
        text = "Previous Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: prev_image(num_images)
    )
    prev_image_button.place(x=15,y=20, width=170, height=25)

    next_image_button = tk.Button(
        side_menu,
        text = "Next Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: next_image(num_images)
    )
    next_image_button.place(x=15,y=65, width=170, height=25)


    mark_image_button = tk.Button(
        side_menu,
        text = "Mark image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: mark_image_reason(current_image)
    )
    mark_image_button.place(x=15,y=110, width=170, height=25)
    #
    # replicate_annotations_button = tk.Button(
    #     side_menu,
    #     text = "Replicate Annotations",
    #     bg = "#1c1c1c",
    #     activebackground = "#3c3c3c",
    #     fg = "#c1c1c1",
    #     command = lambda: replicate_annotations(json_path)
    # )
    # replicate_annotations_button.place(x=15,y=155, width=170, height=25)
    #
    # prev_image_no_save_button = tk.Button(
    #     side_menu,
    #     text = "Previous Image No Save",
    #     bg = "#1c1c1c",
    #     activebackground = "#3c3c3c",
    #     fg = "#c1c1c1",
    #     command = lambda: prev_image(num_images, json_path, False)
    # )
    # prev_image_no_save_button.place(x=15,y=265, width=170, height=25)
    #
    # next_image_no_save_button = tk.Button(
    #     side_menu,
    #     text = "Next Image No Save",
    #     bg = "#1c1c1c",
    #     activebackground = "#3c3c3c",
    #     fg = "#c1c1c1",
    #     command = lambda: next_image(num_images, json_path, False)
    # )
    # next_image_no_save_button.place(x=15,y=310, width=170, height=25)
    #
    show_original_image_button = tk.Button(
        side_menu,
        text = "Show Mosaic Image",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = lambda: show_original_image()
    )
    show_original_image_button.place(x=15,y=155, width=170, height=25)
    #
    close_program_button = tk.Button(
        side_menu,
        text = "Close Program",
        bg = "#1c1c1c",
        activebackground = "#3c3c3c",
        fg = "#c1c1c1",
        command = root.destroy
    )
    close_program_button.place(x=15,y=200, width=170, height=25)
    #
    # select_undefined_button = tk.Button(
    #     side_menu,
    #     text = "Select Undefined",
    #     bg = "#1c1c1c",
    #     activebackground = "#3c3c3c",
    #     fg = "#c1c1c1",
    #     command = lambda: select_undefined(json_path)
    # )
    # select_undefined_button.place(x=15,y=510, width=170, height=25)
    #
    # select_image_button = tk.Button(
    #     side_menu,
    #     text = "Select Image",
    #     bg = "#1c1c1c",
    #     activebackground = "#3c3c3c",
    #     fg = "#c1c1c1",
    #     command = lambda: select_image(num_images)
    # )
    # select_image_button.place(x=15,y=555, width=170, height=25)
    #
    global status_frame
    status_frame = tk.Frame(top, bg= "#1c1c1c")
    status_frame.place(x=0,y=int(res_constraint*(h)),height=20, width=int(res_constraint*(w))+200)
    #
    global status_label
    status_label = tk.Label(
        status_frame,
        text='Image ' + str(current_image) + ' of ' + str(num_images),
        border = 1,
        background = '#1c1c1c',
        foreground = '#c1c1c1',
        highlightbackground = "#c1c1c1",
        highlightcolor = "#c1c1c1",
        highlightthickness = 1,
        anchor = tk.E,
    )
    status_label.pack(expand=True, fill='both')
    #
    global info_label
    info_label = tk.Label(
        status_frame,
        text='Date: ' + str(data[image_id]['image_info']['date'][2])
            + '/' + str(data[image_id]['image_info']['date'][1])
            + '/' + str(data[image_id]['image_info']['date'][0]),
        border = 1,
        background = '#1c1c1c',
        foreground = '#c1c1c1',
        highlightbackground = "#c1c1c1",
        highlightcolor = "#c1c1c1",
        highlightthickness = 1
    )
    info_label.place(x=0, y=0)
    #
    top.bind("<Control-a>", lambda x: prev_image(num_images))
    top.bind("<Control-w>", lambda x: mark_image_reason(current_image))
    top.bind("<Control-s>", lambda x: next_image(num_images))
    # top.bind("<Control-p>", lambda x: prev_image(num_images, json_path, False))
    # top.bind("<Control-n>", lambda x: next_image(num_images, json_path, False))
    # top.bind("<Control-a>", lambda x: select_undefined(json_path))
    # top.bind("<Control-f>", lambda x: select_image(num_images))
    top.bind("<Control-q>", lambda x: show_original_image())
    top.bind("<Escape>", lambda x: root.destroy())


    # return top
