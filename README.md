# Useful commands

#### Rotate picture
```
magick input.webp -rotate 90 input.webp
```

#### Resize video to specific size (without Audio)
```
resize.sh input.mp4 4
```

#### Resize video to specific size .webm
```
python restrict.py -a -s 4 input.mp4
```

#### Start http-server
```
npx http-server -p 1488
```
## GitHub
#### Clone all repos
```
gh repo list kaufmann-dev --limit 4000 | while read -r repo _; do
  gh repo clone "$repo" "$repo"
done
```

## PHP / NGINX
#### NGINX error log (includes PHP errors)
```
tail -f /var/log/nginx/error.log
```

#### Install ZIP extension
###### Install package
```
apt install php7.4-zip
```
###### Restart nginx
```
systemctl restart nginx
```

#### Restart services
###### Restart PHP FPM
```
systemctl restart php7.4-fpm
```
###### Restart nginx
```
systemctl restart nginx
```

#### Run PHP FPM as root
###### Edit pool configuration
```
nano /etc/php/7.4/fpm/pool.d/www.conf
```
```
user = root
group = root
```

###### append -R to the ExecStart
```
nano /lib/systemd/system/php7.4-fpm.service
```
```
ExecStart=/usr/sbin/php-fpm7.4 --nodaemonize --fpm-config /etc/php/7.4/fpm/php-fpm.conf -R
```

###### Reload the configuration
```
systemctl daemon-reload
```

###### Start the service
```
systemctl start php7.4-fpm
```

## .webp

#### Convert image to .webp
```
cwebp -q 75 input.jpg -o output.webp
```

#### Convert gif to animated .webp
```
gif2webp -mixed input.gif -o output.webp
```

## ffmpeg

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

## Linux
#### Rename folder
```
mv old-name new-name
```

#### Copy file
```
cp file-to-copy new-file
```

#### Download file
```
wget https://website.example/item.zip
```

#### Unzip zip folder
```
unzip folder.zip -d .
```
