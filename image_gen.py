"""
Combine json files of color data into an image.
"""
import argparse
import os
import json
import math
from PIL import Image

def join_files(dir, fileName):
    """Combine multiple json arrays stored in numbered files into a list."""
    data = []
    i = 0
    while True:
        file = os.path.join(dir, fileName % i)
        if not os.path.isfile(file):
            return data
        with open(file) as f:    
            data += json.load(f)
        i = i + 1
    
def build_image(colors, width):
    """Build an image from a list of color data."""
    height = int(math.ceil(len(colors) / float(width)))
    img = Image.new('RGB', (width, height), (127, 127, 127))
    pixels = img.load() # create the pixel map
    x = 0
    y = 0
    for c in colors:
        pixels[x, y] = (c[0], c[1], c[2])
        x = (x + 1) % width
        if x == 0:
            y = y + 1  
    return img

def main():
    parser = argparse.ArgumentParser(
        description='Join and convert color json data to an image.')
    parser.add_argument('dir',
        help = 'Data source directory')
    parser.add_argument('--file-name',
        dest = 'filename',
        default = "min_%d.json",
        help = 'File name to grab json data from')
    parser.add_argument('--width',
        dest = 'width',
        type = int,
        default = 800,
        help = 'Width of image to generate')
    parser.add_argument('--out',
        dest = 'out',
        default = "out.png",
        help = 'Name of image file generated.')
        
    args = parser.parse_args()

    colorData = join_files(args.dir, args.filename)
    img = build_image(colorData, args.width)
    img.save(args.out) 

if __name__ == "__main__":
    main()
