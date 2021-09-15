# Mask Checker

Application created for verifying object masks on images datasets.  
Currently, works only in datasets of parking lots, containing information about the images, masks, parking spots and climate in the following format:

```
{ 'images' : [ {'id': Integer => id of the image  
                'file_name': String => path of the image based on the root of the dataset  
                'width': Integer => width of the image  
                'height': Integer => height of the image  
                'annotationsRectangle': [x0,y0,x1,y1] => bottom left and top right 2d points where the masks are
                                                         (if all image is going to be considered, this would be
                                                         [0, 0, width, height])  
                'date': [yyyy, mm, dd] => information about the day when the image was created (if some value is
                                          inexistent, leave this value as 0)  
                'time': [hh, mm, ss] => information about the time when the image was created (if some value is
                                        inexistent, leave this value as 0)  
                'climate': id of the climate (as specified in the 'climates' key of the JSON
             } ],  
  'annotations' :  [ {  'id': Integer => id of the annotation
                        'segmentation': [[Float]] => An array of array of float values, where the outmost array
                                                     represents the full mask and the inner arrays represents
                                                     fragments of the masks, and the float values represent the
                                                     points that corresponds to the fragments, where the points
                                                     are stored as [x0, y0, x1, y1, ...]
                        'area': Integer => represents the area of the mask
                        'bbox': [Float] => An array that stores the minimum rectangle able to fit the entire mask,
                                           in the format [x0, y0, w, h], where x0 and y0 is the information about
                                           the bottom left point of the rectangle and w and h represents width and
                                           height, respectively
                        'iscrowd': Boolean => True if the mask is "blocked" by others masks in the image. Actually,
                                              it isn't used, so it doesn't really matter if it's true or false
                        'image_id': Integer => id of the image that this annotation belongs to
                        'category_id': Integer => id of the category of this annotation. In this case, there is
                                                  only one category, so this value will be always 1
                   } ],
  'categories' :  [ {'supercategory': 'vehicle', 'name': 'car', 'id': 1} ],  
  'parkingSpots' :  [ { 'id': Integer => id of the parking spot
                        'rotatedRect': [Float] => information about the rotated rectangle that fits the parking
                                                  spot. The array is given in the format [x, y, w, h, a], where
                                                  x and y denotates the coordinates of the center, width and
                                                  height are the width and height, respectively, and a is the
                                                  angle of the rectangle
                        'contour': [Integer] => array with the points that more precisely marks the parking
                                                spot. Just like the inner arrays in the segmentation key of the
                                                annotations, this array is in the form [x0, y0, x1, y1, ...]
                        'image_id': Integer => id of the image that this parking spot belongs to
                        'status_id': Integer => id of the status of the parking spot, as defined in the
                                                'statuses' key of the JSON
                    } ],
  'statuses' :  [   {'id': 1, 'name': 'empty'},
                    {'id': 2, 'name': 'occupied'},
                    {'id': 3, 'name': 'undefined' } ],  
  'climates' :  [   {'id': 1, 'name': 'overcast'},
                    {'id': 2, 'name': 'sunny'}, 
                    {'id': 3, 'name': 'rainy'}, 
                    {'id': 4, 'name': 'snowy'}, 
                    {'id': 5, 'name': 'normal'}, 
                    {'id': 6, 'name': 'undefined'} ],
}
```

Note that the keys categories, statuses and climates have the values already defined.  

This app's only purpose is to get the id of the images that have problems in the annotations, like masks that belongs to an inexistent car, cars without any mask in the annotation rectangle, masks that don't fit correctly the car it belongs to or duplicate masks.

The code [getJsonForIds.py](getJsonForIds.py) can be used to get a fragment of the original JSON with only the images and annotations that were marked in the main application. This JSON fragment can be exported to [COCO annotator](https://github.com/jsbroks/coco-annotator) in order to be fixed.

This application don't have any form of structure, because it was developed only fora single purpose and I don't have any intention to continue to develop this project, as it has worked for it's purpose, besides it's limitation. 
