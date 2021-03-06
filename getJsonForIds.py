import json
import numpy as np
import os
import shutil
import cv2 as cv

dataset = 'cnr-camera-1'

os.mkdir('Problem_'+dataset)

ids = []

def get_random_color():
    bgr = [hex(x) for x in list(np.random.choice(range(255), size=3))]
    b = bgr[0][2:]
    if len(b) == 1: b = '0'+b
    g = bgr[1][2:]
    if len(g) == 1: g = '0'+g
    r = bgr[2][2:]
    if len(r) == 1: r = '0'+r
    color = '#'+b+g+r
    return color

while True:
    try:
        ids.append(int(input()))
    except EOFError:
        break


problem_data = {
    'images': [],
    'annotations': [],
    'categories': [{'id': 1, 'name': 'cars', 'supercategory': 'vehicle', 'color': '#4a2c79', 'metadata': {}, 'keypoint_colors': []}],
}

im_offset = 0
an_offset = 0

a = json.load(open(dataset+'.json','r'))

num_annotations = {}

for i in a['annotations']:
    if i['image_id'] in ids:
        if i['image_id'] not in num_annotations:
            num_annotations[i['image_id']] = 1
        else:
            num_annotations[i['image_id']] += 1
        problem_data['annotations'].append(
            {
                'id': i['id']+an_offset,
                'image_id': i['image_id']+im_offset,
                'category_id': 1,
                'segmentation': i['segmentation'],
                'area': i['area'],
                'bbox': i['bbox'],
                'iscrowd': False,
                'isbbox': False,
                'color': get_random_color(),
                'metadata': {}
            }
        )

for i in a['images']:
    if i['id'] in ids:
        aux_file_name = i['file_name'].split('/')
        file_name = aux_file_name[len(aux_file_name)-1]
        img = cv.imread(i['file_name']);
        x0,y0,x1,y1 = i['annotationsRectangle']
        x1 = x1 + x0
        y1 = y1 + y0
        cv.line(img,(x0,y0),(x1,y0),(0,0,0),1);
        cv.line(img,(x1,y0),(x1,y1),(0,0,0),1);
        cv.line(img,(x1,y1),(x0,y1),(0,0,0),1);
        cv.line(img,(x0,y1),(x0,y0),(0,0,0),1);
        cv.imwrite('Problem_'+dataset+'/'+file_name,img)
        try:
            num_annot = num_annotations[i['id']]
        except:
            num_annot = 0

        problem_data['images'].append(
            {
                'id': i['id']+im_offset,
                'dataset_id': 9,
                'category_ids': [1],
                'path': '/datasets/Problem_'+dataset+'/'+file_name,
                'width': 1280,
                'height': 720,
                'file_name': file_name,
                'annotated': False,
                'annotating': [],
                'num_annotations': num_annot,
                'metadata': {},
                'deleted': False,
                'milliseconds': 0,
                'events': [],
                'regenerate_thumbnail': False
            }
        )

json.dump(problem_data, open('problem_'+dataset+'.json','w'))
