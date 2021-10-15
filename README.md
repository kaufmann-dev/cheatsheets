# Some useful commands:
>Make sure to put ffmpeg, ffprobe and ffplay in PATH!

### Convert image to .webp
```
cwebp -q 75 [image input] -o [.webp output]
```

### Resize video to specific size (without Audio)
```
resize.sh [video input] 4
```

### Resize video to specific size .webm
```
python restrict.py -a -s 4 [video input]
```

### Create video from image and audio
```
ffmpeg.exe -loop 1 -i [image input] -i [audio input] -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest [video output]
```

### Start http-server
```
npx http-server -p 1488
```

### Rotate/flip video with ffmpeg

#### Flip video  vertically
```
ffmpeg -i [video input] -vf vflip -c:a copy [video output]
```

#### Flip video horizontally
```
ffmpeg -i [video input] -vf hflip -c:a copy [video output]
```

#### Rotate 90 degrees clockwise
```
ffmpeg -i [video input] -vf transpose=1 -c:a copy [video output]
```

#### Rotate 90 degrees counterclockwise
```
ffmpeg -i [video input] -vf transpose=2 -c:a copy [video output]
```
