import random
from PIL import Image


def new_scramble_algorithm(output_type="PNG", image_path='image', folder_path="", output_name="output", seed=69, size=10, operation_type=1):
    random.seed(seed)
    im = Image.open(image_path)

    block_list = []

    width, height = im.size
    blocks = [(x, y, x + size, y + size) for x in range(0, width, size) for y in range(0, height, size)]

    comparison_list = list(range(0, len(blocks)))
    random.shuffle(comparison_list)

    for iteration in range(len(blocks)):
        block = im.crop(blocks[iteration])
        block_list.append(block)

    new_image = Image.new("RGB", (width, height))

    if operation_type == 1:
        for iteration in range(len(blocks)):
            new_image.paste(block_list[comparison_list[iteration]], blocks[iteration][0:2])
    else:
        for iteration in range(len(blocks)):
            new_image.paste(block_list[comparison_list.index(iteration)], blocks[iteration][0:2])

    try:
        path = folder_path + output_name + "." + output_type.lower()
        new_image.save(path)
    except (FileNotFoundError, ValueError, TypeError):
        path = output_name + "." + output_type.lower()
        new_image.save(path)
        raise FileNotFoundError('Folder not found/specified. Image saved in program folder')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ImageScramble", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src", help="Image path")
    parser.add_argument("-t", "--tile", default=10, type=int, help="tile size")
    parser.add_argument("-s", "--seed", default=0, type=int, help="seed")
    parser.add_argument("-o", "--output-folder", help="output folder")
    parser.add_argument("-f", "--format", help="format", default='PNG')
    parser.add_argument("-n", "--file-name", help="file name", default='scrambled_image')
    parser.add_argument("--encode", action="store_true", help="encode", default=False)
    parser.add_argument("--decode", action="store_true", help="decode", default=False)
    args = parser.parse_args()
    config = vars(args)
    # config = {'src': r"C:\Users\Admin\Desktop\merged_file.png", 'tile': 10, 'seed': 69, 'output_folder': r"C:\Users\Admin\Desktop", 'format': 'JPG', 'file_name': 'test_of_vli', 'encode': True, 'decode': False}
    enc = config['encode']
    dec = config['decode']
    act = 1
    if enc and not dec: act = 1
    if not enc and dec: act = 0
    if enc and dec: raise ValueError('Only one possible (encode or decode)')
    folder = config['output_folder']
    if folder:
        try:
            if folder[-1] == '"': folder = folder[:-1]
            if folder[-1] != "/" or folder[-1] != "\\":
                if "\\" in folder: folder += "\\"
                else: folder += "/"
        except Exception as e: print(f'Inputted folder is not a folder path: {e}')

    print(f"""Running with arguments:
     src -> {config['src']}
     tile -> {config['tile']}
     seed -> {config['seed']}
     folder -> {folder}
     format -> {config['format']}
     name -> {config['file_name']}
     type -> {'encode' if act == 1 else 'decode'}""")

    try:
        new_scramble_algorithm(output_type=config['format'], image_path=config['src'], folder_path=folder, output_name=config['file_name'], seed=config['seed'], size=config['tile'], operation_type=act)
    except Exception as e:
        print(f'Error: \n{e}')