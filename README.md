# One Pixel Cinema

Simple python scripts for finding the dominant colors of each frame in a video.


Image representation of the dominant color of every frame in *Eyes Wide Shut*:
![](/documentation/eyes-average.png?raw=true "Eyes Wide Shut as a Image")


## Usage

### `main.py`
Uses FFMpeg to extract each frame in a movie and a third party color library to conver each frame to a dominant color. Outputs JSON files for each minute in the video.

```
python main.py --method=average "Eyes Wide Shut.mkv" --length 159
```

Name of movie and length of movie (in minutes) must be provided.

Supported methods for getting dominant color:
* `average` - Take the average of every color in the frame.
* `colortheif` - [Color Thief library][colortheif].
* `colorweave` - [Colorweave library][colorweave].
* `colorcube` - [ColorCube library][colorcube].

### `combine.py`
Combines the JSON arrays generated by `main.py` into a single json file

```
$ python combine.py data-average/ --out=average.json
```

### `image_gen.py`
Combines the JSON arrays generated by `main.py` into a png.

```
$ python image_gen.py data-average/ --out img-average.png --width 800
```


[colorthief]: https://github.com/fengsp/color-thief-py
[colorweave]: https://github.com/jyotiska/colorweave
[colorcube]: https://github.com/pixelogik/ColorCube
