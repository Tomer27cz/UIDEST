# UIDEST
 Custom Tkinter UI with all image/text/file utilities that i have built/found.

## Usage

Download the repository and install all the reqirements (open terminal in folder)
```
pip install -r requirements.txt
```
Now you can simply open the `UIDEST UI.py` file.

## Features

All the fatures are located in `Features/...` and can be run separately. Commands for each can be found here.

### Image Scramblerer

Divides the image into chunks of `tile` size. (the widht and hight should be divisible by the `tile` size)

The `seed` entry is an input for `random.seed()` then `random.shuffle()` shuffels the tiles.

#### Command Usage

```
ImageScramble.py src [-h] [-t TILE] [-s SEED] [-o OUTPUT_FOLDER] [-f FORMAT] [-n FILE_NAME] [--encode] [--decode]
```

#### Arguments
```
positional arguments:
  src                   Image path

options:
  -h, --help            show this help message and exit
  -t TILE, --tile TILE  tile size (default: 10)
  -s SEED, --seed SEED  seed (default: 0)
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        output folder (default: None)
  -f FORMAT, --format FORMAT
                        format (default: PNG)
  -n FILE_NAME, --file-name FILE_NAME
                        file name (default: scrambled_image)
  --encode              encode (default: False)
  --decode              decode (default: False)
  ```
  
  
  
  ### Image To Image Steganography





