import napari
import Widgets.Find2Crop_widget as w

# ------------------------------------
# Napari program to find and crop features
# ------------------------------------

viewer = napari.Viewer()

widget = w.Find2CropWidget(viewer)

viewer.window.add_dock_widget(widget)

napari.run()

print("FINISHED")