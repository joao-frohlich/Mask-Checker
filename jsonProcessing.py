import json

def openJson(json_path):
    json_data = json.load(open(json_path,'r'))
    data = {}
    for image in json_data['images']:
        data[image['id']] = {'image_info': image, 'annotations_info': []}
    for ps in json_data['annotations']:
        data[ps['image_id']]['annotations_info'].append(ps)
    return json_data, data

def get_image_ids_from_date(json_data, date):
    image_ids = []
    for image in json_data['images']:
        if image['date'] == date:
            image_ids.append(image['id'])
    return image_ids

def mark_image_as_wrong(image_id):
    out_file = open('problem_ids.txt','a+')
    print(image_id,file=out_file)
    out_file.close
