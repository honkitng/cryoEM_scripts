# Cryo-EM montage scripts

## mmm_stitching.py

Accepts an MMM file and outputs stitched tiff files of all the MMMs.

### Usage

    python3.8 mmm_stitching.py [MMM file] [output root name] [number of rows in MMM] [number of columns in MMM] [overlap %] [dataset type]

### Requirements:
* python3.8
* pip install matplotlib==3.4.2
* pip install opencv-python==4.5.5.62
* pip install numpy==1.22.3
