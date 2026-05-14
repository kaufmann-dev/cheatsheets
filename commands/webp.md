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

#### Convert gif to animated .webp
```
gif2webp -mixed input.gif -o output.webp
```