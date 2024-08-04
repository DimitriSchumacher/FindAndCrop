import napari
import numpy as np
import cv2 as cv
from tkinter import Tk
from tkinter import filedialog

def layers_(viewer):
    
    layers = viewer.layers
    
    shape_layers_ = []
    img_layers_ = []
    shapes_info_ = []
    
    for layer in layers:
        
        if type(layer) == napari.layers.image.image.Image:
            
            img_layers_.append(layer)
            
        elif type(layer) == napari.layers.shapes.shapes.Shapes:
            
            if len(layer.data) > 0:
                
                first_shape = layer.data[0]
                
                dimensions = first_shape.shape
                
                if dimensions[1] == 3:
                    
                    shape_data = np.array(layer.data)
                    shape_slice = shape_data[0:, 0:, 1:].astype("int") # take out frame number from shape info
                    
                    shape_layers_.append(layer)
                    shapes_info_.append(shape_slice)
                
                elif dimensions[1] == 2: 
                    
                    layer_data = np.array(layer.data)
                    layer_data = layer_data.astype("int")
                    
                    
                    shape_layers_.append(layer)
                    shapes_info_.append(layer_data)
                
                else: 
                    message = "Weird ROI dimensions: check shapes layer!"
                    viewer.status = message
                    print(message)
                    break 
            else: 
                message = "Empty shapes layer detected! Add a ROI."
                viewer.status = message
                print(message)
                  
    return img_layers_, shape_layers_, shapes_info_

def crop(viewer):

    img_layers, shape_layers, shapes_info = layers_(viewer)

    shape_layer = viewer.layers.selection.active.data
    
    cropped = []
    
    for shape in shape_layer:
        
        dimensions = shape.shape

        if len(dimensions) == 3:
            
            top_left = shape[0][1:].astype("int")
            bottom_right = shape[2][1:].astype("int")    
        
        elif len(dimensions) == 2:
                
            top_left = shape[0].astype("int")
            bottom_right = shape[2].astype("int")
        
        else: 
            message = "Weird ROI dimensions: check shapes layer!"
            viewer.status = message
            print(message)
            break 
        
        for img in img_layers:
            
            if len(img.data.shape) > 2:
                
                img_data = img.data
                #last_frame = last_frame

                crop = img_data[:, top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
                cropped.append(crop)
                    
            else: 
                
                img_data = img.data
                crop = img_data[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]]
                cropped.append(crop)
    
    return cropped

def threshold(image, viewer, sigma, show_thresh):
    
    img = image

    if len(img.shape) > 2:

        img = image[0]
    else:
        img = image  

    mean_value = np.mean(img)
    std_dev = np.std(img)
    sigma = sigma/50
    threshold_value = mean_value+std_dev*sigma
    
    blur = cv.GaussianBlur(img,(3,3),3)

    ret_, th_ = cv.threshold(blur, threshold_value, 255, cv.THRESH_BINARY)
    th_ = th_.astype('uint8')

    if show_thresh == True: 
        viewer.add_image(th_, name="Threshold")
    
    return th_
        
def detect(image):
    
    detection = cv.connectedComponentsWithStats(image) 

    return detection    

def sort_to_find(stats, area_min, area_max, roi_size, img_size, viewer):
    # roi_size --> roi is a square of roi_size x roi_size
    
    amt = stats[0]
    area = stats[2][:,4]
    centroid = stats[3]

    roi_layer = viewer.add_shapes(name="Detected")
    
    # Iterate over detected features 
    for i in range(amt):
        # Check that amt is not empty
        if i > 0:
            # Check for area criterium
            if area[i] >= area_min and area[i] <= area_max: 

                centroid_x = int(centroid[i][0])
                centroid_y = int(centroid[i][1])

                top_left = [centroid_y+roi_size, centroid_x-roi_size]
                bottom_right = [centroid_y-roi_size, centroid_x+roi_size]
                coordinates = [top_left, bottom_right]

                # Check no overlap with edges
                if top_left[0] < img_size[0] and top_left[1] > 0 and bottom_right[0] > 0 and bottom_right[1] < img_size[1]:
                
                    roi_layer.add_rectangles(coordinates, face_color="#ffffff00", edge_width=3, edge_color="yellow")

def find(viewer, area_min, area_max, sigma, show_thresh, size):

    img = viewer.layers.selection.active.data
    
    thresh = threshold(image=img, viewer=viewer, sigma=sigma, show_thresh=show_thresh)    

    detection = detect(image=thresh)

    sort_to_find(stats=detection, area_min=area_min, area_max=area_max, roi_size=size, img_size=thresh.shape, viewer=viewer)

def crop_rois(viewer, saving):

    crops = crop(viewer)

    for cropped in crops:

        viewer.add_image(cropped, name="Crop")

    if saving == True:
            
        root = Tk()
        root.withdraw()

        path = filedialog.askdirectory()

        img_layers, _, _ = layers_(viewer)

        count = -1

        original_name = 0

        for img in img_layers:

            if "Crop" not in str(img):

                original_name = str(img)

        for img in img_layers:

            img_name = str(img)

            if "Crop" in img_name:
                
                count += 1

                img.save(path + "/" + str(original_name[:-4]) + "_Crop_" + str(count))