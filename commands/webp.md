#### Convert image to .webp with lossy compression
```
cwebp -q 75 input.jpg -o output.webp
```

#### Convert image to .webp with lossless compression
```
cwebp -lossless input.jpg -o output.webp
```

#### Convert image to .webp and resize to fit within 1000x1000 pixel box
```
cwebp -q 75 input.jpg -resize 1000 1000 -o output.webp
```

#### Batch resize images in the current directory
```bash
webp-resize --width 1000 --height 1000 --quality 75
```
*Writes each result as `*-resized.webp` without overwriting existing files. Set either dimension to `0` to preserve the source aspect ratio.*

#### Convert gif to animated .webp
```
gif2webp -mixed input.gif -o output.webp
```
