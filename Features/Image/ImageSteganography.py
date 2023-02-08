from PIL import Image

class Steganography:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        rgb = r1[:4] + r2[:4], g1[:4] + g2[:4], b1[:4] + b2[:4]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[4:] + '0000', g[4:] + '0000', b[4:] + '0000'
        new_rgb2 = r[:4] + '0000', g[:4] + '0000', b[:4] + '0000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2)

    def merge(self, im_list: list):
        image1, image2 = im_list
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i ,j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i, j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2]


class Steganography3:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        rgb = r1[:4] + r2[:2] + r3[:2], g1[:4] + g2[:2] + g3[:2], b1[:4] + b2[:2] + b3[:2]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[:4] + '0000', g[:4] + '0000', b[:4] + '0000'
        new_rgb2 = r[4:6] + '000000', g[4:6] + '000000', b[4:6] + '000000'
        new_rgb3 = r[6:] + '000000', g[6:] + '000000', b[6:] + '000000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2), self._bin_to_int(new_rgb3)

    def merge(self, im_list: list):
        image1, image2, image3 = im_list
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')
        if image3.size[0] > image1.size[0] or image3.size[1] > image1.size[1]:
            raise ValueError('Image 3 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()
        map3 = image3.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                rgb3 = map3[i, j] if i < image3.size[0] and j < image3.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2, rgb3) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()
        new_image3 = Image.new(image.mode, image.size)
        new_map3 = new_image3.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i, j], new_map3[i, j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2, new_image3]



class Steganography4:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)
        rgb = r1[:2] + r2[:2] + r3[:2] + r4[:2], g1[:2] + g2[:2] + g3[:2] + g4[:2], b1[:2] + b2[:2] + b3[:2] + b4[:2]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[:2] + '000000', g[:2] + '000000', b[:2] + '000000'
        new_rgb2 = r[2:4] + '000000', g[2:4] + '000000', b[2:4] + '000000'
        new_rgb3 = r[4:6] + '000000', g[4:6] + '000000', b[4:6] + '000000'
        new_rgb4 = r[6:] + '000000', g[6:] + '000000', b[6:] + '000000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2), self._bin_to_int(new_rgb3), self._bin_to_int(new_rgb4)

    def merge(self, im_list: list):
        image1, image2, image3, image4 = im_list
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')
        if image3.size[0] > image1.size[0] or image3.size[1] > image1.size[1]:
            raise ValueError('Image 3 should be smaller than Image 1!')
        if image4.size[0] > image1.size[0] or image4.size[1] > image1.size[1]:
            raise ValueError('Image 4 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()
        map3 = image3.load()
        map4 = image4.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                rgb3 = map3[i, j] if i < image3.size[0] and j < image3.size[1] else self.BLACK_PIXEL
                rgb4 = map4[i, j] if i < image4.size[0] and j < image4.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2, rgb3, rgb4) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()
        new_image3 = Image.new(image.mode, image.size)
        new_map3 = new_image3.load()
        new_image4 = Image.new(image.mode, image.size)
        new_map4 = new_image4.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i, j], new_map3[i, j], new_map4[i, j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2, new_image3, new_image4]

class Steganography5:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4, rgb5):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)
        r5, g5, b5 = self._int_to_bin(rgb5)
        rgb = r1[:2] + r2[:2] + r3[:2] + r4[0] + r5[0], g1[:2] + g2[:2] + g3[:2] + g4[0] + g5[0], b1[:2] + b2[:2] + b3[:2] + b4[0] + b5[0]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[:2] + '000000', g[:2] + '000000', b[:2] + '000000'
        new_rgb2 = r[2:4] + '000000', g[2:4] + '000000', b[2:4] + '000000'
        new_rgb3 = r[4:6] + '000000', g[4:6] + '000000', b[4:6] + '000000'
        new_rgb4 = r[6] + '0000000', g[6] + '0000000', b[6] + '0000000'
        new_rgb5 = r[7] + '0000000', g[7] + '0000000', b[7] + '0000000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2), self._bin_to_int(new_rgb3), self._bin_to_int(new_rgb4), self._bin_to_int(new_rgb5)

    def merge(self, im_list: list):
        image1, image2, image3, image4, image5 = im_list
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')
        if image3.size[0] > image1.size[0] or image3.size[1] > image1.size[1]:
            raise ValueError('Image 3 should be smaller than Image 1!')
        if image4.size[0] > image1.size[0] or image4.size[1] > image1.size[1]:
            raise ValueError('Image 4 should be smaller than Image 1!')
        if image5.size[0] > image1.size[0] or image5.size[1] > image1.size[1]:
            raise ValueError('Image 5 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()
        map3 = image3.load()
        map4 = image4.load()
        map5 = image5.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                rgb3 = map3[i, j] if i < image3.size[0] and j < image3.size[1] else self.BLACK_PIXEL
                rgb4 = map4[i, j] if i < image4.size[0] and j < image4.size[1] else self.BLACK_PIXEL
                rgb5 = map5[i, j] if i < image5.size[0] and j < image5.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2, rgb3, rgb4, rgb5) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()
        new_image3 = Image.new(image.mode, image.size)
        new_map3 = new_image3.load()
        new_image4 = Image.new(image.mode, image.size)
        new_map4 = new_image4.load()
        new_image5 = Image.new(image.mode, image.size)
        new_map5 = new_image5.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i, j], new_map3[i, j], new_map4[i, j], new_map5[i, j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2, new_image3, new_image4, new_image5]

class Steganography6:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4, rgb5, rgb6):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)
        r5, g5, b5 = self._int_to_bin(rgb5)
        r6, g6, b6 = self._int_to_bin(rgb6)
        rgb = r1[:2] + r2[:2] + r3[0] + r4[0] + r5[0] + r6[0], g1[:2] + g2[:2] + g3[0] + g4[0] + g5[0] + g6[0], b1[:2] + b2[:2] + b3[0] + b4[0] + b5[0] + b6[0]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[:2] + '000000', g[:2] + '000000', b[:2] + '000000'
        new_rgb2 = r[2:4] + '000000', g[2:4] + '000000', b[2:4] + '000000'
        new_rgb3 = r[4] + '0000000', g[4] + '0000000', b[4] + '0000000'
        new_rgb4 = r[5] + '0000000', g[5] + '0000000', b[5] + '0000000'
        new_rgb5 = r[6] + '0000000', g[6] + '0000000', b[6] + '0000000'
        new_rgb6 = r[7] + '0000000', g[7] + '0000000', b[7] + '0000000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2), self._bin_to_int(new_rgb3), self._bin_to_int(new_rgb4), self._bin_to_int(new_rgb5), self._bin_to_int(new_rgb6) # NOQA

    def merge(self, im_list: list):
        image1, image2, image3, image4, image5, image6 = im_list
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')
        if image3.size[0] > image1.size[0] or image3.size[1] > image1.size[1]:
            raise ValueError('Image 3 should be smaller than Image 1!')
        if image4.size[0] > image1.size[0] or image4.size[1] > image1.size[1]:
            raise ValueError('Image 4 should be smaller than Image 1!')
        if image5.size[0] > image1.size[0] or image5.size[1] > image1.size[1]:
            raise ValueError('Image 5 should be smaller than Image 1!')
        if image6.size[0] > image1.size[0] or image6.size[1] > image1.size[1]:
            raise ValueError('Image 6 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()
        map3 = image3.load()
        map4 = image4.load()
        map5 = image5.load()
        map6 = image6.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                rgb3 = map3[i, j] if i < image3.size[0] and j < image3.size[1] else self.BLACK_PIXEL
                rgb4 = map4[i, j] if i < image4.size[0] and j < image4.size[1] else self.BLACK_PIXEL
                rgb5 = map5[i, j] if i < image5.size[0] and j < image5.size[1] else self.BLACK_PIXEL
                rgb6 = map6[i, j] if i < image6.size[0] and j < image6.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2, rgb3, rgb4, rgb5, rgb6) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()
        new_image3 = Image.new(image.mode, image.size)
        new_map3 = new_image3.load()
        new_image4 = Image.new(image.mode, image.size)
        new_map4 = new_image4.load()
        new_image5 = Image.new(image.mode, image.size)
        new_map5 = new_image5.load()
        new_image6 = Image.new(image.mode, image.size)
        new_map6 = new_image6.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i, j], new_map3[i, j], new_map4[i, j], new_map5[i, j], new_map6[i, j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2, new_image3, new_image4, new_image5, new_image6]

class Steganography7:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4, rgb5, rgb6, rgb7):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)
        r5, g5, b5 = self._int_to_bin(rgb5)
        r6, g6, b6 = self._int_to_bin(rgb6)
        r7, g7, b7 = self._int_to_bin(rgb7)
        rgb = r1[:2] + r2[0] + r3[0] + r4[0] + r5[0] + r6[0] + r7[0], g1[:2] + g2[0] + g3[0] + g4[0] + g5[0] + g6[0] + g7[0], b1[:2] + b2[0] + b3[0] + b4[0] + b5[0] + b6[0] + b7[0]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[:2] + '000000', g[:2] + '000000', b[:2] + '000000'
        new_rgb2 = r[2] + '0000000', g[2] + '0000000', b[2] + '0000000'
        new_rgb3 = r[3] + '0000000', g[3] + '0000000', b[3] + '0000000'
        new_rgb4 = r[4] + '0000000', g[4] + '0000000', b[4] + '0000000'
        new_rgb5 = r[5] + '0000000', g[5] + '0000000', b[5] + '0000000'
        new_rgb6 = r[6] + '0000000', g[6] + '0000000', b[6] + '0000000'
        new_rgb7 = r[7] + '0000000', g[7] + '0000000', b[7] + '0000000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2), self._bin_to_int(new_rgb3), self._bin_to_int(new_rgb4), self._bin_to_int(new_rgb5), self._bin_to_int(new_rgb6), self._bin_to_int(new_rgb7)

    def merge(self, im_list: list):
        image1, image2, image3, image4, image5, image6, image7 = im_list
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')
        if image3.size[0] > image1.size[0] or image3.size[1] > image1.size[1]:
            raise ValueError('Image 3 should be smaller than Image 1!')
        if image4.size[0] > image1.size[0] or image4.size[1] > image1.size[1]:
            raise ValueError('Image 4 should be smaller than Image 1!')
        if image5.size[0] > image1.size[0] or image5.size[1] > image1.size[1]:
            raise ValueError('Image 5 should be smaller than Image 1!')
        if image6.size[0] > image1.size[0] or image6.size[1] > image1.size[1]:
            raise ValueError('Image 6 should be smaller than Image 1!')
        if image7.size[0] > image1.size[0] or image7.size[1] > image1.size[1]:
            raise ValueError('Image 7 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()
        map3 = image3.load()
        map4 = image4.load()
        map5 = image5.load()
        map6 = image6.load()
        map7 = image7.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                rgb3 = map3[i, j] if i < image3.size[0] and j < image3.size[1] else self.BLACK_PIXEL
                rgb4 = map4[i, j] if i < image4.size[0] and j < image4.size[1] else self.BLACK_PIXEL
                rgb5 = map5[i, j] if i < image5.size[0] and j < image5.size[1] else self.BLACK_PIXEL
                rgb6 = map6[i, j] if i < image6.size[0] and j < image6.size[1] else self.BLACK_PIXEL
                rgb7 = map7[i, j] if i < image7.size[0] and j < image7.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2, rgb3, rgb4, rgb5, rgb6, rgb7) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        # Create the new image and load the pixel map
        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()
        new_image3 = Image.new(image.mode, image.size)
        new_map3 = new_image3.load()
        new_image4 = Image.new(image.mode, image.size)
        new_map4 = new_image4.load()
        new_image5 = Image.new(image.mode, image.size)
        new_map5 = new_image5.load()
        new_image6 = Image.new(image.mode, image.size)
        new_map6 = new_image6.load()
        new_image7 = Image.new(image.mode, image.size)
        new_map7 = new_image7.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i, j], new_map3[i, j], new_map4[i, j], new_map5[i, j], new_map6[i, j], new_map7[i, j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2, new_image3, new_image4, new_image5, new_image6, new_image7]

class Steganography8:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        if len(rgb) == 4: r, g, b, a = rgb
        else: r, g, b = rgb
        return f'{r:08b}', f'{g:08b}', f'{b:08b}'

    def _bin_to_int(self, rgb):
        r, g, b = rgb
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2, rgb3, rgb4, rgb5, rgb6, rgb7, rgb8):
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        r3, g3, b3 = self._int_to_bin(rgb3)
        r4, g4, b4 = self._int_to_bin(rgb4)
        r5, g5, b5 = self._int_to_bin(rgb5)
        r6, g6, b6 = self._int_to_bin(rgb6)
        r7, g7, b7 = self._int_to_bin(rgb7)
        r8, g8, b8 = self._int_to_bin(rgb8)
        rgb = r1[0] + r2[0] + r3[0] + r4[0] + r5[0] + r6[0] + r7[0] + r8[0], \
              g1[0] + g2[0] + g3[0] + g4[0] + g5[0] + g6[0] + g7[0] + g8[0], \
              b1[0] + b2[0] + b3[0] + b4[0] + b5[0] + b6[0] + b7[0] + b8[0]
        return self._bin_to_int(rgb)

    def _unmerge_rgb(self, rgb):
        r, g, b = self._int_to_bin(rgb)
        new_rgb1 = r[0] + '0000000', g[0] + '0000000', b[0] + '0000000'
        new_rgb2 = r[1] + '0000000', g[1] + '0000000', b[1] + '0000000'
        new_rgb3 = r[2] + '0000000', g[2] + '0000000', b[2] + '0000000'
        new_rgb4 = r[3] + '0000000', g[3] + '0000000', b[3] + '0000000'
        new_rgb5 = r[4] + '0000000', g[4] + '0000000', b[4] + '0000000'
        new_rgb6 = r[5] + '0000000', g[5] + '0000000', b[5] + '0000000'
        new_rgb7 = r[6] + '0000000', g[6] + '0000000', b[6] + '0000000'
        new_rgb8 = r[7] + '0000000', g[7] + '0000000', b[7] + '0000000'
        return self._bin_to_int(new_rgb1), self._bin_to_int(new_rgb2), self._bin_to_int(new_rgb3), self._bin_to_int(new_rgb4), self._bin_to_int(new_rgb5), self._bin_to_int(new_rgb6), self._bin_to_int(new_rgb7), self._bin_to_int(new_rgb8)

    def merge(self, im_list: list):
        image1, image2, image3, image4, image5, image6, image7, image8 = im_list

        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')
        if image3.size[0] > image1.size[0] or image3.size[1] > image1.size[1]:
            raise ValueError('Image 3 should be smaller than Image 1!')
        if image4.size[0] > image1.size[0] or image4.size[1] > image1.size[1]:
            raise ValueError('Image 4 should be smaller than Image 1!')
        if image5.size[0] > image1.size[0] or image5.size[1] > image1.size[1]:
            raise ValueError('Image 5 should be smaller than Image 1!')
        if image6.size[0] > image1.size[0] or image6.size[1] > image1.size[1]:
            raise ValueError('Image 6 should be smaller than Image 1!')
        if image7.size[0] > image1.size[0] or image7.size[1] > image1.size[1]:
            raise ValueError('Image 7 should be smaller than Image 1!')
        if image8.size[0] > image1.size[0] or image8.size[1] > image1.size[1]:
            raise ValueError('Image 8 should be smaller than Image 1!')

        map1 = image1.load()
        map2 = image2.load()
        map3 = image3.load()
        map4 = image4.load()
        map5 = image5.load()
        map6 = image6.load()
        map7 = image7.load()
        map8 = image8.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                rgb1 = map1[i, j]
                rgb2 = map2[i, j] if i < image2.size[0] and j < image2.size[1] else self.BLACK_PIXEL
                rgb3 = map3[i, j] if i < image3.size[0] and j < image3.size[1] else self.BLACK_PIXEL
                rgb4 = map4[i, j] if i < image4.size[0] and j < image4.size[1] else self.BLACK_PIXEL
                rgb5 = map5[i, j] if i < image5.size[0] and j < image5.size[1] else self.BLACK_PIXEL
                rgb6 = map6[i, j] if i < image6.size[0] and j < image6.size[1] else self.BLACK_PIXEL
                rgb7 = map7[i, j] if i < image7.size[0] and j < image7.size[1] else self.BLACK_PIXEL
                rgb8 = map8[i, j] if i < image8.size[0] and j < image8.size[1] else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2, rgb3, rgb4, rgb5, rgb6, rgb7, rgb8) # NOQA

        return new_image

    def unmerge(self, image):
        pixel_map = image.load()

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()
        new_image2 = Image.new(image.mode, image.size)
        new_map2 = new_image2.load()
        new_image3 = Image.new(image.mode, image.size)
        new_map3 = new_image3.load()
        new_image4 = Image.new(image.mode, image.size)
        new_map4 = new_image4.load()
        new_image5 = Image.new(image.mode, image.size)
        new_map5 = new_image5.load()
        new_image6 = Image.new(image.mode, image.size)
        new_map6 = new_image6.load()
        new_image7 = Image.new(image.mode, image.size)
        new_map7 = new_image7.load()
        new_image8 = Image.new(image.mode, image.size)
        new_map8 = new_image8.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                new_map[i, j], new_map2[i,j], new_map3[i,j], new_map4[i,j], new_map5[i,j], new_map6[i,j], new_map7[i,j], new_map8[i,j] = self._unmerge_rgb(pixel_map[i, j]) # NOQA

        return [new_image, new_image2, new_image3, new_image4, new_image5, new_image6, new_image7, new_image8]


if __name__ == '__main__':
    # import time
    #
    # filename1 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP1.png"
    # filename2 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP2.png"
    # filename3 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP3.png"
    # filename4 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP4.png"
    # filename5 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP5.png"
    # filename6 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP6.png"
    # filename7 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP7.png"
    # filename8 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\PP8.png"
    # filename9 = r"C:\Users\Tomer27cz\Desktop\Files\CODING\Python Projects\Image Editors\Steg.png"
    #
    # start = time.time()
    # Steganography().merge([Image.open(filename1), Image.open(filename2)])
    # print(f"Steg2 Time taken: {time.time() - start}")
    #
    # start = time.time()
    # Steganography3().merge([Image.open(filename1), Image.open(filename2), Image.open(filename3)])
    # print(f"Steg3 Time taken: {time.time() - start}")
    #
    # start = time.time()
    # Steganography4().merge([Image.open(filename1), Image.open(filename2), Image.open(filename3), Image.open(filename4)])
    # print(f"Steg4 Time taken: {time.time() - start}")
    #
    # start = time.time()
    # Steganography5().merge([Image.open(filename1), Image.open(filename2), Image.open(filename3), Image.open(filename4), Image.open(filename5)])
    # print(f"Steg5 Time taken: {time.time() - start}")
    #
    # start = time.time()
    # Steganography6().merge([Image.open(filename1), Image.open(filename2), Image.open(filename3), Image.open(filename4), Image.open(filename5), Image.open(filename6)])
    # print(f"Steg6 Time taken: {time.time() - start}")
    #
    # start = time.time()
    # Steganography7().merge([Image.open(filename1), Image.open(filename2), Image.open(filename3), Image.open(filename4), Image.open(filename5), Image.open(filename6), Image.open(filename7)])
    # print(f"Steg7 Time taken: {time.time() - start}")
    #
    # start = time.time()
    # Steganography8().merge([Image.open(filename1), Image.open(filename2), Image.open(filename3), Image.open(filename4), Image.open(filename5), Image.open(filename6), Image.open(filename7), Image.open(filename8)])
    # print(f"Steg8 Time taken: {time.time() - start}")
    #
    #
    #
    # start = time.time()
    # Steganography().unmerge(Image.open(filename9))
    # print(f"Steg2 Decode time: {time.time() - start}")
    #
    # start = time.time()
    # Steganography3().unmerge(Image.open(filename9))
    # print(f"Steg3 Decode time: {time.time() - start}")
    #
    # start = time.time()
    # Steganography4().unmerge(Image.open(filename9))
    # print(f"Steg4 Decode time: {time.time() - start}")
    #
    # start = time.time()
    # Steganography5().unmerge(Image.open(filename9))
    # print(f"Steg5 Decode time: {time.time() - start}")
    #
    # start = time.time()
    # Steganography6().unmerge(Image.open(filename9))
    # print(f"Steg6 Decode time: {time.time() - start}")
    #
    # start = time.time()
    # Steganography7().unmerge(Image.open(filename9))
    # print(f"Steg7 Decode time: {time.time() - start}")
    #
    # start = time.time()
    # Steganography8().unmerge(Image.open(filename9))
    # print(f"Steg8 Decode time: {time.time() - start}")
    import argparse


    def image_number_type(x):
        x = int(x)
        if x < 2 or x > 8: raise argparse.ArgumentTypeError("Image number: Minimum = 2, Maximum = 8")
        return x

    parser = argparse.ArgumentParser(description='Steganography', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('merge', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    merge.add_argument("-b", "--bits", default=2, type=image_number_type, help="MIN-2_MAX-8")
    merge.add_argument('--image1', help='image path')
    merge.add_argument('--image2', help='image path')
    merge.add_argument('--image3', help='image path')
    merge.add_argument('--image4', help='image path')
    merge.add_argument('--image5', help='image path')
    merge.add_argument('--image6', help='image path')
    merge.add_argument('--image7', help='image path')
    merge.add_argument('--image8', help='image path')
    merge.add_argument("-o", "--output-folder")
    merge.add_argument("-f", "--format", default='PNG')
    merge.add_argument("-n", "--file-name", default='SteganographyOutput')

    unmerge = subparser.add_parser('unmerge', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    unmerge.add_argument("-b", "--bits", default=2, type=image_number_type, help="MIN-2_MAX-8")
    unmerge.add_argument('--image', help='image path')
    unmerge.add_argument("-o", "--output-folder")
    unmerge.add_argument("-f", "--format", default='PNG')
    unmerge.add_argument("-n", "--file-name", default='SteganographyOutput')

    args = parser.parse_args()
    config = vars(args)

    print(config)

    folder = config['output_folder']
    if folder:
        try:
            if folder[-1] == '"': folder = folder[:-1]
            if folder[-1] != "/" or folder[-1] != "\\":
                if "\\" in folder: folder += "\\"
                else: folder += "/"
        except Exception as e:
            print(f'Inputted folder is not a folder path: {e}')

    path = f"{folder}{config['file_name']}.{config['format'].lower()}"

    if args.command == 'merge':
        im_list = []
        for i in range(config['bits']):
            exec(f"im_list.append(Image.open(config['image{i+1}']))")
        n = config['bits'] if config['bits'] != 2 else ''

        exec(f'output = Steganography{n}().merge({im_list})')
        exec(f'output.save(path)')

    elif args.command == 'unmerge':
        output = []
        n = config['bits'] if config['bits'] != 2 else ''
        exec(f'output = Steganography{n}().unmerge(Image.open(config["image"]))')
        for index,image in enumerate(output):
            image.save(f'{folder}{config["file_name"]}_{index}.{config["format"].lower()}')
