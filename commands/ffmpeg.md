#### Reduce video size
```
ffmpeg -i input.mp4 -vcodec libx264 -crf 20 output.mp4
```

#### Cut video from [start] 00:10:12.5 to [delay after start] 00:00:28.
```
ffmpeg -i input.mp4 -ss 00:10:12.5 -t 00:00:28.5 -async 1 -strict -2 output.mp4
```

#### Create video from image and audio
```
ffmpeg -loop 1 -i input.jpg -i input.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest output.mp4
```

#### Change video format
```
ffmpeg -i input.mp4 output.webm
```

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