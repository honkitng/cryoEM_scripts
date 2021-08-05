import os
import mrcfile
import matplotlib.pyplot as plt

"""

=== USER SPECIFIED INPUTS ===

"""

OPEN_FILE_PATH = '/path/to/file'
SAVE_ROOT_NAME = 'root_name'
SAVE_ROOT_PATH = '/path/to/save/new/file/'

"""

=== MAIN SCRIPT BODY ===

"""

with mrcfile.open(OPEN_FILE_PATH) as mrc:
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

for key in coords.keys():
    top_x = min(coords[key][0][0], coords[key][1][0])
    bottom_x = max(coords[key][0][0], coords[key][1][0])
    top_y = min(coords[key][0][1], coords[key][1][1])
    bottom_y = max(coords[key][0][1], coords[key][1][1])

    mrc_cropped = mrc_orig[top_y:bottom_y, top_x:bottom_x]
    with mrcfile.new(f'{os.path.join(SAVE_ROOT_PATH, SAVE_ROOT_NAME)}_{key:03}.mrc') as mrc:
        mrc.set_data(mrc_cropped)
