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

Ouput will be `{file name}_{index of image}`. It will output `BITS` amount of imgaes into `OUTPUT_FOLDER`. 

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

### Text To Image

Framework from [Steganography (by kelvins)](https://github.com/kelvins/steganography). I modified the code to use text.

First it looks though the text and identifies the most bits it has to use for each character. Then it uses that amount for each character. It puts the number of bits it will use at the start in an 8 bit intiger.

#### Arguments

##### Encode

This takes an input `.txt` file and an `image` file. Then outputs an image with the `FORMAT` format and `FILE_NAME` name.

```
usage: TextSteganography.py encode [-h] [-o OUTPUT_FOLDER] [-t] [-f FORMAT] [-n FILE_NAME] input-file image

positional arguments:
  input_file            input text file
  image                 image path

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -t, --transparent     use transparent pixels when using PNG
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```

##### Decode

This takes an input `image`. Outputs text file with `FORMAT` format and `FILE_NAME` name.

```
usage: TextSteganography.py decode [-h] [-o OUTPUT_FOLDER] [-t] [-f FORMAT] [-n FILE_NAME] image

positional arguments:
  image                 image path

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -t, --transparent     use transparent pixels when using PNG
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```

### Text To Image Generator

This generates an image with `FORMAT` format and `file_name` name from the text in `input_file`. It selects the smallest `width` and `height` square that the text can fit into. 

`mono` monochromatic - it uses all the rgb channels at once (all channels are the same)

`transparent` - uses transparency and overrides the `FORMAT` to `PNG`

#### Arguments

##### Encode

Input should be a text file. The output will be an image of `FORMAT` format and `FILE_NAME` name.

```
usage: TextToImage.py encode [-h] [-o OUTPUT_FOLDER] [-t] [-m MONO] [-f FORMAT] [-n FILE_NAME] input_file

positional arguments:
  input_file            input text file

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -t, --transparent     use transparent pixels when using PNG
  -m MONO, --mono MONO  monochromatic (all rgb channels are the same)
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```

##### Decode

The input `image` should be an image generated by this script. The output will be a text file of `FORMAT` format and `FILE_NAME` name.

```
usage: TextToImage.py decode [-h] [-o OUTPUT_FOLDER] [-t] [-m MONO] [-f FORMAT] [-n FILE_NAME] image

positional arguments:
  image                 image path

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -t, --transparent     use transparent pixels when using PNG
  -m MONO, --mono MONO  monochromatic (all rgb channels are the same)
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```























