import os
import sys
import math
import argparse

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops


# 添加文字水印
def add_font_mark(image_path, mark, args):
    im = Image.open(image_path)

    image = mark(im)
    name = os.path.basename(image_path)
    if image:
        # 若输出路径不存在则新建
        if not os.path.exists(args.out):
            os.mkdir(args.out)

        # 获取文件名
        new_name = os.path.join(args.out, name)
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        # 保存添加水印后的图片
        image.save(new_name, quality=args.quality)

        print(name + " ---> 成功")
    else:
        print(name + " ---> 失败")


# 生成mark图片，返回添加水印的函数
def generate_mark(args):
    # 设置水印透明度
    def set_opacity(im, opacity):
        assert opacity >= 0 and opacity <= 1

        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im

    # 裁剪图片边缘空白
    def crop_image_white(im):
        bg = Image.new(mode='RGBA', size=im.size)
        diff = ImageChops.difference(im, bg)
        del bg
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
        return im

    # 获取字体宽/度
    is_height_crop_float = '.' in args.font_height_crop
    width = len(args.mark) * args.size
    if is_height_crop_float:
        height = round(args.size * float(args.font_height_crop))
    else:
        height = int(args.font_height_crop)

    # 创建水印图片
    mark = Image.new(mode='RGBA', size=(width, height))

    # 生成文字
    draw_table = ImageDraw.Draw(im=mark)
    draw_table.text(xy=(0, 0), text=args.mark, fill=args.color,
                    font=ImageFont.truetype(args.font_family, size=args.size))
    del draw_table

    # 裁剪空白
    mark = crop_image_white(mark)
    # 设置透明度
    set_opacity(mark, args.opacity)

    # 在im图片上添加水印 im为打开的原图
    def mark_im(im):
        # 计算斜边长度
        c = int(math.sqrt(im.size[0] * im.size[0] + im.size[1] * im.size[1]))

        # 以斜边长度为宽高创建大图（旋转后大图才足以覆盖原图）
        mark2 = Image.new(mode='RGBA', size=(c, c))

        # 在大图上生成水印文字，此处mark为上面生成的水印图片
        y, idx = 0, 0
        while y < c:
            # 制造x坐标错位
            x = -int((mark.size[0] + args.space) * 0.5 * idx)
            idx = (idx + 1) % 2

            while x < c:
                # 在该位置粘贴mark水印图片
                mark2.paste(mark, (x, y))
                x = x + mark.size[0] + args.space
            y = y + mark.size[1] + args.space

        # 将大图旋转一定角度
        mark2 = mark2.rotate(args.angle)

        # 在原图上添加大图水印
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im.paste(mark2,  # 大图
                 (int((im.size[0] - c) / 2), int((im.size[1] - c) / 2)),  # 坐标
                 mask=mark2.split()[3])
        del mark2
        return im

    return mark_im


def main():
    parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parse.add_argument("-f", "--file", type=str, default="./images",
                       help="请输入一个目录或图像文件路径，默认为./images")
    parse.add_argument("-m", "--mark", type=str, default="leeyin98",
                       help="请输入文字水印内容，默认为leeyin98")
    parse.add_argument("-o", "--out", type=str, default="./output",
                       help="请输入一个目录或图像文件路径，默认为./output")
    parse.add_argument("-c", "--color", default="#8B8B1B", type=str,
                       help="请输入HEX颜色值，默认为#8B8B1B")
    parse.add_argument("-s", "--space", default=75, type=int,
                       help="请输入水印间隔，默认为75")
    parse.add_argument("-a", "--angle", default=30, type=int,
                       help="请输入旋转水印角度，默认为30")
    parse.add_argument("--font-family", default="./font/font.ttf", type=str,
                       help="请输入字体路径，默认为./font/font.ttf")
    parse.add_argument("--font-height-crop", default="1.2", type=str,
                       help="请输入水印字体高度，默认为1.2")
    parse.add_argument("-size", "--size", default=50, type=int,
                       help="请输入水印字体大小，默认为50")
    parse.add_argument("-opa", "--opacity", default=0.15, type=float,
                       help="请输入水印的不透明度, 默认为0.15")
    parse.add_argument("-qua", "--quality", default=100, type=int,
                       help="请输入图片输出质量, 默认为100")

    args = parse.parse_args()

    if isinstance(args.mark, str) and sys.version_info[0] < 3:
        args.mark = args.mark.decode("utf-8")

    mark = generate_mark(args)

    # 若文件源路径为目录，则遍历目录下所有图片添加水印
    if os.path.isdir(args.file):
        names = os.listdir(args.file)
        for name in names:
            image_file = os.path.join(args.file, name)
            add_font_mark(image_file, mark, args)
    else:
        add_font_mark(args.file, mark, args)


if __name__ == '__main__':
    main()
