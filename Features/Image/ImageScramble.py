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
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('encode', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    merge.add_argument("image", help="image path")
    merge.add_argument("-t", "--tile", default=10, type=int, help="tile size")
    merge.add_argument("-s", "--seed", default=0, type=int, help="seed")
    merge.add_argument("-o", "--output-folder", help="output folder")
    merge.add_argument("-f", "--format", help="format", default='PNG')
    merge.add_argument("-n", "--file-name", help="file name", default='scrambled_image')

    unmerge = subparser.add_parser('decode', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    unmerge.add_argument("image", help="image path")
    unmerge.add_argument("-t", "--tile", default=10, type=int, help="tile size")
    unmerge.add_argument("-s", "--seed", default=0, type=int, help="seed")
    unmerge.add_argument("-o", "--output-folder", help="output folder")
    unmerge.add_argument("-f", "--format", help="format", default='PNG')
    unmerge.add_argument("-n", "--file-name", help="file name", default='scrambled_image')
    args = parser.parse_args()
    config = vars(args)
    print(config)

    if args.command == 'encode':
        operation_type = 1
    elif args.command == 'decode':
        operation_type = 0
    else:
        print('Invalid command (must be encode or decode)')
        exit(1)

    folder = config['output_folder']
    if folder:
        try:
            if folder[-1] == '"': folder = folder[:-1]
            if folder[-1] != "/" or folder[-1] != "\\":
                if "\\" in folder: folder += "\\"
                else: folder += "/"
        except Exception as e: print(f'Inputted folder is not a folder path: {e}')

    try:
        new_scramble_algorithm(output_type=config['format'], image_path=config['src'], folder_path=folder, output_name=config['file_name'], seed=config['seed'], size=config['tile'], operation_type=operation_type)
    except Exception as e:
        print(f'Error: \n{e}')