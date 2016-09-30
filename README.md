# preprocess_highres_images_ECBME4040
Preprocessing high res bottle images for NN training set (for ECBM E4040 at Columbia)

## Quick demo
![gif animation](https://raw.githubusercontent.com/VirgileACM/preprocess_highres_images_ECBME4040/master/output_crop_resize_py.gif "Quick overview")

## The idea
The main idea is to quickly crop the images to a square, in sequence, centered on the bottle, resize it at a lower resolution and finally save them in a subfolder. The program allows users to crop and resize 20 images under 2 minutes with a good degree of precision.

## The program structure
Here are the steps followed by the program:
Ask user to select images in the directory of the program (crop_resize.py)
For each of these images, display the bottle in a resizable window. The user will have to click on the top and bottom of the bottle (in order to get the height and center point of the bottle in the image)
The image is cropped in a square, centered in the center of the bottle, and of side heightBottle (1+addHeight). The parameter addHeight being in percent the extra height we want around the bottle (by default 10%).
The images are reduced to a RxR resolution, with R an int, normally 64 or 128.
The images are saved in a new directory called /resized, where they appear in the format: CUID#_liquid_%level_RxR_UniqueCode.png

## Dependencies
#### Tkinter for GUI.
Pre installed in all standard distributions of Pyhton. But changed from Tkinter to tkinter since Python 3. Therefore, it might need some extra code to extend the compatibility to Python 2.
#### PIL for image manipulation.
Install with “pip install Pillow“ in a Unix environment. Easy to install with Anaconda in Windows.

## Future improvement
In general, the code would need to be tested in Windows and Linux. Same for the extra work to extend it to Python 2.
