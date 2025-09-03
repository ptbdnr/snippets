
```shell
ffmpeg -i "patth/to/input.mov" -an -c:v libx264 -crf 42 -r 17  -preset slow "path/to/output.mp4"
```

Options:

* `-i path/to/file.ext`: input
* `-an`: audio none
* `-c:v libxx264`: compression with libx264
* `-crf 42`: compression 42 is very agressive, lot of loss
* `-r 17`: frame per seconds
* `-preset slow`: slower process tto optimise compression
* `path/to/output.ext`: output
