"""
Extract the dominant colors from each frame in a movie.
"""
import argparse
import os
import json
import math
import subprocess
import sys

SEC_IN_MIN = 60
MIN_IN_HOUR = 60

FRAME_FILE_NAME = "frame_%d.png"

END = 159 * SEC_IN_MIN

SAMPLE_WIDTH = 1920 / 4

def ensure_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def get_dominant_frame_color(method, file):
    """Extract the dominant color for a given file."""
    if method == "colortheif":
        from colorthief import ColorThief
        color_thief = ColorThief(file)
        return color_thief.get_color(quality=1)
    
    elif method == "colorcube":
        sys.path.append('ColorCube/Python')
        from ColorCube import ColorCube
        from PIL import Image
        cc = ColorCube(bright_threshold=0.0)
        img = Image.open(file)
        colors = cc.get_colors(img)
        return colors[0]
    
    else: # method == "colorweave" or other
        from colorweave import palette
        p = palette(path=file, n=1, mode="kmeans")
        return hex_to_rgb(p[0])
        
def clear_frames(dir):
    """Delete existing frames in a directory."""
    for f in os.listdir(dir):
        if f.endswith(".png"):
            os.remove(os.path.join(dir, f))
        
def extract_frames(src, outFile, fromTime, toTime, width):
    """Extract all frames between two times from a video."""
    command = [
        "ffmpeg",
        "-hide_banner",
        "-ss",  
        str(fromTime),
        "-i",
        src,
        "-to",
        str(toTime),
        "-vf",
        "scale=%s:-1" % width,
        outFile]
    
    with open(os.devnull, "w") as f:
        subprocess.call(command, stdout = f, stderr = f)

def process_frames(method, source):
    """Extract each dominant color from frames stored in dir."""
    i = 1
    data = []
    while True:
        print i
        file = source % i
        #if not os.path.isfile(file):
        #    break
        data.append(get_dominant_frame_color(method, file))
        i = i + 1
    return data

def to_duration(min, sec = 0):
    return "%s:%s:%s" % (
        int(math.floor(min / SEC_IN_MIN)),
        min % SEC_IN_MIN,
        sec)

def write_frame_data(method, movie, frameOut, dataOut, length, width, duration = 60):
    """
    Extract frames in groups, determine dominate color for each.
    """
    for i in range(length):
        dataFile = output % i
        if os.path.isfile(dataFile):
            continue
        print "Processing minute %s" % i
        frameFileNames = os.path.join(frameOut, FRAME_FILE_NAME)
        extract_frames(
            movie,
            frameFileNames,
            to_duration(i),
            duration,
            width)
        frameData = process_frames(method, frameFileNames)
        with open(dataFile, 'w') as out:
            json.dump(frameData, dataOut)

def main():
    parser = argparse.ArgumentParser(
        description='Find the dominant color of every frame in a movie.')
    
    parser.add_argument(
        'movie',
        help='Movie file to process')
    
    parser.add_argument(
        '--method',
        dest='method',
        default='colorweave',
        help='colortheif|colorcube|colorweave')
        
    parser.add_argument(
        '--length',
        dest='length',
        help='Length, in minutes, of the movie')
        
    args = parser.parse_args()

    method = args.method
    framedir = 'frames-' + method
    datadir = 'data-' + method
    ensure_dir(framedir)
    ensure_dir(datadir)
    clear_frames(frameDir)
    write_frame_data(
        method,
        args.movie
        framedir, 
        os.path.join(datadir, "min_%s.json"),
        args.length,
        SAMPLE_WIDTH)
    
if __name__ == "__main__":
    main()
