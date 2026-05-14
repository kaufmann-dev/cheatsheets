#### Start http-server
```
npx http-server -p 8080
```

#### NGINX error log (includes PHP errors)
```
tail -f /var/log/nginx/error.log
```

#### Install package
```
apt install php7.4-zip
```

#### Restart nginx
```
systemctl restart nginx
```

#### Restart PHP FPM
```
systemctl restart php7.4-fpm
```
#### Restart nginx
```
systemctl restart nginx
```

#### Run PHP FPM as root
##### Edit pool configuration
```
nano /etc/php/7.4/fpm/pool.d/www.conf
```
```
user = root
group = root
```

##### append -R to the ExecStart
```
nano /lib/systemd/system/php7.4-fpm.service
```
```
ExecStart=/usr/sbin/php-fpm7.4 --nodaemonize --fpm-config /etc/php/7.4/fpm/php-fpm.conf -R
```

##### Reload the configuration
```
systemctl daemon-reload
```

##### Start the service
```
systemctl start php7.4-fpm
```