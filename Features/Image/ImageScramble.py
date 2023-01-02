import random
from PIL import Image

def new_scramble_algorithm(operation_type="Encode", output_type="PNG", image_path='image.png', folder_path="", output_name="output", seed=69, size=10):
    random.seed(seed)

    try:
        im = Image.open(image_path)
    except FileNotFoundError:
        return "File not found."

    block_list = []

    width, height = im.size
    blocks = [(x, y, x + size, y + size) for x in range(0, width, size) for y in range(0, height, size)]

    comparison_list = list(range(0, len(blocks)))
    random.shuffle(comparison_list)

    for iteration in range(len(blocks)):
        block = im.crop(blocks[iteration])
        block_list.append(block)

    new_image = Image.new("RGB", (width, height))

    if operation_type == 'Encode':
        for iteration in range(len(blocks)):
            new_image.paste(block_list[comparison_list[iteration]], blocks[iteration][0:2])
    else:
        for iteration in range(len(blocks)):
            new_image.paste(block_list[comparison_list.index(iteration)], blocks[iteration][0:2])

    try:
        path = folder_path + output_name + "." + output_type.lower()
        new_image.save(path, output_type)
        return f"Success."
    except FileNotFoundError:
        new_image.save(output_name, output_type)
        return "Success. (Folder not found. Image saved in program folder.)"


if __name__ == "__main__":
    print("Image Scramble")
