import os
import argparse

from PIL import Image


# 图片水印
def add_image_mark(image_path, mark_path, args):
    # 打开并转换图片和水印
    image_file = Image.open(image_path)
    mark_file = Image.open(mark_path)
    rgba_image = image_file.convert("RGBA")
    rgba_watermark = mark_file.convert("RGBA")

    # 读取图片和水印的高度和宽度
    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size
    new_size = (int(image_x), int(image_y))

    # 若类型为局部水印，则缩放水印图并添加水印
    if args.type == 1:
        scale = 10  # 缩放10倍
        watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
        new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))

    rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

    # 设置不透明度
    opacity = args.opacity * 280
    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, opacity))
    rgba_watermark.putalpha(rgba_watermark_mask)

    # 设置水印位置,若为局部水印，则选择判断位置
    if args.type == 1:
        location = args.location
        watermark_x, watermark_y = rgba_watermark.size
        if location == "0":
            rgba_image.paste(rgba_watermark, (0, 0), rgba_watermark_mask)  # 左上角
        elif location == "1":
            rgba_image.paste(rgba_watermark, (0, image_y - watermark_y), rgba_watermark_mask)  # 左下角
        elif location == "2":
            rgba_image.paste(rgba_watermark, (image_x - watermark_x, 0), rgba_watermark_mask)  # 右上角
        elif location == "3":
            rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask)  # 右下角
        else:
            left = location.split(",")[0]
            up = location.split(",")[1]
            rgba_image.paste(rgba_watermark, (int(left), int(up)), rgba_watermark_mask)  # 自定义位置
    else:
        rgba_image.paste(rgba_watermark, (0, 0), rgba_watermark_mask)  # 全屏

    image = rgba_image.convert("RGB")
    # 若类型为全图水印擦除部分
    if args.type == 2:
        index_array = args.range.split(",")
        left = index_array[0]
        up = index_array[1]
        right = index_array[2]
        down = index_array[3]
        temp_path = "./temp/"  # 临时文件夹
        temp_crop_name = temp_path + "crop.png"  # 需擦除部分临时图片
        temp_image_name = temp_path + "image.png"  # 全水印临时图片

        # 若临时文件夹不存在则新建
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

        # 剪切保存需擦除的部分并打开
        image_crop = image_file.crop((int(left), int(up), int(right), int(down)))
        image_crop.save(temp_crop_name, quality=args.quality)
        crop_file = Image.open(temp_crop_name)
        crop_images = crop_file.convert("RGBA")

        # 将打好水印的图存为临时文件并与需擦除部分进行合并
        image.save(temp_image_name, quality=args.quality)
        temp_file = Image.open(temp_image_name)
        temp_images = temp_file.convert("RGBA")
        temp_images.paste(crop_images, (int(left), int(up), int(right), int(down)))
        image = temp_images

    mark_name = os.path.basename(mark_path)
    pre_name = mark_name.split(".")[0]
    print(mark_path)
    file_name = pre_name + "-" + os.path.basename(image_path)
    if file_name:
        # 若输出路径不存在则新建
        if not os.path.exists(args.out):
            os.mkdir(args.out)

        # 获取文件名
        new_name = os.path.join(args.out, file_name)
        if os.path.splitext(new_name)[1] != ".png":
            image = image.convert("RGB")
        # 保存添加水印后的图片
        image.save(new_name, quality=args.quality)

        print(file_name + " ---> 成功")
    else:
        print(file_name + " ---> 失败")

def main():
    parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parse.add_argument("-f", "--file", type=str, default="./images",
                       help="请输入一个目录或图像文件路径，默认为./images")
    parse.add_argument("-m", "--mark", type=str, default="./watermark",
                       help="请输入一个目录或图片水印路径，默认为./watermark")
    parse.add_argument("-o", "--out", type=str, default="./output",
                       help="请输入一个目录或图像文件路径，默认为./output")
    parse.add_argument("-t", "--type", default=0, type=int,
                       help="请输入水印类型（0：全图水印，1：局部水印，2：全图水印擦除部门），默认为0")
    parse.add_argument("-r", "--range", default="0,0,100,100", type=str,
                       help="若type为2，则请输入需擦除的矩形范围（左，上，右，下）, 默认为：0,0,100,100")
    parse.add_argument("-l", "--location", default="0", type=str,
                       help="若为局部水印请输入水印位置（0：左上，1：左下，2：右上，3：右下），若需自定义则填写开始坐标如：0,0, 默认为:0")
    parse.add_argument("-opa", "--opacity", default=0.15, type=float,
                       help="请输入水印的不透明度, 默认为0.15")
    parse.add_argument("-qua", "--quality", default=100, type=int,
                       help="请输入图片输出质量, 默认为100")

    args = parse.parse_args()

    # 若水印路径为目录，则遍历目录下所有水印进行添加
    if os.path.isdir(args.mark):
        mark_names = os.listdir(args.mark)
        for mark in mark_names:
            mark_file = os.path.join(args.mark, mark)
            # 若文件源路径为目录，则遍历目录下所有图片添加水印
            if os.path.isdir(args.file):
                image_names = os.listdir(args.file)
                for image in image_names:
                    image_file = os.path.join(args.file, image)
                    add_image_mark(image_file, mark_file, args)
            else:
                add_image_mark(args.file, mark_file, args)
    else:
        # 若文件源路径为目录，则遍历目录下所有图片添加水印
        if os.path.isdir(args.file):
            names = os.listdir(args.file)
            for name in names:
                image_file = os.path.join(args.file, name)
                add_image_mark(image_file, args.mark, args)
        else:
            add_image_mark(args.file, args.mark, args)


if __name__ == "__main__":
    main()