import json
import numpy as np
import os
import shutil

os.mkdir('Problem_ufpr04')

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

im_offset = 300000
an_offset = 1000000

problem_data = {
    'images': [],
    'annotations': [],
    'categories': [{'id': 1, 'name': 'cars', 'supercategory': 'vehicle', 'color': '#4a2c79', 'metadata': {}, 'keypoint_colors': []}],
}

a = json.load(open('ufpr04.json','r'))

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
        file_name = i['file_name'].split('/')[3]
        shutil.copy(i['file_name'], 'Problem_ufpr04/'+file_name)
        problem_data['images'].append(
            {
                'id': i['id']+im_offset,
                'dataset_id': 9,
                'category_ids': [1],
                'path': '/datasets/Problem_ufpr04/'+file_name,
                'width': 1280,
                'height': 720,
                'file_name': file_name,
                'annotated': False,
                'annotating': [],
                'num_annotations': num_annotations[i['id']],
                'metadata': {},
                'deleted': False,
                'milliseconds': 0,
                'events': [],
                'regenerate_thumbnail': False
            }
        )

json.dump(problem_data, open('problem_ufpr04.json','w'))
