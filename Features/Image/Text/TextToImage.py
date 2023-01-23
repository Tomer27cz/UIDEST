from PIL import Image
import time

class TextToImageDynamic:
    def str_to_bin(self, s, bits=8):
        """Convert a string to binary."""
        binary = [format(bits, 'b').zfill(8)]
        binary.extend(format(ord(x), 'b').zfill(bits) for x in s)
        binary.extend([('0' * (bits - 2) + '11')] * 16)
        bin_str = self.div(''.join(binary), 8)
        return [bin_str[i:i + 8] for i in range(0, len(bin_str), 8)]

    def div(self, n, x):
        """Check if length of string is divisible by X. If not, add a 0 to it until it is."""
        if len(n) % x == 0: return n
        else: return self.div(n + '0', x)

    def group_by_x(self, lst, x):
        """Group a list by 3."""
        groups = []
        for i in range(0, len(lst), x):
            group = lst[i:i + x]
            while len(group) < x:
                if len(group) >= 3: group.append("11111111")
                else: group.append("00000000")
            groups.append(group)
        return groups

    def get_dimensions(self, area):
        """Get the dimensions of an image with the given area."""
        width = 1
        height = 1
        while width * height < area:
            if width < height: width += 1
            else: height += 1
        return width, height

    def bin_to_str(self, s, bits=8):
        """Convert a binary string to a string."""
        s = s[:s.index(('0' * (bits - 2) + '11') * 16)]
        return ''.join(chr(int(s[i * bits:i * bits + bits], 2)) for i in range(len(s) // bits))

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to binary."""
        return f'{rgb[0]:08b}', f'{rgb[1]:08b}', f'{rgb[2]:08b}'

    def _int_to_bin_alpha(self, rgb):
        """Convert an integer tuple to binary."""
        return f'{rgb[0]:08b}', f'{rgb[1]:08b}', f'{rgb[2]:08b}', f'{rgb[3]:08b}'

    def _bin_to_int(self, rgb):
        """Convert a binary tuple to an integer tuple."""
        return int(rgb[0], 2), int(rgb[1], 2), int(rgb[2], 2)

    def _bin_to_int_alpha(self, rgb):
        """Convert a binary tuple to an integer tuple."""
        return int(rgb[0], 2), int(rgb[1], 2), int(rgb[2], 2), int(rgb[3], 2)

    def encode(self, text, mode="RGB", bits=None):
        """Create an image from a string."""
        if not bits: bits = max(ord(x) for x in text).bit_length()

        bin_list = self.str_to_bin(text, bits)
        if mode == "RGB": bin_list = self.group_by_x(bin_list, 3)
        if mode == "RGBA": bin_list = self.group_by_x(bin_list, 4)
        list_len = len(bin_list)
        width, height = self.get_dimensions(list_len)

        # Create the image
        if mode == "RGB": image = Image.new("RGB", (width, height), color=(0, 0, 0))
        elif mode == "RGBA": image = Image.new("RGBA", (width, height), color=(0, 0, 0, 255))
        elif mode == "L": image = Image.new("L", (width, height), color=0)
        else: raise ValueError("Invalid mode.")
        # Get the pixel map of the image
        new_map = image.load()

        if mode == "L":
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    iteration = (i * image.size[1]) + j
                    if iteration < list_len: new_map[i, j] = int(bin_list[iteration], 2)
        elif mode == "RGBA":
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    iteration = (i * image.size[1]) + j
                    if iteration < list_len: new_map[i, j] = self._bin_to_int_alpha(bin_list[iteration])
        elif mode == "RGB":
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    iteration = (i * image.size[1]) + j
                    if iteration < list_len: new_map[i, j] = self._bin_to_int(bin_list[iteration])
        else: raise ValueError("Invalid mode.")

        return image, bits

    def decode(self, image, mode="RGB", bits=None):
        """Decode an image. The image must be merged with this program."""
        pixel_map = image.load()

        bin_list = []
        if mode == "L":
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    bin_list.append(f'{pixel_map[i, j]:08b}')

        elif mode == "RGBA":
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    bin_list.append(''.join(self._int_to_bin_alpha(pixel_map[i, j])))

        elif mode == "RGB":
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    bin_list.append(''.join(self._int_to_bin(pixel_map[i, j])))

        else: raise ValueError("Invalid mode.")

        binary = "".join(bin_list)
        if not bits:
            bits = int(binary[:8], 2)
            binary = binary[8:]
        return self.bin_to_str(binary, bits=bits), bits


if __name__ == "__main__":

    from bee_movie import bee_movie_script

    filename1 = "../../../../TextToImageOutput.png"
    filename11 = "../../../../TextToImageOutput.jpg"
    filename2 = "../../../../Dobry_den.txt"

    #txt = "Ahoj Světe"
    # with open(filename2, "r") as f:
    #     txt = f.read()
    txt = bee_movie_script*100

    print(len(txt))

    start = time.time()
    output, bits = TextToImageDynamic().encode(txt, mode="RGB")
    end = time.time()
    print(f"Encoded in {end - start} seconds. With {bits} bits.")
    output.save(filename1)


    start = time.time()
    output, bits = TextToImageDynamic().decode(Image.open(filename1), mode="RGB")
    end = time.time()
    print(f"Decoded in {end - start} seconds. With {bits} bits.")

    if output == txt:
        print("Success!")


