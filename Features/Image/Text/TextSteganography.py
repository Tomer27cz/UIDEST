from PIL import Image

class TextSteganography:

    def str_to_bin(self, s):
        """Convert a string to binary."""
        binary_list = [format(ord(x), 'b').zfill(8) for x in s]
        binary_list.append('00000100') # Add an "end of transmission" byte to the end of the string
        return binary_list

    def calc_x(self, image, text):
        """Calculate the X value for the specified image and text."""
        pixels_needed = (len(text) * 8) / 3
        pixels = image.size[0] * image.size[1]

        for i in range(8):
            if pixels_needed <= pixels * (i+1): return i+1

    def div(self, n, x):
        """Check if length of string is divisible by X. If not, add a 0 to it until it is."""
        if len(n) % x == 0: return n
        else: return self.div(n + '0', x)

    def bin_list_to_x_str_list(self, bin_list, x):
        """Convert a list of binary strings to a string. Then a list of X*3 digit binary strings."""
        bin_str = ''.join(bin_list)
        bin_str = self.div(bin_str, x*3)
        chunks = [bin_str[i:i + x] for i in range(0, len(bin_str), x)]
        chunks3 = [list(chunks[i:i+3]) for i in range(0, len(chunks), 3)]
        return chunks3

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

    def _merge_rgb(self, rgb, txt, x):
        """Merge RGB with text. The text is 3 digits long."""
        r1, g1, b1 = self._int_to_bin(rgb)
        rgb = r1[:(8-x)] + txt[0], g1[:(8-x)] + txt[1], b1[:(8-x)] + txt[2]
        return self._bin_to_int(rgb)

    def _decode_rgb(self, rgb, x):
        """Unmerge RGB. Into a 3 digit binary string."""
        r, g, b = self._int_to_bin(rgb)
        return r[(8-x):] + g[(8-x):] + b[(8-x):]

    def encode(self, image, text):
        """Encode an image with text. The text must be ASCII."""
        # Check if the text will be shorter than image
        x = self.calc_x(image, text)
        if x > 8: raise ValueError('Text is too long for this image.')
        if not text.isascii(): raise ValueError('The text must be ASCII.')

        blank_spot = ["0" * x] * 3

        # Get the pixel map of the two images
        map1 = image.load()
        txt_bin_list = self.str_to_bin(text) # Convert every character in the text to binary and put it in a list
        txt_bin_list_x = self.bin_list_to_x_str_list(txt_bin_list, x) # Convert the list of binary strings to a list of 3 digit binary strings

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                iteration = (i * image.size[1]) + j
                is_valid = lambda: iteration < len(txt_bin_list_x) # Check if the current pixel is valid
                rgb = map1[i ,j]
                txt = txt_bin_list_x[iteration] if is_valid() else blank_spot # If the current pixel is valid, use the text. If not, use a blank spot
                new_map[i, j] = self._merge_rgb(rgb, txt, x) # NOQA

        return new_image, x

    def decode(self, layer, image):
        """Decode an image. The image must be merged with this program."""
        pixel_map = image.load()

        binary_list = []

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                binary_list.append(self._decode_rgb(pixel_map[i, j], layer))

        return self.bin_to_str(''.join(binary_list))

class TextSteganographyLayered:

    def str_to_bin(self, s):
        """Convert a string to binary."""
        if type(s) == list: return s
        binary_list = [format(ord(x), 'b').zfill(8) for x in s]
        for x in range(16):
            binary_list.append('00000011') # Add 16 "end of text" bytes to the end of the string
        return binary_list

    def is_ascii(self, s):
        """Check if a string is ASCII."""
        if type(s) == list: return True
        return all(ord(c) < 128 for c in s)

    def div(self, n, x):
        """Check if length of string is divisible by X. If not, add a 0 to it until it is."""
        if len(n) % x == 0: return n
        else: return self.div(n + '0', x)

    def bin_list_to_3_str_list(self, bin_list):
        """Convert a list of binary strings to a string. Then a list of 3 digit binary strings."""
        bin_str = ''.join(bin_list)
        bin_str = self.div(bin_str, 3)
        return [bin_str[i:i + 3] for i in range(0, len(bin_str), 3)]

    def bin_to_str(self, s):
        """Convert a binary string to a string."""
        s = s[:s.index('00000011'*16)]
        return ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) // 8)) # get the text between the start of string and 16 "end of text" bytes

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to binary."""
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        """Convert a binary tuple to an integer tuple."""
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb, txt, x):
        """Merge RGB with text. The text is 3 digits long."""
        r1, g1, b1 = self._int_to_bin(rgb)
        rgb = r1[:(8-x)] + txt[0] + r1[(8-x)+1:], g1[:(8 - x)] + txt[1] + g1[(8 - x) + 1:], b1[:(8 - x)] + txt[2] + b1[(8 - x) + 1:]
        return self._bin_to_int(rgb)

    def _decode_rgb(self, rgb, x):
        """Unmerge RGB. Into a 3 digit binary string."""
        r, g, b = self._int_to_bin(rgb)
        return r[7-x] + g[7-x] + b[7-x]

    def encode(self, image, text, layer=1):
        """Encode an image with text. The text must be ASCII."""

        # Check if the text will be shorter than image
        if type(text) != list and len(text) > (image.size[0]*image.size[1])*3: raise ValueError('Text is too long for this image.')
        # check if the text is ascii
        if not self.is_ascii(text): raise ValueError('The text must be ASCII.')

        # Get the pixel map of the image
        map1 = image.load()
        # Convert every character in the text to binary and put it in a list
        # Convert the list of binary strings to a list of 3 digit binary strings
        txt_bin_list = self.bin_list_to_3_str_list(self.str_to_bin(text))
        list_len = len(txt_bin_list)

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                iteration = (i * image.size[1]) + j
                rgb = map1[i ,j]

                if iteration < list_len: # If the current pixel is valid, use the text. If not, use a blank spot
                    txt = txt_bin_list[iteration]
                    new_map[i, j] = self._merge_rgb(rgb, txt, layer)  # NOQA
                else:
                    new_map[i, j] = rgb # NOQA

        bin_list_left = txt_bin_list[image.size[0]*image.size[1]:]
        layers = layer+1
        if len(bin_list_left) > 0:
            new_image, layers = self.encode(new_image, bin_list_left, layers)

        return new_image, layers

    def decode(self, image):
        """Decode an image. The image must be merged with this program."""
        pixel_map = image.load()

        layer_list = []
        for layer in range(8):
            binary_list = []
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    binary_list.append(self._decode_rgb(pixel_map[i, j], layer))
            layer_list.append(''.join(binary_list))

        return self.bin_to_str(''.join(layer_list))

class TextSteganographyLayeredDynamic:
    def str_to_bin(self, s, bits=8):
        """Convert a string to binary."""
        if type(s) == list: return s
        binary_list = [format(bits, 'b').zfill(8)]
        for x in s:
            char = ord(x)
            if char > 2 ** bits - 1: raise ValueError(f"Character {x} cannot be encoded with {bits} bits.")
            binary_list.append(format(char, 'b').zfill(bits))
        binary_list.extend([('0' * (bits - 2) + '11')] * 16)  # Add 16 "end of text" bytes to the end of the string
        return binary_list

    def div(self, n, x):
        """Check if length of string is divisible by X. If not, add a 0 to it until it is."""
        if len(n) % x == 0: return n
        else: return self.div(n + '0', x)

    def bin_list_to_x_str_list(self, bin_list, x):
        """Convert a list of binary strings to a string. Then a list of 3 digit binary strings."""
        bin_str = ''.join(bin_list)
        bin_str = self.div(bin_str, x)
        return [bin_str[i:i + x] for i in range(0, len(bin_str), x)]

    def bin_to_str(self, s, bits=8):
        """Convert a binary string to a string."""
        s = s[:s.index(('0'*(bits-2)+'11')*16)]
        return ''.join(chr(int(s[i * bits:i * bits + bits], 2)) for i in range(len(s) // bits)) # get the text between the start of string and 16 "end of text" bytes

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to binary."""
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        """Convert a binary tuple to an integer tuple."""
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb, txt, x):
        """Merge RGB with text. The text is 3 digits long."""
        r1, g1, b1 = self._int_to_bin(rgb)
        rgb = r1[:(8-x)] + txt[0] + r1[(8-x)+1:], g1[:(8-x)] + txt[1] + g1[(8-x)+1:], b1[:(8-x)] + txt[2] + b1[(8-x)+1:]
        return self._bin_to_int(rgb)

    def _decode_rgb(self, rgb, x):
        """Unmerge RGB. Into a 3 digit binary string."""
        r, g, b = self._int_to_bin(rgb)
        return r[7-x] + g[7-x] + b[7-x]

    def encode(self, image, text, bits=None, layer=1):
        """Encode an image with text. The text must be ASCII."""
        if not bits: bits = max(ord(x) for x in text).bit_length()

        if type(text) != list and len(text)*bits > (image.size[0]*image.size[1])*3*3: raise ValueError('Text is too long for this image.')

        map1 = image.load()
        txt_bin_list = self.bin_list_to_x_str_list(self.str_to_bin(text, bits), 3)
        list_len = len(txt_bin_list)

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                iteration = (i * image.size[1]) + j
                rgb = map1[i ,j]

                if iteration < list_len: # If the current pixel is valid, use the text. If not, use a blank spot
                    txt = txt_bin_list[iteration]
                    new_map[i, j] = self._merge_rgb(rgb, txt, layer)  # NOQA
                else:
                    new_map[i, j] = rgb # NOQA

        bin_list_left = txt_bin_list[image.size[0]*image.size[1]:]
        layers = layer+1
        if len(bin_list_left) > 0:
            new_image, not_important, layers = self.encode(new_image, bin_list_left, bits=bits, layer=layers)

        return new_image, bits, layers

    def decode(self, image, bits=None):
        """Decode an image. The image must be merged with this program."""
        pixel_map = image.load()

        layer_list = []
        for layer in range(8):
            binary_list = []
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    binary_list.append(self._decode_rgb(pixel_map[i, j], layer))
            layer_list.append(''.join(binary_list))
            if layer == 0:
                if not bits:
                    bits = int(layer_list[0][:8], 2)
                layer_list[0] = layer_list[0][8:]

        return self.bin_to_str(''.join(layer_list), bits=bits), bits


class TextSteganographyLayeredDynamicTransparent:
    def str_to_bin(self, s, bits=8):
        """Convert a string to binary."""
        if type(s) == list: return s
        binary_list = [format(bits, 'b').zfill(8)]
        for x in s:
            char = ord(x)
            if char > 2 ** bits - 1: raise ValueError(f"Character {x} cannot be encoded with {bits} bits.")
            binary_list.append(format(char, 'b').zfill(bits))
        binary_list.extend([('0' * (bits - 2) + '11')] * 16)  # Add 16 "end of text" bytes to the end of the string
        return binary_list

    def div(self, n, x):
        """Check if length of string is divisible by X. If not, add a 0 to it until it is."""
        if len(n) % x == 0: return n
        else: return self.div(n + '0', x)

    def bin_list_to_x_str_list(self, bin_list, x):
        """Convert a list of binary strings to a string. Then a list of 3 digit binary strings."""
        bin_str = ''.join(bin_list)
        bin_str = self.div(bin_str, x)
        return [bin_str[i:i + x] for i in range(0, len(bin_str), x)]

    def bin_to_str(self, s, bits=8):
        """Convert a binary string to a string."""
        s = s[:s.index(('0'*(bits-2)+'11')*16)]
        return ''.join(chr(int(s[i * bits:i * bits + bits], 2)) for i in range(len(s) // bits)) # get the text between the start of string and 16 "end of text" bytes

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to binary."""
        r, g, b, a = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}', f'{a:08b}'

    def _bin_to_int(self, rgb):
        """Convert a binary tuple to an integer tuple."""
        r, g, b, a = rgb
        return int(r, 2), int(g, 2), int(b, 2), int(a, 2)

    def _merge_rgb(self, rgb, txt, x):
        """Merge RGB with text. The text is 3 digits long."""
        r1, g1, b1, a1 = self._int_to_bin(rgb)
        rgb = r1[:(8-x)] + txt[0] + r1[(8-x)+1:], g1[:(8-x)] + txt[1] + g1[(8-x)+1:], b1[:(8-x)] + txt[2] + b1[(8-x)+1:], a1[:(8-x)] + txt[3] + a1[(8-x)+1:]
        return self._bin_to_int(rgb)

    def _decode_rgb(self, rgb, x):
        """Unmerge RGB. Into a 3 digit binary string."""
        r, g, b, a = self._int_to_bin(rgb)
        return r[7-x] + g[7-x] + b[7-x] + a[7-x]

    def encode(self, image, text, bits=None, layer=1):
        """Encode an image with text. The text must be ASCII."""
        if not bits: bits = max(ord(x) for x in text).bit_length()

        if type(text) != list and len(text)*bits > (image.size[0]*image.size[1])*4*8: raise ValueError('Text is too long for this image.')


        map1 = image.load()
        txt_bin_list = self.bin_list_to_x_str_list(self.str_to_bin(text, bits), 4)
        list_len = len(txt_bin_list)

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                iteration = (i * image.size[1]) + j
                rgb = map1[i ,j]

                if iteration < list_len: # If the current pixel is valid, use the text. If not, use a blank spot
                    txt = txt_bin_list[iteration]
                    new_map[i, j] = self._merge_rgb(rgb, txt, layer)  # NOQA
                else:
                    new_map[i, j] = rgb # NOQA

        bin_list_left = txt_bin_list[image.size[0]*image.size[1]:]
        layers = layer+1
        if len(bin_list_left) > 0:
            new_image, not_important, layers = self.encode(new_image, bin_list_left, bits=bits, layer=layers)

        return new_image, bits, layers

    def decode(self, image, bits=None):
        """Decode an image. The image must be merged with this program."""
        pixel_map = image.load()

        layer_list = []
        for layer in range(8):
            binary_list = []
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    binary_list.append(self._decode_rgb(pixel_map[i, j], layer))
            layer_list.append(''.join(binary_list))
            if layer == 0:
                if not bits:
                    bits = int(layer_list[0][:8], 2)
                layer_list[0] = layer_list[0][8:]

        return self.bin_to_str(''.join(layer_list), bits=bits), bits


if __name__ == '__main__':
    # from bee_movie import bee_movie_script
    # from time import time
    # filename1 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP1.png"
    # filename2 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\Text_Steganography_Output_yes.png"
    # filename3 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\bee_movie_script12.txt"
    # filename4 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\out.png"
    #
    # # text = bee_movie_script*5
    # # print(len(text))
    # #
    # # text = "Hello World!"
    #
    # text = bee_movie_script
    # # text = "Hello World"
    # print(len(text))
    #
    # # with open(filename3, 'w') as f:
    # #     f.write(text)
    #
    # start = time()
    # output, bits, layers = TextSteganographyLayeredDynamicTransparent().encode(Image.open(filename1), text)
    # output.save(filename2)
    # end = time()
    # print(f'Encoding took {end-start} seconds.')
    #
    # # start = time()
    # # output, bits = TextSteganographyLayeredDynamicTransparent().decode(Image.open(filename2))
    # # end = time()
    # # print(output)
    # # print(f"Decoding took {end-start} seconds.")
    #
    # if output == text:
    #     print("Success!")
    # else:
    #     print("Failure!")
    #
    # input_text = """The unanimous Declaration of the thirteen united States of America, When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another, and to assume among the powers of the earth, the separate and equal station to which the Laws of Nature and of Nature's God entitle them, a decent respect to the opinions of mankind requires that they should declare the causes which impel them to the separation.
    #
    # We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.--That to secure these rights, Governments are instituted among Men, deriving their just powers from the consent of the governed, --That whenever any Form of Government becomes destructive of these ends, it is the Right of the People to alter or to abolish it, and to institute new Government, laying its foundation on such principles and organizing its powers in such form, as to them shall seem most likely to effect their Safety and Happiness. Prudence, indeed, will dictate that Governments long established should not be changed for light and transient causes; and accordingly all experience hath shewn, that mankind are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing the forms to which they are accustomed. But when a long train of abuses and usurpations, pursuing invariably the same Object evinces a design to reduce them under absolute Despotism, it is their right, it is their duty, to throw off such Government, and to provide new Guards for their future security.--Such has been the patient sufferance of these Colonies; and such is now the necessity which constrains them to alter their former Systems of Government. The history of the present King of Great Britain is a history of repeated injuries and usurpations, all having in direct object the establishment of an absolute Tyranny over these States. To prove this, let Facts be submitted to a candid world.
    #
    # He has refused his Assent to Laws, the most wholesome and necessary for the public good.
    #
    # He has forbidden his Governors to pass Laws of immediate and pressing importance, unless suspended in their operation till his Assent should be obtained; and when so suspended, he has utterly neglected to attend to them.
    #
    # He has refused to pass other Laws for the accommodation of large districts of people, unless those people would relinquish the right of Representation in the Legislature, a right inestimable to them and formidable to tyrants only.
    #
    # He has called together legislative bodies at places unusual, uncomfortable, and distant from the depository of their public Records, for the sole purpose of fatiguing them into compliance with his measures.
    #
    # He has dissolved Representative Houses repeatedly, for opposing with manly firmness his invasions on the rights of the people.
    #
    # He has refused for a long time, after such dissolutions, to cause others to be elected; whereby the Legislative powers, incapable of Annihilation, have returned to the People at large for their exercise; the State remaining in the mean time exposed to all the dangers of invasion from without, and convulsions within.
    #
    # He has endeavoured to prevent the population of these States; for that purpose obstructing the Laws for Naturalization of Foreigners; refusing to pass others to encourage their migrations hither, and raising the conditions of new Appropriations of Lands.
    #
    # He has obstructed the Administration of Justice, by refusing his Assent to Laws for establishing Judiciary powers.
    #
    # He has made Judges dependent on his Will alone, for the tenure of their offices, and the amount and payment of their salaries.
    #
    # He has erected a multitude of New Offices, and sent hither swarms of Officers to harrass our people, and eat out their substance.
    #
    # He has kept among us, in times of peace, Standing Armies without the Consent of our legislatures.
    #
    # He has affected to render the Military independent of and superior to the Civil power.
    #
    # He has combined with others to subject us to a jurisdiction foreign to our constitution, and unacknowledged by our laws; giving his Assent to their Acts of pretended Legislation:
    #
    # For Quartering large bodies of armed troops among us:
    #
    # For protecting them, by a mock Trial, from punishment for any Murders which they should commit on the Inhabitants of these States:
    #
    # For cutting off our Trade with all parts of the world:
    #
    # For imposing Taxes on us without our Consent:
    #
    # For depriving us in many cases, of the benefits of Trial by Jury:
    #
    # For transporting us beyond Seas to be tried for pretended offences
    #
    # For abolishing the free System of English Laws in a neighbouring Province, establishing therein an Arbitrary government, and enlarging its Boundaries so as to render it at once an example and fit instrument for introducing the same absolute rule into these Colonies:
    #
    # For taking away our Charters, abolishing our most valuable Laws, and altering fundamentally the Forms of our Governments:
    #
    # For suspending our own Legislatures, and declaring themselves invested with power to legislate for us in all cases whatsoever.
    #
    # He has abdicated Government here, by declaring us out of his Protection and waging War against us.
    #
    # He has plundered our seas, ravaged our Coasts, burnt our towns, and destroyed the lives of our people.
    #
    # He is at this time transporting large Armies of foreign Mercenaries to compleat the works of death, desolation and tyranny, already begun with circumstances of Cruelty & perfidy scarcely paralleled in the most barbarous ages, and totally unworthy the Head of a civilized nation.
    #
    # He has constrained our fellow Citizens taken Captive on the high Seas to bear Arms against their Country, to become the executioners of their friends and Brethren, or to fall themselves by their Hands.
    #
    # He has excited domestic insurrections amongst us, and has endeavoured to bring on the inhabitants of our frontiers, the merciless Indian Savages, whose known rule of warfare, is an undistinguished destruction of all ages, sexes and conditions.
    #
    # In every stage of these Oppressions We have Petitioned for Redress in the most humble terms: Our repeated Petitions have been answered only by repeated injury. A Prince whose character is thus marked by every act which may define a Tyrant, is unfit to be the ruler of a free people.
    #
    # Nor have We been wanting in attentions to our Brittish brethren. We have warned them from time to time of attempts by their legislature to extend an unwarrantable jurisdiction over us. We have reminded them of the circumstances of our emigration and settlement here. We have appealed to their native justice and magnanimity, and we have conjured them by the ties of our common kindred to disavow these usurpations, which, would inevitably interrupt our connections and correspondence. They too have been deaf to the voice of justice and of consanguinity. We must, therefore, acquiesce in the necessity, which denounces our Separation, and hold them, as we hold the rest of mankind, Enemies in War, in Peace Friends.
    #
    # We, therefore, the Representatives of the united States of America, in General Congress, Assembled, appealing to the Supreme Judge of the world for the rectitude of our intentions, do, in the Name, and by Authority of the good People of these Colonies, solemnly publish and declare, That these United Colonies are, and of Right ought to be Free and Independent States; that they are Absolved from all Allegiance to the British Crown, and that all political connection between them and the State of Great Britain, is and ought to be totally dissolved; and that as Free and Independent States, they have full Power to levy War, conclude Peace, contract Alliances, establish Commerce, and to do all other Acts and Things which Independent States may of right do. And for the support of this Declaration, with a firm reliance on the protection of divine Providence, we mutually pledge to each other our Lives, our Fortunes and our sacred Honor."""
    #
    import argparse

    parser = argparse.ArgumentParser(description='TextSteganography', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('encode', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    merge.add_argument("input_file", help="input text file")
    merge.add_argument('image', help='image path')
    merge.add_argument("-o", "--output-folder")
    merge.add_argument("-t", "--transparent", action='store_true', help="use transparent pixels when using PNG")
    merge.add_argument("-f", "--format", default='PNG')
    merge.add_argument("-n", "--file-name", default='TextSteganographyOutput')

    unmerge = subparser.add_parser('decode', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    unmerge.add_argument('image', help='image path')
    unmerge.add_argument("-o", "--output-folder")
    unmerge.add_argument("-t", "--transparent", action='store_true', help="use transparent pixels when using PNG")
    unmerge.add_argument("-f", "--format", default='TXT')
    unmerge.add_argument("-n", "--file-name", default='TextSteganographyOutput')

    args = parser.parse_args()
    config = vars(args)

    print(config)

    def run():
        if args.command == 'encode':
            encode()
        elif args.command == 'decode':
            decode()
        else:
            print('Invalid command (must be encode or decode)')
            exit(1)

    def encode():
        folder = config['output_folder']
        if folder:
            try:
                if folder[-1] == '"': folder = folder[:-1]
                if folder[-1] != "/" or folder[-1] != "\\":
                    if "\\" in folder:
                        folder += "\\"
                    else:
                        folder += "/"
            except Exception as e:
                print(f'Inputted folder is not a folder path: {e}')
                exit(1)

        path = f"{folder}{config['file_name']}.{config['format'].lower()}"

        print("Encoding")
        try:
            with open(config['input_file'], 'r') as f:
                text = f.read()
        except Exception as e:
            print(f'Error reading input file: {config["input_file"]}')
            return 1

        try:
            img = Image.open(config['image'])
        except Exception as e:
            print(f'Error opening image: {config["image"]}')
            return 1

        if config['transparent']:
            try:
                img = img.convert('RGBA')
                output = TextSteganographyLayeredDynamicTransparent().encode(img, text)
                image, bits, layers = output
            except Exception as e:
                print(f'Error encoding text: {e}')
                return 1
        else:
            try:
                img = img.convert('RGB')
                output = TextSteganographyLayeredDynamic().encode(img, text)
                image, bits, layers = output
            except Exception as e:
                print(f'Error encoding text: {e}')
                return 1

        print(f'Encoded {bits} bits in {layers} layers')

        try:
            image.save(path)
            print(f'Saved to {path}')
        except Exception as e:
            print(f'Error saving image: {path}')
            return 1


    def decode():
        folder = config['output_folder']
        if folder:
            try:
                if folder[-1] == '"': folder = folder[:-1]
                if folder[-1] != "/" or folder[-1] != "\\":
                    if "\\" in folder:
                        folder += "\\"
                    else:
                        folder += "/"
            except Exception as e:
                print(f'Inputted folder is not a folder path: {e}')
                exit(1)

        path = f"{folder}{config['file_name']}.{config['format'].lower()}"

        print("Decoding")
        try:
            img = Image.open(config['image'])
        except Exception as e:
            print(f'Error opening image: {config["image"]}')
            return 1

        if config['transparent']:
            try:
                img = img.convert('RGBA')
                output = TextSteganographyLayeredDynamicTransparent().decode(img)
                text, bits = output
            except Exception as e:
                print(f'Error decoding text: {e}')
                return 1
        else:
            try:
                img = img.convert('RGB')
                output = TextSteganographyLayeredDynamic().decode(img)
                text, bits = output
            except Exception as e:
                print(f'Error decoding text: {e}')
                return 1

        print(f'Decoded {bits} bits')

        try:
            with open(path, 'w') as f:
                f.write(text)
            print(f'Saved to {path}')
        except Exception as e:
            print(f'Error saving text: {path}')
            return 1


    run()
