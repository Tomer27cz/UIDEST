# UIDEST
 Custom Tkinter UI with all image/text/file utilities that i have built/found.

## Usage

Download the repository and install all the reqirements (open terminal in folder)
``` commandline
pip install -r requirements.txt
```
Now you can simply open the `UIDEST UI.py` file. To launch the UI.

## Features

All the fatures are located in `Features/...` and can be run separately. Commands for each can be found here.

### Image Scramblerer

Divides the image into chunks of `tile` size. (the widht and hight should be divisible by the `tile` size)

The `seed` entry is an input for `random.seed()` then `random.shuffle()` shuffels the tiles.

#### Command Usage

##### Encode

``` commandline
ImageScramble.py encode [-h] [-t TILE] [-s SEED] [-o OUTPUT_FOLDER] [-f FORMAT] [-n FILE_NAME] image
```

``` commandline
positional arguments:
  image                 image path

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
```

##### Decode

``` commandline
ImageScramble.py decode [-h] [-t TILE] [-s SEED] [-o OUTPUT_FOLDER] [-f FORMAT] [-n FILE_NAME] image
```

``` commandline
positional arguments:
  image                 image path

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
```
  
### Image To Image Steganography

Framework from [Steganography (by kelvins)](https://github.com/kelvins/steganography). I added support for `more images`, `better cli`, `optimization`

Examples of image combination with 8 bit pixel. Max is 8 images because a pixel is 8 bit. Each number represents bits dedicated to the image number.

![bits](https://cdn.discordapp.com/attachments/892404510465613875/1074626734336512051/bits_dark.png#gh-dark-mode-only)
![bits](https://cdn.discordapp.com/attachments/892404510465613875/1074626734625914920/bits_light.png#gh-light-mode-only)

##### Merge usage

``` commandline
ImageSteganography.py merge [-h] [-b BITS] [--image1 IMAGE1] [--image2 IMAGE2]
                            [--image3 IMAGE3] [--image4 IMAGE4] [--image5 IMAGE5]
                            [--image6 IMAGE6] [--image7 IMAGE7] [--image8 IMAGE8]
                            [-o OUTPUT_FOLDER] [-f FORMAT] [-n FILE_NAME]
```

``` commandline
options:
  -h, --help            show this help message and exit
  -b BITS, --bits BITS  MIN-2_MAX-8 (default: 2)
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

``` commandline
ImageSteganography.py unmerge [-h] [-b BITS] [--image IMAGE] [-o OUTPUT_FOLDER]
                              [-f FORMAT] [-n FILE_NAME]
```

``` commandline
options:
  -h, --help            show this help message and exit
  -b BITS, --bits BITS  MIN-2_MAX-8 (default: 2)
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

``` commandline
TextSteganography.py encode [-h] [-o OUTPUT_FOLDER] [-t] [-f FORMAT] [-n FILE_NAME] input-file image
```

``` commandline
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

``` commandline
TextSteganography.py decode [-h] [-o OUTPUT_FOLDER] [-t] [-f FORMAT] [-n FILE_NAME] image
```

``` commandline
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

``` commandline
TextToImage.py encode [-h] [-o OUTPUT_FOLDER] [-t] [-m] [-f FORMAT] [-n FILE_NAME] input_file
```

``` commandline
positional arguments:
  input_file            input text file

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -t, --transparent     use transparent pixels when using PNG (default: False)
  -m, --mono            monochromatic (all rgb channels are the same) (default: False)
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```

##### Decode

The input `image` should be an image generated by this script. The output will be a text file of `FORMAT` format and `FILE_NAME` name.

``` commandline
TextToImage.py decode [-h] [-o OUTPUT_FOLDER] [-t] [-m] [-f FORMAT] [-n FILE_NAME] image
```

``` commandline
positional arguments:
  image                 image path

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
  -t, --transparent     use transparent pixels when using PNG (default: False)
  -m, --mono            monochromatic (all rgb channels are the same) (default: False)
  -f FORMAT, --format FORMAT
  -n FILE_NAME, --file-name FILE_NAME
```

### Image Extension Transformer

This takes an input `image` and outputs an image with `FORMAT` format.

It is based on the [Pillow](https://pillow.readthedocs.io/en/stable/) library. Because when you just rename the extension it doesn't change the file encoding / type.

This doesn't have a `cli`. It is just a function you can add to your code.

```python
import PIL.Image as Image

input_filename = "input.png"
filename = "output"
extension = "jpg"

try: 
    image = Image.open(input_filename)
except Exception as e: 
    print(f"Error opening image: {e}")

try: 
    image.save(filename, extension)
except Exception as e: 
    print(f"Error saving image: {e}")
```

### Get Metadata

This takes an input `file` and outputs the metadata. 

It is based on [exiftool.exe](https://exiftool.org/). It is a command line tool. It is not a python library.

It is stored in `Features/Executable/exiftool.exe`. It has its own `cli` that you can find [here](https://exiftool.org/#running).

### YouTube Downloader

This is just a user interface for the `cli` of [yt-dlp (fork of youtube-dl)](https://github.com/yt-dlp/yt-dlp).

This is more of a command constructor which shows you the command line. If you want a more easy to use interface you can use [yt-dlp-gui](https://github.com/kannagi0303/yt-dlp-gui).

## Development

This software is still in development. I am still adding features and fixing bugs.

I am a **beginner** programmer. This is my first project that I am **publishing**. I am still **learning**. I am open to suggestions and improvements.

 

### To Do

- [x] Add text to image
- [x] Add metadata extractor
- [x] Add youtube downloader gui for `yt-dlp`
- [ ] Add file path drag and drop (when moving a file over the input file path entry)
- [ ] Add text encoder `(rot13, caesar, hex, binary, base64, etc.)`
- [ ] Add more features to the `gui`
- [ ] Add more features to the `youtube downloader`

















