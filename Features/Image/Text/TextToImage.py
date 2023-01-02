from PIL import Image
import time

class TextToImage:
    def __init__(self):
        self.end_of_text_bytes = ['00000011'] * 16

    def str_to_bin(self, s):
        """Convert a string to binary."""
        binary_list = [format(ord(x), 'b').zfill(8) for x in s]
        binary_list.extend(self.end_of_text_bytes)
        return binary_list

    def group_by_3(self, lst):
        """Group a list by 3."""
        groups = []
        for i in range(0, len(lst), 3):
            group = lst[i:i + 3]
            while len(group) < 3:
                group.append("00000000")
            groups.append(group)
        return groups

    def get_dimensions(self, area):
        """Get the dimensions of an image with the given area."""
        width = 1
        height = 1
        while width * height < area:
            if width < height:
                width += 1
            else:
                height += 1
        return width, height

    def bin_to_str(self, s):
        """Convert a binary string to a string."""
        return ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) // 8))

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to binary."""
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        """Convert a binary tuple to an integer tuple."""
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def encode(self, text, mono=False):
        """Create an image from a string."""
        if not text.isascii(): raise ValueError('The text must be ASCII.')


        bin_list = self.str_to_bin(text)
        if not mono: bin_list = self.group_by_3(bin_list)
        list_len = len(bin_list)
        width, height = self.get_dimensions(len(bin_list))

        # Create the image
        image = Image.new("RGB", (width, height))
        # Get the pixel map of the image
        new_map = image.load()


        for i in range(image.size[0]):
            for j in range(image.size[1]):
                iteration = (i * image.size[1]) + j

                if iteration < list_len: # If the current pixel is valid, use the text. If not, use a blank spot
                    if mono: rgb = self._bin_to_int((bin_list[iteration], bin_list[iteration], bin_list[iteration]))
                    else: rgb = self._bin_to_int((bin_list[iteration][0], bin_list[iteration][1], bin_list[iteration][2]))
                else:
                    rgb = self._bin_to_int(("00000000", "00000000", "00000000"))
                new_map[i, j] = rgb

        return image

    def decode(self, image, mono=False):
        """Decode an image. The image must be merged with this program."""
        pixel_map = image.load()
        only_red = True

        bin_list = []
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                binary = self._int_to_bin(pixel_map[i, j])
                if mono:
                    if binary[0] == binary[1] == binary[2]:
                        only_red = False
                    bin_list.append(binary[0])
                else: bin_list.append(binary[0] + binary[1] + binary[2])

        binary = "".join(bin_list)
        if only_red: print("Only red was used. Because the image is not monochrome.")
        return self.bin_to_str(binary[:binary.index('00000011'*16)]) # Remove the "end of text" bytes


if __name__ == "__main__":

    from bee_movie import bee_movie_script

    filename = "../../../../TextToImageOutput.png"

    # start = time.time()
    # output = TextToImage().decode(Image.open(filename))
    # end = time.time()
    # print(f"Decoded in {end - start} seconds.")

    start = time.time()
    output = TextToImage().encode(bee_movie_script)
    end = time.time()
    print(f"Encoded in {end - start} seconds.")
    output.save(filename)
