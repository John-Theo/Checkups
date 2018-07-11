from PIL import Image, ImageDraw
import hashlib
import os


def color(i, size, fill_start, fill_end):
    def channel(c):
        """calculate the value of a single color channel for a single pixel"""
        return fill_start[c] + int((i * 1.0 / size) * (fill_end[c] - fill_start[c]))

    """calculate the RGB value of a single pixel"""
    return tuple([channel(c) for c in range(3)])


def apply_grad_to_corner(corner, gradient, backwards=False):
    width, height = corner.size
    width_iter = list(range(width))
    if backwards:
        width_iter.reverse()

    for i in range(height):
        grad_pos = 0
        for j in width_iter:
            pos = (i, j)
            pix = corner.getpixel(pos)
            grad_pos += 1
            if pix[3] != 0:
                corner.putpixel(pos, gradient[grad_pos])

    return corner


def round_rectangle(size, radius, padding, fill_start, fill_end):
    def add_border(img):
        real_img = Image.new('RGBA', (width + 2 * padding, height + 2 * padding), (0, 0, 0, 0))
        real_img.paste(img, (padding, padding))
        return real_img

    def round_corner():
        """Draw a round corner"""
        corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(corner)
        draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill="blue")
        return corner

    """Draw a rounded rectangle"""
    width, height = size
    # size = (width + 2*padding, height + 2*padding)
    rectangle = Image.new('RGBA', size)

    gradient = [color(i, width, fill_start, fill_end) for i in range(height)]

    grad_rect = []
    for i in range(height):
        grad_rect += [gradient[i]] * width
    rectangle.putdata(grad_rect)

    orig_corner = round_corner()

    # upper left
    corner = orig_corner
    apply_grad_to_corner(corner, gradient, False)
    rectangle.paste(corner, (0, 0))

    # lower left
    gradient.reverse()
    backwards = True

    corner = orig_corner.rotate(90)
    apply_grad_to_corner(corner, gradient, backwards)
    rectangle.paste(corner, (0, height - radius))

    # lower right
    corner = orig_corner.rotate(180)
    apply_grad_to_corner(corner, gradient, True)
    rectangle.paste(corner, (width - radius, height - radius))

    # upper right
    gradient.reverse()
    backwards = False

    corner = orig_corner.rotate(270)
    apply_grad_to_corner(corner, gradient, backwards)
    rectangle.paste(corner, (width - radius, 0))

    return add_border(rectangle)


class HashBlock:
    def __init__(self, size, radius, padding, fill_start, fill_end, U2D_FLAG, save_dir='./blocks/'):
        hash_string = [str(x) for x in [size, radius, padding, fill_start, fill_end, U2D_FLAG]]
        hash_ = hashlib.md5()
        hash_.update(''.join(hash_string).encode('utf-8'))
        self.pic_hash = hash_.hexdigest()
        self.save_dir = save_dir
        self.EXIST_FLAG = False

        if os.path.exists(save_dir+self.pic_hash+'.PNG'):
            self.EXIST_FLAG = True
            # print('Pic already exist!')
        else:
            if U2D_FLAG:
                fill_start, fill_end = fill_end, fill_start
            size = (size[0]*10, size[1]*10)
            radius *= 10
            padding *= 10
            self.img = round_rectangle(size, radius, padding, fill_start, fill_end)

    def save(self):
        # pic_type = file_name[-3:].upper()
        # if pic_type not in ['JPG', 'PNG', 'BMP']:
        #     raise Warning('Invalid image type!')
        if not self.EXIST_FLAG:
            if self.save_dir[-1] != '/':
                self.save_dir += '/'
            self.img.save(self.save_dir+self.pic_hash+'.PNG', 'PNG')
        else:
            print('Pic already exist!')
        return self.pic_hash


if __name__ == '__main__':
    hb = HashBlock(
        size=(21, 21),
        radius=2,
        padding=1,
        fill_start=(97, 195, 255),
        fill_end=(199, 234, 255),
        U2D_FLAG=True
    )

    pic_hash = hb.save()
    print(pic_hash+'.PNG')
