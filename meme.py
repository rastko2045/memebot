from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from dotenv import load_dotenv

basewidth = 1200            #Width to make the meme
fontBase = 100              #Font size
letSpacing = 9              #Space between letters
fill = (255, 255, 255)      #TextColor
stroke_fill = (0,0,0)       #Color of the text outline
lineSpacing = 10            #Space between lines
stroke_width=9              #How thick the outline of the text is
fontfile = "./fonts/impact.ttf"

load_dotenv()
memes_dir = os.getenv('MEME_DIR')

def create_meme(memeName, text):
    img = open_meme(memeName)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontfile, fontBase)
    write_meme(text, img, draw)
    return img

def write_meme(text, img, draw):
    font = ImageFont.truetype(fontfile, fontBase)
    textLines = textwrap.wrap(text, width = 20)
    textLines.reverse()
    iw, ih = img.size
    y = ih-(ih/10)-lineSpacing
    for line in textLines:
        x = (iw - font.getsize(line)[0]) / 2
        print("Printing line: " + line + " at coordinates: " + str((x, y)))
        draw.text((x, y), line, fill, font=font, stroke_width=stroke_width, stroke_fill=stroke_fill)
        y -= font.getsize(line)[1] + lineSpacing
    return img

def open_meme(memeName):
    img = Image.open(get_meme_path(memeName))
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    return img.resize((basewidth, hsize))
    
def get_meme_path(memeName):
    return os.path.join(memes_dir, memeName + ".jpeg")