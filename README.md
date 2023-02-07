# UIDEST
 Custom Tkinter UI with all image/text/file utilities that i have built/found.

## Usage

Download the repository and install all the reqirements (open terminal in folder)
```
pip install -r requirements.txt
```
Now you can simply open the `UIDEST UI.py` file. To launch the UI.

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

Framework from [Steganography (by kelvins)](https://github.com/kelvins/steganography). I added support for `more images`, `better cli`, `optimization`

Examples of image combination with 8 bit pixel. Max is 8 images because a pixel is 8 bit. Each number represents bits dedicated to the image number.

`[1,1,1,1,2,2,2,2]` 2 images
`[1,1,1,1,2,2,3,3]` 3 images
`[1,1,2,2,3,3,4,4]` 4 images
`[1,1,2,2,3,3,4,5]` 5 images
`[1,1,2,2,3,4,5,6]` 6 images
`[1,1,2,3,4,5,6,7]` 7 images
`[1,2,3,4,5,6,7,8]` 8 images

##### Merge usage

```
usage: ImageSteganography.py merge [-h] [-b BITS] [--image1 IMAGE1] [--image2 IMAGE2]
                                   [--image3 IMAGE3] [--image4 IMAGE4] [--image5 IMAGE5]
                                   [--image6 IMAGE6] [--image7 IMAGE7] [--image8 IMAGE8]
                                   [-o OUTPUT_FOLDER] [-f FORMAT] [-n FILE_NAME]
options:
  -h, --help            show this help message and exit
  -b BITS, --bits BITS  MIN-2_MAX-8
  --image1 IMAGE1       image path
  --image2 IMAGE2       image path
  --image3 IMAGE3       image path
  --image4 IMAGE4       image path
  --image5 IMAGE5       image path
  --image6 IMAGE6       image path
  --image7 IMAGE7       image path
  --image8 IMAGE8       image path
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```

##### Unmerge usage

Ouput will be `{file name}_{index of image}`. 

```
usage: ImageSteganography.py unmerge [-h] [-b BITS] [--image IMAGE] [-o OUTPUT_FOLDER]
                                     [-f FORMAT] [-n FILE_NAME]

options:
  -h, --help            show this help message and exit
  -b BITS, --bits BITS  MIN-2_MAX-8
  --image IMAGE         image path
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```







