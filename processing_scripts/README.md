# Cryo-EM data processing scripts

## crop_mrc.py

Accepts a mrc file as an input and outputs cropped mrc files specified by the user.

### Usage

1. Edit user specified inputs
2. Run script from command line
3. Add boxes around areas you wish to crop (boxes not visible in current version)
4. Close GUI and all images should be saved to the specified directory

### Requirements:
* python3.8
* pip install matplotlib==3.4.2
* pip install mrcfile==1.3.0
