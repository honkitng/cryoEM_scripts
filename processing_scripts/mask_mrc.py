import os
import mrcfile
import matplotlib.pyplot as plt

"""

=== USER SPECIFIED INPUTS ===

"""

MRC_DIRECTORY = '/path/to/mrc/directory/'
TIFF_DIRECTORY = '/path/to/tiff/directory/'
SAVE_DIRECTORY = '/path/to/save/new/tiff/files/'

"""

=== MAIN SCRIPT BODY ===

"""

mrc_files = [file for file in os.listdir(MRC_DIRECTORY) if file.endswith(".mrc")]
tiff_files = [file for file in os.listdir(MRC_DIRECTORY) if file.endswith(".tif") or file.endswith(".tiff")]

for file in mrc_files:
    with mrcfile.open(os.path.join(MRC_DIRECTORY, file)) as mrc:
        mrc_orig = mrc.data

    mrc_orig.setflags(write=1)
    fig, ax = plt.subplots()

    crop_count = 0
    first_coords = (0, 0)
    coords = {}


    def onclick(event):
        global first_coords

        if event.button == 1:
            first_coords = (int(event.xdata), int(event.ydata))


    def onrelease(event):
        global crop_count, first_coords, coords

        if event.button == 1:
            crop_count += 1
            second_coords = (int(event.xdata), int(event.ydata))
            coords[crop_count] = (first_coords, second_coords)


    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.canvas.mpl_connect('button_release_event', onrelease)
    plt.imshow(mrc_orig, cmap='gray')
    plt.show()