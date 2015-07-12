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
    

def main():
    parser = argparse.ArgumentParser(
        description='Join and convert color json data to an image.')
    parser.add_argument('dir',
        help = 'Data source directory')
    parser.add_argument('--file-name',
        dest = 'filename',
        default = "min_%d.json",
        help = 'File name to grab json data from')
    parser.add_argument('--out',
        dest = 'out',
        default = "out.png",
        help = 'Name of image file generated.')
        
    args = parser.parse_args()

    colorData = join_files(args.dir, args.filename)
    with open(args.out, 'w') as out:
        json.dump(colorData, out)

if __name__ == "__main__":
    main()
