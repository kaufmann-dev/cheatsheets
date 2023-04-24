# Useful commands
>Make sure to put ffmpeg, ffprobe and ffplay in PATH!

### NGINX error log
```
tail -f /var/log/nginx/error.log
```

### .webp

#### Convert image to .webp
```
cwebp -q 75 input.jpg -o output.webp
```

#### Convert gif to animated .webp
```
gif2webp -mixed input.gif -o output.webp
```

### Resize video to specific size (without Audio)
```
resize.sh input.mp4 4
```

### Resize video to specific size .webm
```
python restrict.py -a -s 4 input.mp4
```

### Create video from image and audio
```
ffmpeg.exe -loop 1 -i input.jpg -i input.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output.mp4
```

### Change video format
```
ffmpeg -i input.mp4 output.webm
```

### Start http-server
```
npx http-server -p 1488
```

### Rotate/flip video with ffmpeg

#### Flip video  vertically
```
ffmpeg -i input.mp4 -vf vflip -c:a copy output.mp4
```

#### Flip video horizontally
```
ffmpeg -i input.mp4 -vf hflip -c:a copy output.mp4
```

#### Rotate 90 degrees clockwise
```
ffmpeg -i input.mp4 -vf transpose=1 -c:a copy output.mp4
```

#### Rotate 90 degrees counterclockwise
```
ffmpeg -i input.mp4 -vf transpose=2 -c:a copy output.mp4
```
