## 批量添加水印

**Pre**：导入PIL库，`pip install Pillow`

### 文字水印

#### 用法说明

```
usage: wordMarker.py [-h]
		     [-f FILE] --请输入一个目录或图像文件路径，默认为./images
		     [-m MARK] --请输入文字水印内容，默认为leeyin98
		     [-o OUT] --请输入一个目录或图像文件路径，默认为./output
		     [-c COLOR] --请输入HEX颜色值，默认为#8B8B1B
		     [-s SPACE] --请输入水印间隔，默认为75
                     [-a ANGLE] --请输入旋转水印角度，默认为30
                     [--font-family FONT_FAMILY] --请输入字体路径，默认为./font/font.ttf
                     [--font-height-crop FONT_HEIGHT_CROP] --请输入水印字体高度，默认为1.2
                     [-size SIZE] --请输入水印字体大小，默认为50
                     [-opa OPACITY] --请输入水印的不透明度, 默认为0.15
                     [-qua QUALITY] --请输入图片输出质量, 默认为100

完整用法示例：python wordMarker.py -f ./images/test.jpg -m leeyin98 -opa 0.5
```

#### 示例效果

**原图：**

<img src="https://raw.githubusercontent.com/leeyin98/figurebed/master/typoraImgs/test.jpg" alt="test" style="zoom:33%;max-width:33%" />

**效果图：**

命令：`python wordMarker.py -f ./images/test.jpg -m leeyin98 -opa 0.5`

<img src="https://raw.githubusercontent.com/leeyin98/figurebed/master/typoraImgs/test-16501151465691.jpg" alt="test" style="zoom:33%;max-width:33%" />

### 图片水印

#### 用法说明

```
usage: imageMarker.py [-h]
		      [-f FILE] --请输入一个目录或图像文件路径，默认为./images
		      [-m MARK] --请输入一个目录或图片水印路径，默认为./watermark
		      [-o OUT] --请输入一个目录或图像文件路径，默认为./output
		      [-t TYPE] --请输入水印类型（0：全图水印，1：局部水印，2：全图水印擦除部门），默认为0
		      [-r RANGE] --若type为2，则请输入需擦除的矩形范围（左，上，右，下）, 默认为：0,0,100,100
                      [-l LOCATION] --若为局部水印请输入水印位置（0：左上，1：左下，2：右上，3：右下），若需自定义则填写开始坐标如：0,0, 默认为:0
                      [-opa OPACITY] --请输入水印的不透明度, 默认为0.15
                      [-qua QUALITY] --请输入图片输出质量, 默认为100


完整用法示例：python imageMarker.py -t 0 --opa 0.2
```

#### 示例效果

**原图：**

<img src="https://raw.githubusercontent.com/leeyin98/figurebed/master/typoraImgs/test.jpg" alt="test" style="zoom:33%;max-width:33%" />

**效果图（type=0）：**

命令：`python imageMarker.py -t 0 --opa 0.2`

<img src="https://raw.githubusercontent.com/leeyin98/figurebed/master/typoraImgs/test-16501152777732.jpg" alt="test" style="zoom:33%;max-width:33%" />

**效果图（type=1）：**

命令：`python imageMarker.py -t 1 --opa 0.9 -l 3`

<img src="https://raw.githubusercontent.com/leeyin98/figurebed/master/typoraImgs/test-16501153743883.jpg" alt="test" style="zoom:33%;max-width:33%" />

**效果图（type=2）：**

命令：`python imageMarker.py -t 2 --opa 0.7 -r 300,300,630,600`

<img src="https://raw.githubusercontent.com/leeyin98/figurebed/master/typoraImgs/test-16501156182614.jpg" alt="test" style="zoom:33%;max-width:33%" />
