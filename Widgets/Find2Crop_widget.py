import Functions.Find2Crop_Funcs as funcs
import PyQt5.QtCore as Qt
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QPushButton, QSlider, QVBoxLayout, QWidget, QLineEdit, QLabel

class Find2CropWidget(QMainWindow):
    def __init__(self, viewer):
        super().__init__()
        
        self.setWindowTitle("Find2Crop Widget")
        
        layout = QVBoxLayout()
        label = QLabel("Find2Crop Widget")

        find_button = QPushButton("Find")
        crop_button = QPushButton("Crop ROIs")

        thresh_check = QCheckBox("Show Threshold")
        save_check = QCheckBox("Save Crops")

        sigma_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        area_min_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        area_max_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)
        size_slider = QSlider(Qt.Qt.Orientation.Horizontal, self)


        size_slider.setMinimum(1)
        size_slider.setMaximum(500)
        size_slider.setValue(20)
        size_slider_value = size_slider.value()
        label_size_slider = QLabel("ROI Size = " + str(size_slider_value))

        sigma_slider.setMinimum(0)
        sigma_slider.setMaximum(500)
        sigma_slider.setValue(50)
        sigma_slider_value = sigma_slider.value()/50
        label_sigma_slider = QLabel("Sigma = " + str(sigma_slider_value))
        
        area_min_slider.setMinimum(0)
        area_min_slider.setMaximum(1000)
        area_min_slider.setValue(50)
        area_min_slider_value = area_min_slider.value()
        label_area_min_slider = QLabel("Minimum Area = " + str(area_min_slider_value))
        
        area_max_slider.setMinimum(0)
        area_max_slider.setMaximum(10000)
        area_max_slider.setValue(6000)
        area_max_slider_value = area_max_slider.value()
        label_area_max_slider = QLabel("Maximum Area = " + str(area_max_slider_value))

        widgets = [label, 
                   thresh_check,
                   label_sigma_slider,
                   sigma_slider,
                   label_area_min_slider,
                   area_min_slider,
                   label_area_max_slider,
                   area_max_slider, 
                   label_size_slider,
                   size_slider,
                   find_button,
                   save_check,
                   crop_button]
        
        for w in widgets:
            layout.addWidget(w)
            
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
        def updateLabel():
            
            sigma_slider_value = sigma_slider.value()/50
            area_min_slider_value = area_min_slider.value()
            area_max_slider_value = area_max_slider.value()
            size_slider_value = size_slider.value()
            
            label_sigma_slider.setText("Sigma = " + str(sigma_slider_value))
            label_area_min_slider.setText("Minimum Area = " + str(area_min_slider_value))
            label_area_max_slider.setText("Maximum Area = " + str(area_max_slider_value)) 
            label_size_slider.setText("ROI Size = " + str(size_slider_value)) 

        find_button.clicked.connect(lambda: funcs.find(viewer,
                                                        area_min=area_min_slider.value(),
                                                        area_max=area_max_slider.value(),
                                                        sigma=sigma_slider.value(),
                                                        show_thresh=thresh_check.isChecked(),
                                                        size=size_slider.value()))

        crop_button.clicked.connect(lambda: funcs.crop_rois(viewer, saving=save_check.isChecked()))

        area_min_slider.valueChanged.connect(updateLabel)
        area_max_slider.valueChanged.connect(updateLabel)
        sigma_slider.valueChanged.connect(updateLabel)
        size_slider.valueChanged.connect(updateLabel)

