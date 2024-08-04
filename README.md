---FindAndCrop Readme---

Napari Program to automatically detect features on an image and cropping the detected features. The feature detection is based on simple intensity thresholding. The features to be detected can be filtered and selected by their minimum and maximum size. Sigma determines the intensity threshold (sigma std. deviations away from the mean intensity of the image).

Checking the "save" box, will save the crops as .tif images in the selected directory in the dialog. 

Required Python packages: 
napari
numpy
tkinter
opencv-python (cv2)
PyQt5
